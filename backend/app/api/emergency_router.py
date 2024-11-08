from fastapi import APIRouter

router = APIRouter()


@router.get("/emergency")
def root():
    return f"Hola Mundo"
