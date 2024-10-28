import hashlib
import base64
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import URL

# This function does the work of the converting to 128bit hash for input
# .digest() converts that to binary string to byte
# hased_url into a base64-encoded, URL-safe string and the decode it to UTF-8
def generate_slug(url: str) -> str:
    hashed_url = hashlib.md5(url.encode()).digest()
    return base64.urlsafe_b64encode(hashed_url).decode()[:8]

# Function Generates the slug
# Checks if it is already made in the database
# This process repeats until a unique slug is found and returned.
async def get_unique_slug(original_url: str, db: AsyncSession) -> str:
    slug = generate_slug(original_url)
    while True:
        result = await db.execute(select(URL).filter_by(short_url=slug))
        existing_url = result.scalar_one_or_none()
        if not existing_url:
            return slug
        slug = generate_slug(slug + original_url)
