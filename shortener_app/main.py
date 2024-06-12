from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import validators
from fastapi import Depends, FastAPI, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import URL

from . import crud, models, schemas, utils
from .config import get_settings
from .database import get_db, init_models


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, None]:
    await init_models()
    yield


app = FastAPI(
    title='URL Shortener',
    summary='Summary example',
    description='Description example',
    version='1',
    lifespan=lifespan,
)


def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for(
        'administration info', secret_key=db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))

    return db_url


@app.get('/')
async def read_root():
    return {'detail': 'Welcome to the URL shortener API :)'}


@app.post('/url', response_model=schemas.URLInfo)
async def create_url(url: schemas.URLBase, db: AsyncSession = Depends(get_db)):
    if not validators.url(url.target_url):
        utils.raise_bad_request(message='Your provided URL is not valid')

    db_url = await crud.create_db_url(db, url)
    return get_admin_info(db_url)


@app.get('/{url_key}')
async def forward_to_target_url(
    url_key: str, request: Request, db: AsyncSession = Depends(get_db)
):
    if db_url := await crud.get_db_url_by_key(db, url_key):
        await crud.update_db_clicks(db, db_url)
        return RedirectResponse(db_url.target_url)

    utils.raise_not_found(request)


@app.get(
    '/admin/{secret_key}',
    name='administration info',
    response_model=schemas.URLInfo,
)
async def get_url_info(
    secret_key: str, request: Request, db: AsyncSession = Depends(get_db)
):
    if db_url := await crud.get_db_url_by_secret_key(db, secret_key):
        return get_admin_info(db_url)

    utils.raise_not_found(request)


@app.delete('/admin/{secret_key}')
async def delete_url(
    secret_key: str, request: Request, db: AsyncSession = Depends(get_db)
):
    if db_url := await crud.deactivate_db_url_by_secret_key(db, secret_key):
        message = 'Successfully deleted shortened URL for {}'
        return {'detail': message.format(db_url.target_url)}

    utils.raise_not_found(request)
