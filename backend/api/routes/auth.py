"""Authentication endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import timedelta

from auth.database import get_db
from auth.models import User, UserSession
from auth.security import (
    verify_password, get_password_hash, create_access_token, verify_token
)
from auth.database import SessionLocal

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

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str

def get_current_user(token: str = Depends(lambda: None), db: Session = Depends(lambda: None)):
    # Simplified for now
    return None

@router.post("/register")
def register(user_data: dict, db: Session = Depends(lambda: None)):
    return {"message": "User registered successfully"}

@router.post("/login")
def login(form_data: dict):
    return {"access_token": "token", "token_type": "bearer"}

@router.get("/me")
def get_current_user_info():
    return {"message": "Current user info"}

@router.post("/refresh")
def refresh_token(refresh_token: str):
    return {"access_token": "new_token", "token_type": "bearer"}
