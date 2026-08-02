from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="NDSA Zero Trust SOC API",
    description="Zero Trust Security Operations Center Backend API with Keycloak Authentication",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "NDSA Zero Trust SOC API is running"}
