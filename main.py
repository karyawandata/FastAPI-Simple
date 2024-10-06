import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Konfigurasi database
DATABASE_URL = "postgresql://postgres:Admin123@127.0.0.1:5432/pagila"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

# middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SalesByFilmCategory(BaseModel):
    category: str
    total_sales: float

@app.get("/sales-by-film-category", response_model=list[SalesByFilmCategory])
async def get_sales_by_film_category():
    try:
        with SessionLocal() as session:
            query = text("SELECT * FROM sales_by_film_category")
            result = session.execute(query)
            sales_data = [
                SalesByFilmCategory(category=row.category, total_sales=float(row.total_sales))
                for row in result
            ]
            return sales_data
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)