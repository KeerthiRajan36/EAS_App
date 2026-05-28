from fastapi import FastAPI
import uvicorn
from app.database import Base, engine

from app.routers import auth, assests, allocations, maintenance

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Enterprise Asset Management")

app.include_router(auth.router)
app.include_router(assests.router)
app.include_router(allocations.router)
app.include_router(maintenance.router)


@app.get("/")
def home():
    return {"message": "EAM API Running"}


if __name__ == "__main__":

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )