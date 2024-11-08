from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.emergency_router import router as emergency_router

app = FastAPI(title="CatGPT API", debug=True, version="1.0.0")
app.include_router(emergency_router, tags=["emergency"])

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
