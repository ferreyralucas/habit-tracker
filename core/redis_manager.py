"""Wrapper over redis for this project."""
import socket
import datetime

from django.conf import settings

import redis

redis_client = None


def get_redis_client():
    """Get a redis client using defined settings."""
    global redis_client
    if not redis_client:
        redis_client = redis.StrictRedis.from_url(settings.REDIS_LOCK_URL)

    return redis_client


class RedisQueue(object):
    """Simple Queue with Redis Backend"""

    def __init__(self, name, namespace='queue', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.key = '%s:%s' % (namespace, name)
        self._db = get_redis_client()

    def qsize(self):
        """Return the approximate size of the queue."""
        return self._db.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def push(self, item, time=datetime.timedelta(minutes=30)):
        """Put item into the queue with expiry time (default: 30 minutes)."""
        self._db.rpush(self.key, item)
        self.expire(time)

    def pop(self, block=True, timeout=None):
        """Remove and return an item from the queue.

        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self._db.blpop(self.key, timeout=timeout)
        else:
            item = self._db.lpop(self.key)

        if item:
            item = item[1]
        return item

    def items(self):
        """Return all items from queue."""
        return self._db.lrange(self.key, 0, -1)

    def remove(self, item):
        self._db.lrem(self.key, 0, item)

    def exists(self, item):
        items = list(self.items())
        return item in items

    def pop_nowait(self):
        """Equivalent to pop(False)."""
        return self.pop(False)

    def destroy(self):
        self._db.delete(self.key)

    def expire(self, time):
        self._db.expire(self.key, time)


class RedisLock(object):
    """Redis Lock implementation over redis.StrictRedis.lock.

    :param name: Key to use in redis.
    :type name: str
    :param owner: Lock's owner by default hostname.
    :type owner: str
    :param options: Options for redis.StrictRedis.lock
    :type options: dict

    """

    def __init__(self, name, owner=None, **options):
        self.name = name
        self._owner = None
        if self._owner is None:
            self._owner = socket.gethostname()
        # self._redis_client = self.get_redis_client()
        self._redis_client = get_redis_client()
        self._lock = None
        self._lock_acquired = False
        self._options = options

    def __enter__(self):
        blocking = self._options.get('blocking', True)
        expire = self._options.get('expire', None)
        self.acquire(blocking=blocking, expire=expire)
        return self

    def __exit__(self, type_, value, tb):
        self.release()

    # def get_redis_client(self):
    #     """Get a redis client using defined settings."""
    #     redis_client = redis.StrictRedis(**(settings.REDIS_LOCK))

        return redis_client

    def acquire(self, blocking=True, expire=None):
        """Return whether the lock was acquired or not.

        :param blocking: If we should block or not while try to get the log.
        :type blocking: bool.
        :param expire: Second before the lock expires.
        :type expire: number

        :return: Flag indicating if the lock was acquired or not.
        :rtype: bool

        """
        self._lock = self._redis_client.lock(self.name, timeout=expire)
        self._lock_acquired = self._lock.acquire(blocking=blocking)
        return self._lock_acquired

    def release(self):
        """Return whether the lock was released or not.

        :return: Flag indicating if the lock was released or not.
        :rtype: bool

        """
        if self.acquired:
            self.lock.release()
            return True
        return False

    @property
    def owner(self):
        return self._owner

    @property
    def acquired(self):
        """Returns whether the lock is acquired or not."""
        return self._lock_acquired

    @property
    def lock(self):
        """Returns the redis.lock instance (low-level API)."""
        return self._lock
