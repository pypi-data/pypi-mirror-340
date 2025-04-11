

from email.policy import default


def translate_scholar_socket_support_state(state:str):
    match state:
        case "NO_NEED_SUPPORT":
            return "不需要支持"
        case "NOT_SUPPORT_YET":
            return "暂未支持"
        case "ALREADY_SUPPORT":
            return "支持"

    return "未知"