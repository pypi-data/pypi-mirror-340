import asyncio
import inspect
import logging
import os
import threading
import time
import functools
import traceback
import json
from typing import Callable, Dict, Any, Coroutine, TypeVar

from fastapi import (
    FastAPI,
    Request,
    Response, HTTPException
)

from sthg_fastapi_logs.enumerate import BusinessCode, HttpStatusCode, RESULT_SUCCESS
from sthg_fastapi_logs.log_util import create_loggers, TraceID, local_trace, get_process_funcname, get_module_line, \
    get_main_tracebak, clean_error_message
from sthg_fastapi_logs.utils.code_utils import handle_method_status, handle_business_code, get_main_traceback, \
    exception_module_func
from sthg_fastapi_logs.utils.exception_utils import CustomException
from sthg_fastapi_logs.utils.response_utils import get_process_time, get_response_msg, get_request_data, \
    get_header, get_ip, get_response_data, logs_set_header

# 声明全局变量
default_config = {
    "access": {
        "enable": True,
        "is_console": False,
        "is_msg": False,
        "is_request": False,
        "is_response": False,
        "logger_level": logging.DEBUG,
        "console_level": logging.INFO,
        "acc_when": "W6",
        "backupCount": 0
    },
    "error": {
        "enable": True,
        "is_console": False,
        "is_msg": False,
        "is_request": False,
        "is_response": False,
        "logger_level": logging.ERROR,
        "console_level": logging.ERROR,
        "acc_when": "W6",
        "backupCount": 0
    },
    "all_info": {
        "enable": True,
        "is_console": False,
        "is_msg": False,
        "is_request": False,
        "is_response": False,
        "logger_level": logging.INFO,
        "console_level": logging.INFO,
        "acc_when": "W6",
        "backupCount": 0
    },
    "server": {
        "enable": True,
        "is_console": False,
        "is_msg": False,
        "is_request": False,
        "is_response": False,
        "logger_level": logging.DEBUG,
        "console_level": logging.INFO,
        "acc_when": "W6",
        "backupCount": 0
    }
}


def init_log_config(config: dict[str, dict] = None):
    global default_config, acc_logger, server_logger, error_logger, all_info
    if config:
        for key, value in config.items():
            for k, v in value.items():
                default_config[k] = v
    acc_logger, server_logger, error_logger, all_info = create_loggers(default_config)


def custom_edit_log(level: str = 'info', exc: Any = None, message: Any = None):
    """
    封装的方法，用于记录异常日志和描述
    :param logger: 日志记录器
    :param description: 对异常的描述
    :param exception: 捕获到的异常对象
    """
    if 'info' == level:
        print_message = f"{message}"
        all_info.info(print_message)
    if 'error' == level:
        print_message = f"{message}: {str(exc)}"
        error_logger.error(print_message, exc_info=exc)


def get_module_func_by_router(request):
    route = request.scope.get("route")
    if route:
        endpoint = route.endpoint
        # 获取函数的定义信息
        source_lines, start_line = inspect.getsourcelines(endpoint)
        method_name = endpoint.__name__
        module_file = inspect.getmodule(endpoint).__file__
        return module_file, method_name, start_line
    else:
        # pass
        raise HTTPException(status_code=404, detail='路由未找到，请检查请求的 URL 是否正确。')


def register_log_middleware(app: FastAPI):
    # 全局变量,以便通过中间件引入,可以进行配置
    @app.middleware("http")
    async def log_middleware(request: Request, call_next):
        _request_id_key = "X-Request-Id"
        _trace_id_key = "X-Request-Id"
        _trace_id_val = request.headers.get(_trace_id_key)
        if _trace_id_val:
            TraceID.set_trace(_trace_id_val)
            TraceID.set_trace(_trace_id_val)
        else:
            TraceID.new_trace()
            _trace_id_val = TraceID.get_trace()
        local_trace.trace_id = TraceID.get_trace()
        local_trace.request = request

        async  def set_body(request: Request):
            receive_ = await  request._receive()
            async def receive():
                return receive_
            request._receive = receive

        await set_body(request)

        return await call_next(request)


