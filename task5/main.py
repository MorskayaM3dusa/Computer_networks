import uvicorn
import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from parser import parse_site
from db import init_db, save_to_db, get_all_products


DB_URL = 'postgresql://postgres:postgres@app-db:5432/shoes_catalog'
engine, SessionLocal = init_db(DB_URL)
app = FastAPI(title="parse_site")


@app.get('/parse')
def parse(request: Request):
    url = request.query_params.get('url', r'https://www.podkablukom.ru/catalog1c/men-botinki/')
    data = parse_site(url)
    if not data:
        return JSONResponse(
            content={'status': 'error', 'source': 'parser'},
        )
    save_result = save_to_db(SessionLocal, data['items'])
    return JSONResponse(
        content={'status': f'{save_result}', 'source': 'save_to_db'},
    )


@app.get('/get_data')
def get_data():
    try:
        products = get_all_products(SessionLocal)
        return products
    except Exception as e:
        return JSONResponse(
            content={'status': 'error', 'source': 'get_data', 'detail': str(e)},
        )

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)