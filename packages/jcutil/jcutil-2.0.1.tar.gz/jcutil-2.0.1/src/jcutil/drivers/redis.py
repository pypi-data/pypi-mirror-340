# Redis driver
# please install redis-py
#
import asyncio
import time
from datetime import timedelta
from functools import wraps
from typing import Any, Optional, Protocol, Union
from uuid import uuid4

from redis.asyncio import Redis
from redis.asyncio.cluster import RedisCluster

__clients = {}


class RedisClientP(Protocol):
    async def exists(self, key) -> bool: ...
    async def get(self, key) -> Any: ...
    async def set(self, key, value, ex: Optional[int] = None) -> bool: ...
    async def setnx(self, key, value) -> int: ...
    async def delete(self, key) -> int: ...
    async def expire(self, key, seconds) -> int: ...


async def new_client(uri: str, tag: str = None):
    if tag is None:
        tag = uuid4()

    if uri.startswith('cluster'):
        __clients[tag] = RedisCluster.from_url(uri)
    else:
        __clients[tag] = Redis.from_url(uri)


def connect(tag: Union[str, int] = 0) -> RedisClientP:
    pool = __clients.get(tag, None)
    if pool:
        return pool
    raise RuntimeWarning(f'Not found redis client with name: {tag}')


async def load(conf: dict):
    if conf and len(conf) > 0:
        for key in conf:
            await new_client(conf[key], key)
            # print(f'redis: {key} connected')


conn = get_client = connect


class Lock:
    def __init__(self, tag, lock_flg):
        self._client = connect(tag)
        self._flg = lock_flg
        self._owner = False

    async def acquire(self, blocking=True, timeout=None):
        if not blocking and timeout is not None:
            raise ValueError("can't specify timeout for non-blocking acquire")
        start_time = int(time.time())
        while await self._client.exists(self._flg):
            if not blocking:
                break
            await asyncio.sleep(0.5)
            curr_time = int(time.time())
            if isinstance(timeout, int) and curr_time - start_time > timeout:
                return False
        r = await self._client.setnx(self._flg, int(time.time()))
        if r:
            self._owner = True
            return True
        return False

    async def release(self):
        if self._owner:
            await self._client.delete(self._flg)
            self._owner = False

    @property
    def locked(self):
        return self._owner


class SpinLock(Lock):
    def __init__(self, tag, flag, blocking=True, timeout=None):
        super(SpinLock, self).__init__(tag, flag)
        self._blocking = blocking
        self._timeout = timeout

    async def __aenter__(self):
        r = await self.acquire(self._blocking, self._timeout)
        if not r:
            raise RuntimeError(f'Cannot acquire lock: {self._flg}')
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.release()


class IntervalLimitError(RuntimeError):
    pass


def interval_lock(flg, name, timeout=timedelta(seconds=3)):
    def limit_ann(fn):
        @wraps(fn)
        async def wrapped(*args, **kwargs):
            client = connect(flg)
            time_limit = int(timeout.total_seconds())
            if await client.exists(name):
                raise IntervalLimitError(
                    f'time interval limit in {time_limit}s')
            await client.setnx(name, time.time())
            await client.expire(name, time_limit)
            return await fn(*args, **kwargs)
        return wrapped
    return limit_ann
