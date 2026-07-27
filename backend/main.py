from fastapi import FastAPI
app = FastAPI(title="NDSA Zero Trust SOC")
@app.get("/")
def root():
    return {"message": "NDSA Zero Trust SOC API is running"}
