import json
import functools
import hashlib
from typing import Any, Callable, Optional

from loguru import logger

from app.core.config import settings


class CacheBackend:
    """缓存后端抽象基类，支持 Redis 和内存两种模式。"""

    def get(self, key: str) -> Optional[str]:
        raise NotImplementedError

    def set(self, key: str, value: str, ttl: int = 300) -> None:
        raise NotImplementedError

    def delete(self, key: str) -> None:
        raise NotImplementedError

    def delete_pattern(self, pattern: str) -> None:
        raise NotImplementedError


class MemoryCache(CacheBackend):
    """内存缓存（开发/降级用），基于 dict + 简单过期。"""

    def __init__(self):
        self._store: dict[str, tuple[str, float]] = {}
        import time
        self._time = time

    def get(self, key: str) -> Optional[str]:
        entry = self._store.get(key)
        if entry is None:
            return None
        value, expire_at = entry
        if expire_at > 0 and self._time.time() > expire_at:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: str, ttl: int = 300) -> None:
        expire_at = self._time.time() + ttl if ttl > 0 else 0
        self._store[key] = (value, expire_at)

    def delete(self, key: str) -> None:
        self._store.pop(key, None)

    def delete_pattern(self, pattern: str) -> None:
        import fnmatch
        keys_to_delete = [k for k in self._store if fnmatch.fnmatch(k, pattern)]
        for k in keys_to_delete:
            del self._store[k]


class RedisCache(CacheBackend):
    """Redis 缓存后端。"""

    def __init__(self):
        import redis
        self._client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD or None,
            db=settings.REDIS_DB,
            decode_responses=True,
            socket_connect_timeout=3,
            socket_timeout=3,
            retry_on_timeout=True,
        )

    def get(self, key: str) -> Optional[str]:
        try:
            return self._client.get(key)
        except Exception as e:
            logger.warning(f"Redis GET 失败 key={key}: {e}")
            return None

    def set(self, key: str, value: str, ttl: int = 300) -> None:
        try:
            self._client.set(key, value, ex=ttl)
        except Exception as e:
            logger.warning(f"Redis SET 失败 key={key}: {e}")

    def delete(self, key: str) -> None:
        try:
            self._client.delete(key)
        except Exception as e:
            logger.warning(f"Redis DELETE 失败 key={key}: {e}")

    def delete_pattern(self, pattern: str) -> None:
        try:
            keys = self._client.keys(pattern)
            if keys:
                self._client.delete(*keys)
        except Exception as e:
            logger.warning(f"Redis DELETE_PATTERN 失败 pattern={pattern}: {e}")


_cache_backend: Optional[CacheBackend] = None


def get_cache() -> CacheBackend:
    """获取缓存后端单例。优先 Redis，Redis 不可用时降级为内存缓存。"""
    global _cache_backend
    if _cache_backend is not None:
        return _cache_backend

    if settings.REDIS_ENABLED:
        try:
            _cache_backend = RedisCache()
            _cache_backend.set("__health_check__", "1", ttl=10)
            logger.info("Redis 缓存已启用")
            return _cache_backend
        except Exception as e:
            logger.warning(f"Redis 连接失败，降级为内存缓存: {e}")

    _cache_backend = MemoryCache()
    logger.info("使用内存缓存（开发模式）")
    return _cache_backend


def invalidate_cache(pattern: str) -> None:
    """失效匹配 pattern 的所有缓存。"""
    get_cache().delete_pattern(pattern)


def make_cache_key(prefix: str, *args, **kwargs) -> str:
    """根据参数生成缓存键。"""
    raw = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True, default=str)
    return f"{prefix}:{hashlib.md5(raw.encode()).hexdigest()}"


def cached(prefix: str, ttl: int = 300):
    """装饰器：缓存函数返回值（JSON 序列化）。"""
    def decorator(func: Callable):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            cache = get_cache()
            key = make_cache_key(prefix, func.__name__, *args, **kwargs)
            cached_value = cache.get(key)
            if cached_value is not None:
                return json.loads(cached_value)
            result = await func(*args, **kwargs)
            cache.set(key, json.dumps(result, default=str), ttl=ttl)
            return result

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            cache = get_cache()
            key = make_cache_key(prefix, func.__name__, *args, **kwargs)
            cached_value = cache.get(key)
            if cached_value is not None:
                return json.loads(cached_value)
            result = func(*args, **kwargs)
            cache.set(key, json.dumps(result, default=str), ttl=ttl)
            return result

        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    return decorator