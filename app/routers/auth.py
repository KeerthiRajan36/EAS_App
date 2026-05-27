from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.auth import RegisterSchema, LoginSchema
from app.services.auth_service import login_user, register_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(request: RegisterSchema, db: Session = Depends(get_db)):
    user = register_user(request, db)
    if not user:

        raise HTTPException(status_code=400, detail="Email already exists")

    return {"message": "User registered"}


@router.post("/login")
def login(request: LoginSchema, db: Session = Depends(get_db)):

    response = login_user(request, db)

    if not response:

        raise HTTPException(status_code=401, detail="Invalid credentials")

    return response