def get_exception_msg(func, exc, moduler_func_line, ):
    try:
        file_path = inspect.getfile(func)
        # 获取文件所在的目录路径
        current_dir = os.path.dirname(os.path.abspath(file_path))

        moduler_func_line = moduler_func_line if moduler_func_line else get_module_line(
            traceback.format_exc(), project_path=current_dir)
        exc_type = type(exc)
        exc_value = exc
        exc_tb = exc.__traceback__
        # 调用 format_exception 函数格式化异常信息
        formatted_exception = traceback.format_exception(exc_type, exc_value, exc_tb)
        # 打印格式化后的异常信息
        main_error = "Traceback (most recent call last):\n" + get_main_tracebak(
            ''.join(formatted_exception), project_path=current_dir)
        return main_error, moduler_func_line
    except Exception as e:
        error_logger.error('日志处理异常 :{}'.format(str(e)))


def access_log(print_message:str = "默认值"):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if default_config['access']['enable']:
                moduler_func_line, return_desc, msg = '-', '-', '-'
                start_time = time.time()
                response = None
                access_info = {
                    'header_str': "",
                    'process_time': '-',
                    "status_code": RESULT_SUCCESS,
                    "code": BusinessCode.OK,
                    'return_desc': return_desc,
                    'msg': msg,
                    'moduler_func_line': moduler_func_line,
                    'param_input': '-',
                    'respData': '-',
                    "log_time_start": '-'
                }
                try:
                    if asyncio.iscoroutinefunction(func) or 'function' not in str(type(func)):
                        response = await func(*args, **kwargs)
                        if isinstance(response, (asyncio.Future, asyncio.Task)):
                            response = await response
                    else:
                        response = func(*args, **kwargs)
                except Exception as exc:
                    process_time = get_process_time(start_time, time.time())
                    log_time_start = time.time()
                    main_error, moduler_func_line = get_exception_msg(func, exc, moduler_func_line)  #
                    if not response:
                        response = Response(status_code=500)
                    access_info['process_time'] = process_time
                    access_info['status_code'] = 'ERROR'
                    access_info['code'] = 'InnerError'
                    access_info['return_desc'] = HttpStatusCode.get_description(response.status_code)
                    access_info['msg'] = main_error
                    access_info['moduler_func_line'] = moduler_func_line
                    access_info['respData'] = '-'
                    access_info['log_time_start'] = log_time_start
                    await get_access_log_str(**access_info)
                    raise
                try:
                    process_time = get_process_time(start_time, time.time())
                    log_time_start = time.time()
                    params = await request_params()
                    header_str = logs_set_header()
                    access_info['header_str'] = header_str
                    access_info['param_input'] = params
                    method_name = func.__name__
                    module = inspect.getmodule(func)
                    if module is not None and hasattr(module, '__file__'):
                        # 获取模块对应的文件路径
                        project_root = os.getcwd()
                        module_file = module.__file__
                        relative_path = os.path.relpath(module_file, project_root)
                        module_path = relative_path.replace(os.sep, '.')[:-3]  # 去除 .py 扩展名
                        new_module_path = module_path.split('.')[-1]
                        moduler_func_line = "{}.{}".format(new_module_path, method_name)
                    if response:
                        if isinstance(response, dict):
                            new_response = response
                        else:
                            new_response = response.dict()
                        if 'code' in new_response or 'http_code' in new_response:
                            if 'code' in new_response:
                                code = new_response['code']
                            else:
                                code = new_response['http_code']
                        else:
                            raise CustomException('返回不是标准结构')
                    else:
                        raise CustomException('返回不是标准结构')
                    status_code = handle_method_status(code)
                    busiCode = handle_business_code(code)
                    if code in [0, 1]:
                        if code == 0:
                            return_desc = f"请求成功"
                        if code == 1:
                            return_desc = f"请求失败"
                    elif code in [200]:
                        return_desc = f"请求成功"
                    elif code in [400, 401, 403, 404]:
                        return_desc = HttpStatusCode.get_description(code)
                    elif code in [500]:
                        return_desc = HttpStatusCode.get_description(code)
                    else:
                        return_desc = HttpStatusCode.get_description(code)
                    access_info['process_time'] = process_time
                    access_info['status_code'] = status_code
                    access_info['code'] = busiCode
                    access_info['return_desc'] = return_desc
                    access_info['msg'] = msg
                    access_info['moduler_func_line'] = moduler_func_line
                    access_info['respData'] = response if response else '-'
                    access_info['log_time_start'] = log_time_start
                    await get_access_log_str(**access_info)
                except Exception as exc:
                    error_logger.error('日志处理异常 :{}'.format(str(exc)))
                return response
            return func(*args, **kwargs)
        return wrapper
    return decorator


