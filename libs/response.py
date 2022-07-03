from django.http import JsonResponse

from libs.res_code import Code, error_map


def json_response(result_code=Code.OK, message=error_map[Code.OK], data=None, **kwargs):
    """返回 JSON 序列化响应"""

    js_dict = {
        "result_code": result_code,
        "message": message,
        "data": data
    }
    js_dict.update(**kwargs)

    return JsonResponse(js_dict, json_dumps_params={"ensure_ascii": False})
