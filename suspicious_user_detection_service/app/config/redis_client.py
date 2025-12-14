import asyncio
import redis.asyncio as redis
from app.config.config import redis_password

redis_client = redis.Redis(
    host='redis-17279.c91.us-east-1-3.ec2.redns.redis-cloud.com',
    port=17279,
    decode_responses=True,
    username="default",
    password=redis_password,
)

async def test_redis():
    await redis_client.set('foo', 'bar')
    result = await redis_client.get('foo')
    return result


