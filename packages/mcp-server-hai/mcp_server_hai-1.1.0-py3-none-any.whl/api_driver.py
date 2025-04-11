from typing import Optional
from tencentcloud.common import credential
from tencentcloud.hai.v20230812 import models, hai_client
import os


class HAIHandler:

    def __init__(self,
                 secret_id: str,
                 secret_key: str,
                 token: Optional[str] = "") -> None:
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.token = token
        self.default_region = "ap-shanghai"

    def get_client(self, region: str):
        cred = credential.Credential(self.secret_id, self.secret_key,
                                     self.token)
        return hai_client.HaiClient(cred, region)

    def get_regions(self) -> list[models.RegionInfo]:
        """获取所有地域"""
        req = models.DescribeRegionsRequest()
        resp = self.get_client(self.default_region).DescribeRegions(req)

        if not isinstance(resp.RegionSet, list):
            return []

        return resp.RegionSet

    def get_all_region_code(self) -> list[str]:
        return [
            item.Region for item in self.get_regions()
            if isinstance(item.Region, str)
        ]

    def get_instances(
        self,
        region_ls: Optional[list[str]] = None
    ) -> dict[str, list[models.Instance]]:

        if not region_ls:
            region_ls = self.get_all_region_code()

        res = {}
        for region in region_ls:
            res[region] = self.get_instances_for_region(region)

        return res

    def get_instances_for_region(self, region: str) -> list[models.Instance]:
        req = models.DescribeInstancesRequest()
        resp = self.get_client(region).DescribeInstances(req)

        if not isinstance(resp.InstanceSet, list):
            return []
        return resp.InstanceSet

    def find_instances_region(self, instance_id_ls: list[str]):
        """寻找实例所处的region"""
        ins_to_region = {}
        for region, instance_ls in self.get_instances().items():
            for instance in instance_ls:
                if instance.InstanceId in instance_id_ls:
                    ins_to_region[instance.InstanceId] = region

        for instance_id in instance_id_ls:
            if instance_id not in ins_to_region:
                ins_to_region[instance_id] = "unknown"

        return ins_to_region

    def get_applications(self, region: Optional[str] = ""):
        if not region:
            region = self.default_region
        req = models.DescribeApplicationsRequest()
        resp = self.get_client(region).DescribeApplications(req)
        return resp.ApplicationSet

    def create_instance(self, region: str, application_id: str,
                        bundle_type: str):
        req = models.RunInstancesRequest()
        req.ApplicationId = application_id
        req.BundleType = bundle_type
        resp = self.get_client(region).RunInstances(req)
        return resp

    def start_instance(self, region: str, instance_id: str):
        req = models.StartInstanceRequest()
        req.InstanceId = instance_id
        resp = self.get_client(region).StartInstance(req)
        return resp

    def stop_instance(self, region: str, instance_id: str):
        req = models.StopInstanceRequest()
        req.InstanceId = instance_id
        return self.get_client(region).StopInstance(req)

    def remove_instance(self, region: str, instance_id_ls: list[str]):
        req = models.TerminateInstancesRequest()
        req.InstanceIds = instance_id_ls
        return self.get_client(region).TerminateInstances(req)

    def query_instance_network(self, region: str, instance_id_ls: list[str]):
        req = models.DescribeInstanceNetworkStatusRequest()
        req.InstanceIds = instance_id_ls
        return self.get_client(region).DescribeInstanceNetworkStatus(req)

    def query_login_info(self, region: str, instance_id: str):
        req = models.DescribeServiceLoginSettingsRequest()
        req.InstanceId = instance_id
        return self.get_client(region).DescribeServiceLoginSettings(req)


if __name__ == "__main__":
    handler = HAIHandler(os.environ["TENCENTCLOUD_SECRET_ID"],
                         os.environ["TENCENTCLOUD_SECRET_KEY"])

    print(handler.find_instances_region(["hai-62rfhmf8", "hai-183g6z7u"]))
