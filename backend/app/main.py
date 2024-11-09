from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.forecast_summary import router as forecast_summary_router
from app.api.generate_alert import router as generate_alert_router
from app.api.municipality_router import router as municipality_router
from app.api.riskpoint_router import router as riskpoint_router
from app.api.poi_router import router as poi_router


app = FastAPI(title="CatGPT API", debug=True, version="1.0.0")

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(forecast_summary_router, tags=["forecast_summary"])
app.include_router(riskpoint_router, tags=["riskpoint"])
app.include_router(generate_alert_router, tags=["generate_alert"])
app.include_router(municipality_router, tags=["municipality"])
app.include_router(poi_router, tags=["poi"])

