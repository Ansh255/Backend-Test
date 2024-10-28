from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db, engine
from models import Base, URL
from schemas import URLCreate, URLResponse
from fastapi.middleware.cors import CORSMiddleware
from utils import get_unique_slug
from rate_limiter import check_rate_limit
from datetime import datetime
from fastapi.responses import RedirectResponse  # Import RedirectResponse

# start the redis server 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with a list of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # You can specify allowed methods
    allow_headers=["*"],  # You can specify allowed headers
)

# On startup this function gets called
# Main work of this function is to set the database connection .
# if the database schema are not present then it makes the schema automatically
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Function Parameter working
# Request is which type of request, Here HTTP
# url_data contains the data coming from the request body
# Function Working
# Slug(Unique Identifier) gets generated and then it is appended to string
# Lastly all the things gets inserted to the database and a Json response is generated
@app.post("/shorten", response_model=URLResponse)
async def create_short_url(request: Request, url_data: URLCreate, db: AsyncSession = Depends(get_db)):
    if await check_rate_limit(request.client.host):
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")

    slug = await get_unique_slug(url_data.original_url, db)
    short_url = f"http://short.ly/{slug}"


    print(slug)

    url_entry = URL(short_url=slug, original_url=url_data.original_url, expires_at=url_data.expires_at)
    db.add(url_entry)
    await db.commit()
    await db.refresh(url_entry)  # Refresh to load any auto-generated values

    return URLResponse(
        short_url=short_url,
        original_url=url_entry.original_url,
        created_at=url_entry.created_at,
        expires_at=url_entry.expires_at
    )

# this get api will get the slug and then basically redirect it to that page when the get method is called
@app.get("/new/{slug}")
async def redirect(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(URL).filter_by(short_url=slug))
    url_entry = result.scalars().first()

    if url_entry is None or (url_entry.expires_at and url_entry.expires_at < datetime.utcnow()):
        raise HTTPException(status_code=404, detail="URL not found or expired")

    # Use RedirectResponse to redirect to the original URL
    return RedirectResponse(url=url_entry.original_url)  # Redirecting to the original URL



# this is the function that returns the url only and will not redirect to that page
@app.get("/{slug}", response_model=URLResponse)
async def redirect(slug: str, db: AsyncSession = Depends(get_db)):
    url_entry = await db.get(URL, slug)
    if url_entry is None or (url_entry.expires_at and url_entry.expires_at < datetime.utcnow()):
        raise HTTPException(status_code=404, detail="URL not found or expired")

    return URLResponse(
        short_url=f"http://short.ly/{slug}",
        original_url=url_entry.original_url,
        created_at=url_entry.created_at,
        expires_at=url_entry.expires_at
    )
