from fastapi import FastAPI

from app.api.emergency_router import router as emergency_router
from app.api.riskpoint_router import router as riskpoint_router

app = FastAPI(title="CatGPT API", debug=True, version="1.0.0")
app.include_router(emergency_router, tags=["emergency"])
app.include_router(riskpoint_router, tags=["riskpoint"])
