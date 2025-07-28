from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserLogin
from app.models.user import User
from app.db.deps import get_db
from app.core.security import hash_password, verify_password

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # 1. Verificăm dacă userul există deja
    existing_user = db.query(User).filter(
        User.username == user_data.username
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Acest username este deja înregistrat."
        )

    # 2. Criptăm parola
    hashed_pw = hash_password(user_data.password)

    # 3. Creăm userul
    new_user = User(
        username=user_data.username,
        password_hash=hashed_pw
    )

    # 4. Salvăm în DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Utilizator înregistrat cu succes.",
        "user_id": new_user.id
    }


@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username sau parolă incorectă."
        )

    return {
        "message": "Autentificare reușită.",
        "user_id": user.id
    }
