# server.py
import os
from mcp.server.fastmcp import FastMCP

from api_driver import HAIHandler

# Create an MCP server
mcp = FastMCP("HAI(Hyper Application Inventor) MCP Server")
hai_handler = HAIHandler(os.environ["TENCENTCLOUD_SECRET_ID"],
                         os.environ["TENCENTCLOUD_SECRET_KEY"])


@mcp.resource("resources://hai_introduction")
def hai_introduction():
    """关于腾讯云HAI的介绍"""
    intro = """高性能应用服务（Hyper Application Inventor，HAI）是一款面向 AI 和科学计算的\
    GPU/NPU 应用服务产品，提供即插即用的强大算力和常见环境。它可以帮助中小企业和开发者快速部署语言模型（LLM）、\
    AI 绘图、数据科学等高性能应用，原生集成配套的开发工具和组件，大大提升应用层的开发生产效率。
    """
    return intro


@mcp.resource("resources://hai_regions")
def get_all_regions_for_hai() -> dict[str, dict[str, str]]:
    """获取HAI服务支持的所有地域的详细信息
    return:
    地域详细信息的Mapper
    在给用户展示时, 除地域编码外, 其余应该使用中文
    """
    regions = hai_handler.get_regions()
    region_info = {}
    for region in regions:
        region_info[region.Region] = {
            "地域中文名称": region.RegionName,
            "区域状态": region.RegionState,
            "是否支持学术加速": region.ScholarRocketSupportState,
        }

    return region_info


@mcp.resource("resources://hai_instances/{regions}")
def get_instances_in_hai(regions: str):
    """获取HAI中的实例信息(服务器信息)

    Args:
        regions: 地域编码的以逗号分隔的字符串, 比如ap-shanghai,ap-nanjing, 当指定为all时,
        获取所有region的实例信息

    return:
        实例信息的字典, key为地域, value为实例信息组成的列表
    """

    if regions == "all":
        region_ls = []
    else:
        region_ls = regions.split(",")

    return hai_handler.get_instances(region_ls)


@mcp.resource("resources://application_templates")
def application_templates():
    """获取HAI上所有的应用信息
    return:
        应用信息的字典组成的列表, 其中ApplicationId为应用的Id(创建实例时使用), Description描述了应用的使用场景
    """
    return hai_handler.get_applications()


@mcp.resource("resource://instance_type")
def instance_type():
    """HAI服务器支持的机型
    return:
        csv文件:
        bundle_type: 机型代号, 创建实例时bundle_type取值范围为该列,
        如XL, 创建实例时的bundle_type字段从此处查找
        bundle_name: 机型名称, 在applications描述中使用该字段说明应用至少需要的实例级别, 如GPU基础型
        description: 对机型的补充描述
        gpu_performance: 机型的总GPU算力
        gpu_mem: GPU显存大小
    """
    with open("./bundle_type.csv", "r", encoding="utf-8") as fp:
        return fp.read()


@mcp.tool("create_instance")
def create_instance(region: str, application_id: str, bundle_type: str):
    """购买并创建HAI实例

    Args:
        region: 实例所在reigon, 默认设置为ap-shanghai
        application_id: 实例的应用模版id,
        关于应用模版的定义见: resources://application_templates,
        application_id允许的全部值都包含在application_templates中, 其他值非法
        如果用户未在对话中指定, 则需要用户进行选择
        bundle_type: 实例的机型, 关于可选的机型见: resource://instance_type,
        bundle_type的可取值全部包含在instance_type中, 其他值非法
        如果用户未指定, 则需要用户进行选择

    return:
        已创建机型的实例ID和requestID

    在实例创建完成之后, 助手应该使用:
    resources://login_method/{region}/{instance_id} 查询实例的登录方式并展示给用户

    应该提醒用户, 当请求成功时, 实例有可能还处在创建中的状态, 需要用户等待创建成功

    """
    return hai_handler.create_instance(region, application_id, bundle_type)


@mcp.resource("config://region/{instance_ids_str}")
def find_instance_region(instance_ids_str: str) -> dict[str, str]:
    """查找实例id所属的region

    Args:
        instance_ids_str: 实例id以逗号分隔组成的字符串, 比如hai-xx1,hai-xx2

    return:
        字典, 字典的key是实例id, 字典的value是实例所处的region
    """

    return hai_handler.find_instances_region(instance_ids_str.split(","))


@mcp.tool("start_instance",
          description="used to start or power on the instance")
def start_instance(region: str, instance_id: str) -> str:
    """将指定实例开机
    Args:
        region: 实例所在的region, 如果用户没有明确指出,
        可以通过resources://hai_instances/all进行查询
        instance_id: 实例id, 需要用户指定, 如果用户未指定, 则不能执行此任务
    """
    resp = hai_handler.start_instance(region, instance_id)
    return f"开机任务提交成功, 请耐心等待开机, 服务器返回结果: {resp}"


@mcp.tool("stop_instance", description="used to power off the instance")
def stop_instance(region: str, instance_id: str) -> str:
    """将指定实例关机
    Args:
        region: 实例所在的region, 如果用户没有明确指出,
        可以通过resources://hai_instances/all进行查询
        instance_id: 实例id, 需要用户指定, 如果用户未指定, 则不能执行此任务
    """
    resp = hai_handler.stop_instance(region, instance_id)
    return f"关机任务提交成功, 请耐心等待关机, 服务器返回结果: {resp}"


@mcp.tool("remove_instance")
def remove_instance(region: str, instance_id_ls: list[str]):
    """用于将指定实例删除、退还
    Args:
        region: 实例所在的region, 如果用户没有明确指出,
        可以通过find_instance_region进行查询
        instance_id_ls: 实例id组成的列表, 列表中的实例需要处于指定的region内, 需要用户指定,
        如果用户未指定, 则不能执行此任务
    Note: 该操作会删除该实例, 需要明确提醒用户该操作带来的风险, 提醒用户做好数据备份
    """
    resp = hai_handler.remove_instance(region, instance_id_ls)
    return f"实例删除成功, 服务器返回结果: {resp}"


@mcp.tool("query_instance_network")
def query_instance_network(region: str, instance_id_ls: list[str]):
    """查询实例的网络配置及消耗情况
    Args:
        region: 实例所在的region, 如果用户没有明确指出,
        可以通过find_instance_region进行查询
        instance_id_ls: 实例id组成的列表, 列表中的实例需要处于指定的region内, 需要用户指定,
        如果用户未指定, 则不能执行此任务

    return:
        实例网络状态组成的字典

    应该使用中文给用户解释每个字段的含义
    """
    return hai_handler.query_instance_network(region, instance_id_ls)


@mcp.resource("resources://login_method/{region}/{instance_id}")
def login_method(region: str, instance_id: str):
    """查询实例上的运行的服务及可以登录的web url
    Args:
        region: 实例所处的region
        instance_id: 实例id
    """
    return hai_handler.query_login_info(region, instance_id)


if __name__ == "__main__":
    mcp.run(transport="stdio")
