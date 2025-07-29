# app/api/auth.py
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserLogin
from app.models.user import User
from app.db.deps import get_db
from app.core.security import hash_password, verify_password

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Acest username este deja înregistrat."
        )

    new_user = User(
        username=user_data.username,
        password_hash=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Cont creat cu succes!"}


@router.post("/login")
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credențiale invalide.")

    access_token = Authorize.create_access_token(subject=str(user.id))
    return {"access_token": access_token, "username": user.username}
