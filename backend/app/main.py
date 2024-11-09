from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.emergency_router import router as emergency_router
from app.api.riskpoint_router import router as riskpoint_router
from app.api.municipality_router import router as municipality_router

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
app.include_router(emergency_router, tags=["emergency"])
app.include_router(riskpoint_router, tags=["riskpoint"])
app.include_router(municipality_router, tags=["municipality"])