"""
"time":请求时间
,"traceId":全链路Id
,"method":访问方法
,"status":http状态码
,"code":业务状态码
,"msg": 返回描述，当异常时，可以把简略堆栈放里面
,"resRT": 响应时长
,"logRT": 日志打印耗时
,"reqParams": 请求参数
,"reData": 返回参数
"""


# 记录方法执行日志
def service_log():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if default_config['server']['enable']:
                msg = '-'
                moduler_func_line = '-'
                start_time = time.time()
                try:
                    if asyncio.iscoroutinefunction(func) or 'function' not in str(type(func)):
                        response = await func(*args, **kwargs)
                        if isinstance(response, (asyncio.Future, asyncio.Task)):
                            response = await response
                    else:
                        response = func(*args, **kwargs)
                except Exception as exc:
                    error_logger.error('日志处理异常 :{}'.format(str(exc)))
                    raise
                try:
                    process_time = get_process_time(start_time, time.time())
                    log_time_start = time.time()
                    params = get_request_data(args, kwargs)
                    method_name = func.__name__
                    module = inspect.getmodule(func)
                    if module is not None and hasattr(module, '__file__'):
                        # 获取模块对应的文件路径
                        project_root = os.getcwd()
                        module_file = module.__file__
                        relative_path = os.path.relpath(module_file, project_root)
                        module_path = relative_path.replace(os.sep, '.')[:-3]  # 去除 .py 扩展名
                        new_module_path = module_path.split('.')[-1]
                        moduler_func_line = "{}.{}".format(new_module_path, method_name)
                    reData = get_response_data(response)
                    if not params: params = '-'
                    await get_service_log_str(moduler_func_line, process_time, log_time_start, RESULT_SUCCESS, "OK",
                                              "业务处理成功", msg, params, reData)
                except Exception as e:
                    error_logger.error('日志处理异常 :{}'.format(str(e)))
                return response
            return func(*args, **kwargs)
        return wrapper
    return decorator


