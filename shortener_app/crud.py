from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import keygen, models, schemas


async def create_db_url(db: AsyncSession, url: schemas.URLBase) -> models.URL:
    key = (
        url.custom_key
        if url.custom_key
        else await keygen.create_unique_random_key(db)
    )
    secret_key = f'{key}_{keygen.create_random_key(8)}'
    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )
    db.add(db_url)
    await db.commit()

    return db_url


async def get_db_url_by_key(db: AsyncSession, url_key: str) -> models.URL:
    stmt = select(models.URL).filter(
        models.URL.key == url_key, models.URL.is_active
    )
    db_url = await db.scalar(stmt)

    return db_url


async def get_db_url_by_secret_key(
    db: AsyncSession, secret_key: str
) -> models.URL:
    stmt = select(models.URL).filter(
        models.URL.secret_key == secret_key, models.URL.is_active
    )
    db_url = await db.scalar(stmt)

    return db_url


async def update_db_clicks(
    db: AsyncSession, db_url: schemas.URL
) -> models.URL:
    db_url.clicks += 1
    await db.commit()

    return db_url


async def deactivate_db_url_by_secret_key(
    db: AsyncSession, secret_key: str
) -> models.URL:
    if db_url := await get_db_url_by_secret_key(db, secret_key):
        db_url.is_active = False
        await db.commit()

    return db_url
