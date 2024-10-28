import redis
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor

# redis is used here for storage count ,efficient expiring and fast access
# redis Connection Configurations
REDIS_URL = "redis://localhost:6379"
pool = redis.ConnectionPool.from_url(REDIS_URL)
redis_client = redis.Redis(connection_pool=pool)

# this function synchronously checks
# if the number of requests made by a given IP address in the current 1-minute window has exceeded 100.
# if the request limit has exceeded then the true get returned
def is_rate_limited(ip: str) -> bool:
    current_time = int(time.time())
    window = current_time // 60
    requests = redis_client.incr(f"{ip}:{window}")
    if requests > 100:
        return True
    redis_client.expire(f"{ip}:{window}", 60)
    return False

async def check_rate_limit(ip: str) -> bool:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(ThreadPoolExecutor(), is_rate_limited, ip)
