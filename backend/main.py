from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI(
    title="NDSA Zero Trust SOC API",
    description="Zero Trust Security Operations Center Backend API with Keycloak Authentication",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://192.168.2.211:5173",
        "http://192.168.2.211:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "NDSA Zero Trust SOC API is running"}
