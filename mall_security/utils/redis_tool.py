import aioredis
import logging


logger = logging.getLogger('redis')


class RedisConn:
    @classmethod
    async def redis_init(cls, app, loop):
        app.redis = await aioredis.create_redis_pool(
            address=(app.server_config.redis_host, app.server_config.redis_port),
            db=app.server_config.redis_db,
            password=app.server_config.redis_password,
            loop=loop
        )
