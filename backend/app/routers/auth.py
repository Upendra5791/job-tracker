from fastapi import APIRouter, Depends, HTTPException, Response, Cookie, status

from sqlmodel import Session, select
from fastapi import Depends, HTTPException
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin
from app.database import get_session
from app.services.auth_service import create_access_token, create_refresh_token, hash_password, verify_password

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, response: Response, session: Session = Depends(get_session)):
    if session.exec(select(User).where(User.email==data.email)).first():
        raise HTTPException(status_code=400, detail="Email already registered!")
    user = User(email=data.email, hashed_password=hash_password(data.password), full_name=data.full_name)
    session.add(user)
    session.commit()
    session.refresh(user)
    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))
    response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, samesite="lax", max_age=604800)
    return {"access_token": access_token, "token_type": "bearer", "user": user}

@router.post("/login")
def login(data: UserLogin, response: Response, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == data.email)).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))
    response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, samesite="lax", max_age=604800)
    return {"access_token": access_token, "token_type": "bearer", "user": user}