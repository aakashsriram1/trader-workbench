from fastapi import FastAPI
from routers import health

app = FastAPI(title="Trader's Workbench")

app.include_router(health.router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Trader's Workbench API running"}
