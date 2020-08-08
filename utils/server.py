from flask import Flask
from gevent.pywsgi import WSGIServer
from utils.signal_tool import SignalTool
from utils.log_tool import log_init
from utils.redis_tool import RedisConn
import logging
import traceback
logger = logging.getLogger('server')


# 服务器类
class MallServer:
    init_register = None
    app = Flask('')
    config = None

    @classmethod
    def init(cls):
        """
        初始化
        注册路由
        异常处理
        钩子函数，请求前处理与请求后处理

        """
        cls.init_register()

        # cls.app.errorhandler(Exception)
        # cls.app.before_request()
        # cls.app.after_request()

    @classmethod
    def run(cls, ip, port):
        logger.info(f'The server listen at: {port}')
        server = WSGIServer((ip, port), cls.app)
        server.serve_forever()
        logger.info('===============server start===============')


class Application:
    @classmethod
    def init(cls, config):
        try:
            SignalTool.init(config.pid_path)
            log_init(config.log_path, config.log_level, config.log_reverse, config.log_to_console)
            RedisConn.init(config.redis_host, config.redis_post, config.redis_password, config.redis_db)
        except Exception as e:
            logger.critical(f'application init fail: {e}')
            logger.critical(traceback.format_tb(e.__traceback__))
            exit(1)

    @classmethod
    def run(cls, config):
        MallServer.run(ip=config.ip, port=config.port)

    @classmethod
    def main(cls):
        cls.init(MallServer.config)
        cls.run(MallServer.config)
