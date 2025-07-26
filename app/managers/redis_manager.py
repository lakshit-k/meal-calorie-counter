import redis.asyncio as redis
from app.config.settings import Settings as settings

class RedisManager:
    _redis_client: redis.Redis = None

    @classmethod
    async def get_client(cls) -> redis.Redis:
        if cls._redis_client is None:
            cls._redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        return cls._redis_client

    @classmethod
    async def close_client(cls):
        if cls._redis_client:
            await cls._redis_client.close()
            cls._redis_client = None

    @classmethod
    async def set_key_with_ttl(cls, key: str, value: str, ttl: int):
        client = await cls.get_client()
        await client.setex(key, ttl, value)

    @classmethod
    async def get_key(cls, key: str):
        client = await cls.get_client()
        return await client.get(key)

    @classmethod
    async def delete_key(cls, key: str):
        client = await cls.get_client()
        await client.delete(key)
