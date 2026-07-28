from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="NDSA Zero Trust SOC")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "NDSA Zero Trust SOC API is running"}