#
def class_decorator(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        if default_config['server']['enable']:
            msg = "-"
            reData = '-'
            moduler_func_line = '-'
            params = '-'
            try:
                params = get_request_data(args, kwargs)
                method_name = func.__name__
                module = inspect.getmodule(func)
                if module is not None and hasattr(module, '__file__'):
                    # 获取模块对应的文件路径
                    project_root = os.getcwd()
                    current_dir = os.path.dirname(os.path.abspath(project_root))
                    module_file = module.__file__
                    relative_path = os.path.relpath(module_file, current_dir)
                    module_path = relative_path.replace(os.sep, '.')[:-3]  # 去除 .py 扩展名
                    new_module_path = module_path.split('.')[-1]
                    moduler_func_line = "{}.{}".format(new_module_path, method_name)
            except  Exception as e:
                error_logger.error('日志处理异常 :{}'.format(str(e)))
            start_time = time.time()
            try:
                response = func(*args, **kwargs)
            except Exception as exc:
                error_logger.error('日志处理异常 :{}'.format(str(exc)))
                raise
            process_time = get_process_time(start_time, time.time())
            log_time_start = time.time()
            reData = response if response else reData
            await get_service_log_str(moduler_func_line, process_time, log_time_start, "SUCCESS", 'OK', '业务处理成功',
                                      msg, params, reData)
            return response
        return func(*args, **kwargs)

    return wrapper


def class_log(cls):
    for name, method in vars(cls).items():
        if callable(method) and name != '__init__':  # 排除__init__方法
            setattr(cls, name, class_decorator(method))
    return cls


async def get_access_log_str(**access_kwargs):
    # acc_logger, server_logger, error_logger, all_info = create_loggers(default_config)
    try:

        header_str = access_kwargs['header_str']
        msg = clean_error_message(access_kwargs['msg'])
        moduler_func_line = str(access_kwargs['moduler_func_line']).replace('...', '')
        status_code = access_kwargs['status_code']
        code = access_kwargs['code']
        return_desc = access_kwargs['return_desc']
        process_time = access_kwargs['process_time']
        param_input = access_kwargs['param_input']
        respData = access_kwargs['respData']
        log_time_start = access_kwargs['log_time_start']
        logRT = get_process_time(log_time_start, time.time())
        info_msg = f"""{moduler_func_line}\t {status_code}\t {code}\t {return_desc}\t {process_time}\t {logRT}\t {header_str}\t {param_input}\t {respData}\t {msg}"""

        acc_logger.info(str(info_msg))
    except Exception as e:
        error_logger.error('日志记录异常 :{}'.format(str(e)))


async def get_error_log(header_str, status_code, code, msg, module_line="-"):
    try:
        t1 = time.time()
        module_line = str(module_line).replace('...', '')
        logRT = get_process_time(t1, time.time())
        info_msg = f'{module_line}\t {status_code}\t {code}\t {logRT}\t {header_str}\n{msg}'
        error_logger.error(str(info_msg))
    except Exception as e:
        error_logger.error('日志记录异常 :{}'.format(str(e)))
        raise e


async def get_service_log_str(
        method, process_time, log_time_start, status_code, code, return_desc, msg, reqParam, reData):
    try:
        msg = clean_error_message(msg)
        logRT = get_process_time(log_time_start, time.time())
        service_msg = f"""{method}\t {status_code}\t {code}\t {return_desc}\t {process_time}\t {logRT}\t {reqParam}\t {reData} {msg}"""
        server_logger.debug(str(service_msg))
    except Exception as e:
        error_logger.error('service log error :{}'.format(str(e)))


async def request_params():
    try:
        request = local_trace.request
        # 查询参数
        query_params = dict(request.query_params)

        content_type = request.headers.get('content-type') if request.headers.get('content-type') else ''
        # 表单数据
        form_data = {}
        # 不可识别数据
        others = ''
        # 请求体数据
        body_data = {}
        if content_type and 'application/json' in content_type:
            body_data = await asyncio.wait_for(request.body(), timeout=5)
            body_data = json.dumps(body_data.decode())
        elif content_type and 'multipart/form-data' in content_type:
            if 'multipart/form-data; boundary=' in content_type:
                form = await asyncio.wait_for(request.form(), timeout=5)
                has_file = False
                for field_name, value in form.items():
                    if hasattr(field_name, 'filename'):
                        has_file = True
                        break
                if has_file:
                    form_data["file_upload"] = 1
                else:
                    form = await asyncio.wait_for(request.form(), timeout=5)
                    form_data = {key: value for key, value in form.items()}
            else:
                form = await asyncio.wait_for(request.form(), timeout=5)
                form_data = {key: value for key, value in form.items()}
        elif content_type and 'application/x-www-form-urlencoded' in content_type:
            form = await asyncio.wait_for(request.form(), timeout=5)
            form_data = {key: value for key, value in form.items()}
        else:
            others = '-'
        params_input = {}
        if query_params:
            params_input['params'] = query_params
        if form_data:
            params_input['form_data'] = form_data
        if body_data:
            params_input['body'] = body_data
        if others:
            params_input['others'] = others
        return params_input
    except Exception as e:
        error_logger.error('日志处理异常 :{}'.format(str(e)))

