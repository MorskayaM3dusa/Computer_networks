from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(String)
    old_price = Column(String)
    credit_info = Column(String)


def init_db(db_url: str):
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return engine, SessionLocal


def save_to_db(session_local, data):
    with session_local() as session:
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


def get_all_products(session_local):
    with session_local() as session:
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
        except Exception as e:
            raise Exception(f"Error getting data from database: {e}")