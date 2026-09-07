"""Authentication endpoints with full JWT implementation."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import timedelta, datetime
import secrets

from auth.database import get_db, SessionLocal
from auth.models import User, UserSession
from auth.security import (
    verify_password, get_password_hash, create_access_token, verify_token,
    ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
)
from jose import jwt
from fastapi import HTTPException

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None
    preferred_language: str = "en"

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    preferred_language: str
    is_active: bool
    
    class Config:
        from_attributes = True

def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/register")
def register(user_data: dict, db: Session = Depends(get_db)):
    # Check if user exists
    if db.query(User).filter(User.email == user_data.get("email")).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    hashed_password = get_password_hash(user_data.get("password"))
    user = User(
        email=user_data.get("email"),
        hashed_password=hashed_password,
        full_name=user_data.get("full_name"),
        preferred_language=user_data.get("preferred_language", "en")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login")
def login(form_data: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.get("username")).first()
    if not user or not verify_password(form_data.get("password"), user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, 
        expires_delta=access_token_expires
    )
    
    # Create refresh token
    refresh_token = secrets.token_urlsafe(32)
    refresh_expires = datetime.utcnow() + timedelta(days=30)
    
    # Store refresh token hash
    refresh_token_hash = get_password_hash(refresh_token)
    session = UserSession(
        user_id=user.id,
        refresh_token_hash=get_password_hash(refresh_token),
        expires_at=datetime.utcnow() + timedelta(days=30)
    )
    db.add(session)
    db.commit()
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "preferred_language": user.preferred_language
        }
    }

@router.get("/me")
def get_current_user_info(current_user = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "preferred_language": current_user.preferred_language,
        "is_active": current_user.is_active
    }

@router.post("/refresh")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    # Find session by refresh token hash
    session = db.query(UserSession).filter(
        UserSession.refresh_token_hash == get_password_hash(refresh_token),
        UserSession.revoked == False,
        UserSession.expires_at > datetime.utcnow()
    ).first()
    
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    
    user = db.query(User).filter(User.id == session.user_id).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    
    # Create new access token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    # Rotate refresh token
    new_refresh_token = secrets.token_urlsafe(32)
    session.refresh_token_hash = get_password_hash(new_refresh_token)
    session.expires_at = datetime.utcnow() + timedelta(days=30)
    db.commit()
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": new_refresh_token
    }

# Add missing imports
from fastapi import Depends
from sqlalchemy.orm import Session
from auth.database import get_db
from auth.models import User, UserSession
from auth.security import (
    verify_password, get_password_hash, create_access_token, verify_token,
    ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
)
from jose import jwt
from fastapi import HTTPException
from datetime import datetime
import secrets
