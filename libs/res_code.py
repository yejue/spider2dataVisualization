class Code:
    OK = "200"

    PARAM_ERR = "4001"
    CONNECT_ERR = "5001"
    UNKNOWN_ERR = "-1"


error_map = {
    Code.OK: "成功",
    Code.UNKNOWN_ERR: "未知错误",
    Code.PARAM_ERR: "参数值错误",
    Code.CONNECT_ERR: "爬虫连接错误",
}
