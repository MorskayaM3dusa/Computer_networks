import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

from parser import parse_site


app = FastAPI(title="parse_site")

DB = 'postgresql://postgres:postgres@localhost:5433/shoes_catalog'

engine = create_engine(DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Product(Base):

    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(String)
    old_price = Column(String)
    credit_info = Column(String)

Base.metadata.create_all(bind=engine)

def savetodb(data):
    with SessionLocal() as session:
        try:
            for item in data:
                existing = session.query(Product).filter_by(
                    title=item['title'],
                    price=item['price']
                ).first()
                
                if not existing:
                    product = Product(
                        title=item['title'],
                        price=item['price'],
                        old_price=item['old_price'],
                        credit_info=item['credit_info']
                    )
                    session.add(product)   
            session.commit()
            return 'SUCCESS'
        except Exception as e:
            print(f"Error saving to database: {e}")
            session.rollback()
            return 'ERROR'

    
@app.get('/parse')
async def parse(request: Request):
    url = request.query_params.get('url', r'https://www.podkablukom.ru/catalog1c/men-botinki/')
    data = parse_site(url)
    if not data:
        return JSONResponse(
            content={'status': 'error', 'source': 'parser'},
        )
    
    save_result = savetodb(data['items'])
    return JSONResponse(
        content={'status': f'{save_result}', 'source': 'savetodb'},
    )


@app.get('/get_data')
async def get_data():
    with SessionLocal() as session:
        try:
            products = session.query(Product).all()

            result = []
            for product in products:
                result.append(
                    {
                        'id': product.id,
                        'title': product.title,
                        'price': product.price,
                        'old_price': product.old_price,
                        'credit_info': product.credit_info
                    }
                )
            return result
        except:
            return JSONResponse(
                content={'status': 'error', 'source': 'get_data'},
            )

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)