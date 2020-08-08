import redis
import logging

logger = logging.getLogger('redis')


class RedisConn:
    redis_conn = None

    @classmethod
    def init(cls, host, port, password, db):
        if password is not None:
            url = 'redis://:%s@%s:%s/%s' % (password, host, port, db)
        else:
            url = 'redis://@%s:%s/%s' % (host, port, db)

        logger.info('redis url:%s' % url)

        cls.redis_conn = redis.from_url(url)
