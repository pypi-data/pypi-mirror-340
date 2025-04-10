"""
@Author  ：duomei
@File    ：response_utils.py
@Time    ：2025/4/8 14:23
"""

from sthg_fastapi_logs.log_util import local_trace, TraceID


def get_process_time(start_time, end_time):
    return '{}'.format(round((end_time - start_time) * 1000, 6))


def get_ip(request):
    return request.client.host


def get_header(request):
    return dict(request.headers)


def get_response_msg(response):
    if response and type(response) == dict:
        msg = response.get('msg') or response.get('message') or response.get('Message')
    else:
        msg = "-"
    return msg


def get_response_data(response):
    if response :
        msg = response
    else:
        msg = "-"
    return msg


def get_request_data(args, kwargs):
    params = {
        'args': args[1:],
        'kwargs': kwargs
    }
    if not params:
        params = '-'
    return params

# 依赖函数，用于获取所有类型的参数



def logs_set_header():
    request = local_trace.request
    request_header = get_header(request)
    guid = request_header.get('X-GUID') if request_header.get('X-GUID') else "-"
    requestId = TraceID.get_trace() if TraceID.get_trace() else "-"
    if request_header.get('X-User-ID'):
        userId = request_header.get('X-User-ID')
    elif request_header.get('user_id'):
        userId = request_header.get('user_id')
    else:
        userId = "-"
    header = {"user_ip": get_ip(request), "host": request_header['host'], 'user_id': userId}
    return f'{guid}\t {userId}\t {requestId}\t header-{header}'

