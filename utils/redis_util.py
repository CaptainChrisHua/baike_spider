# -*- coding:utf-8 -*-
import time

import redis


class RedisUtil(object):
    # 使用示例
    """
    from algo_database_utils.redis_util import RedisUtil

    REDIS_ALGORITHMS = {
        'host': '127.0.0.1',
        'port': '6379',
        'db': '6',
        'password': '123456'
    }

    redis_util = RedisUtil(REDIS_ALGORITHMS)
    result = redis_util.get("key")
    """

    def __init__(self, redis_config: dict, decode_responses=True):
        redis_pool = redis.ConnectionPool(**redis_config,
                                          max_connections=1000,
                                          socket_connect_timeout=1,
                                          health_check_interval=30,
                                          decode_responses=decode_responses)  # 连接池方式连接，将二进制响应自动转成字符串
        self.redis_conn = redis.Redis(connection_pool=redis_pool)

    def set(self, key, value):
        return self.redis_conn.set(key, value)

    def setex(self, key, value, seconds):
        return self.redis_conn.setex(key, seconds, value)

    def incr(self, key):
        return self.redis_conn.incr(key, 1)

    def get(self, key):
        return self.redis_conn.get(key)

    def mget(self, keys):
        return self.redis_conn.mget(keys)

    def setnx(self, name, value):
        return self.redis_conn.setnx(name, value)

    def expire(self, key, time):
        return self.redis_conn.expire(key, time)

    def delete(self, key):
        return self.redis_conn.delete(key)

    def lpush(self, queue_name, value):
        """
        队列写入数据
        :param queue_name: 队列名
        :param value: 写入值
        :return:
        """
        return self.redis_conn.lpush(queue_name, value)

    def llen(self, queue_name):
        """
        队列长度
        :param queue_name: 队列名
        :return:
        """
        return self.redis_conn.llen(queue_name)

    def rpop(self, queue_name):
        """
        获取指定队列数据
        :param queue_name: 队列名称
        :return: 队列中取出来的值
        """
        return self.redis_conn.rpop(queue_name)

    def rpush(self, queue_name, value):
        """
        队列写入数据
        :param queue_name: 队列名
        :param value: 写入值
        :return:
        """
        return self.redis_conn.rpush(queue_name, value)

    def lpop(self, queue_name):
        """
        获取指定队列数据
        :param queue_name: 队列名称
        :return: 队列中取出来的值
        """
        return self.redis_conn.lpop(queue_name)

    def hgetall(self, key):
        return self.redis_conn.hgetall(key)

    def zadd(self, sortset_name, **mapping):
        result = self.redis_conn.zadd(sortset_name, mapping)
        return result > 0

    def zrange(self, sortset_name, start, end, desc=False  # pylint: disable=R0913
               , withscores=False, score_cast_func=float):
        return self.redis_conn.zrange(sortset_name, start, end, desc
                                      , withscores, score_cast_func)

    def zcard(self, sortset_name):
        return self.redis_conn.zcard(sortset_name)

    def hset(self, name, key, value, mapping=None):
        self.redis_conn.hset(name, key, value, mapping)

    def hdel(self, name, *keys):
        return self.redis_conn.hdel(name, *keys)

    def hget(self, name, key):
        result = self.redis_conn.hget(name, key)
        if result:
            result = result.decode('utf-8')
        return result

    def smembers(self, name):
        return self.redis_conn.smembers(name)

    def sismember(self, setname, value):
        return self.redis_conn.sismember(setname, value)

    def sadd(self, name, *values):
        self.redis_conn.sadd(name, *values)

    def hmget(self, name, keys, *args):
        """
        获取hashmap键值多个键值对
        """
        return self.redis_conn.hmget(name, keys, *args)

    def exists(self, key):
        return self.redis_conn.exists(key)

    def acquire_lock(self, project, env, func, timeout=10):  # 超时时间，默认10秒
        for i in range(timeout * 100):
            try:
                lock = self.setnx(f"{project}:{env}:{func}:mutex", f"expire_in_{timeout}_seconds")
                self.expire(f"{project}:{env}:{func}:mutex", timeout)
            except Exception:
                self.delete(f"{project}:{env}:{func}:mutex")
                lock = False
            if lock:
                return
            else:
                time.sleep(0.01)
        else:
            self.delete(f"{project}:{env}:{func}:mutex")
            raise TimeoutError("获取锁超时")

    def release_lock(self, project, env, func):
        self.delete(f"{project}:{env}:{func}:mutex")
