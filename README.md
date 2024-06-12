# Shortener App 🚀

Simple async URL shortener app written with FastAPI featuring CRUD operations.

You can create a short link for your target URL, view full information using your secret key, and delete it.

## Get Started

Make sure to create a virtual environment and activate it before running the app.

```bash
git clone git@github.com:ezemlyanskiy/fastapi_async_url_shortener.git
python -m pip install -U pip
python -m pip install -r requirements.txt
uvicorn shortener_url.main:app
```

## Usage

Navigate to http://127.0.0.1:8000/docs to interact with the API. Have fun!
