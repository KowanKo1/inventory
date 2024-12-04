from fastapi import FastAPI
from database import init_db
from routes import items, categories, transactions

app = FastAPI(title="Inventory Management API")

# Initialize database
init_db()

# Include routes
app.include_router(items.router, prefix="/items", tags=["Items"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Inventory Management API"}
