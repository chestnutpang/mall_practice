from gevent import pool, monkey
monkey.patch_all()

gevent_pool = pool.Pool(45)
