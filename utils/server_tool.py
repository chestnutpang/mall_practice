from flask import Blueprint
import functools
import logging

logger = logging.getLogger('server_tool')


class MallBlueprint(Blueprint):
    def route(self, rule, **options):
        super_obj = super()

        def resp_decorator(func):
            @functools.wraps(func)
            def wrapped(*args, **kwargs):
                resp = func(*args, **kwargs)
                if isinstance(resp, (dict, list)):
                    resp = {'result': resp}
                logger.debug(f'response: {resp}')
                return resp
            super_obj.route(rule, **options)(wrapped)
            return wrapped
        return resp_decorator


# 钩子函数（请求前）
def before_request():
    pass


# 钩子函数（请求后）
def after_request(response):
    return response


# 错误处理
def handle_error(error):
    return {
        'error': f'{error}'
    }


