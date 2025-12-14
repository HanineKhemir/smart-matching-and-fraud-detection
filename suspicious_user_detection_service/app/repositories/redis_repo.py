from app.config.redis_client import redis_client, test_redis

async def add_to_set(set_key: str, value: str, ttl_seconds: int = 86400*30):
    exists = await redis_client.exists(set_key)
    result= await redis_client.sadd(set_key, value)
    if not exists:
        await redis_client.expire(set_key, ttl_seconds)
    return result

async def is_member_of_set(set_key: str, value: str) -> bool:
    return await redis_client.sismember(set_key, value)

async def increment_id_key(key: str, ttl_seconds: int = 86400):
    exists = await redis_client.exists(key)
    if not exists:
        await redis_client.set(key, 0, ex=ttl_seconds)
    return await redis_client.incr(key)


async def test():
    await add_to_set("myset", "element1",60)
    print(await is_member_of_set("myset", "element1"))  # True

    await increment_id_key("user:counter",60)
    print(await increment_id_key("user:counter"))  # 1
    print(await increment_id_key("user:counter"))  # 2
