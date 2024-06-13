from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models
from .constants import ERROR_MESSAGES


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


def raise_not_found(request):
    url = str(request.url)
    if 'peek' in url:
        url = ''.join(url.split('peek/'))

    raise HTTPException(
        status_code=404,
        detail=ERROR_MESSAGES['url_does_not_exist'].format(url),
    )


async def check_key_already_exist(db: AsyncSession, custom_key: str) -> bool:
    stat = select(models.URL).filter(models.URL.key == custom_key).exists()
    return await db.execute(stat).scalar()
