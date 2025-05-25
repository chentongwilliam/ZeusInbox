from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models import email_account as models
from app.schemas import email_account as schemas
from pydantic import BaseModel
from app.services.email_service import EmailService
from app.models.email_account import EmailAccount
from app.utils.env_manager import update_email_settings

router = APIRouter()

@router.post("/accounts/", response_model=schemas.EmailAccount)
def create_email_account(
    account: schemas.EmailAccountCreate,
    db: Session = Depends(get_db)
):
    db_account = models.EmailAccount(**account.model_dump())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@router.get("/accounts/", response_model=List[schemas.EmailAccount])
def read_email_accounts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    accounts = db.query(models.EmailAccount).offset(skip).limit(limit).all()
    return accounts

@router.get("/accounts/{account_id}", response_model=schemas.EmailAccount)
def read_email_account(
    account_id: int,
    db: Session = Depends(get_db)
):
    db_account = db.query(models.EmailAccount).filter(models.EmailAccount.id == account_id).first()
    if db_account is None:
        raise HTTPException(status_code=404, detail="Email account not found")
    return db_account

@router.put("/accounts/{account_id}", response_model=schemas.EmailAccount)
def update_email_account(
    account_id: int,
    account: schemas.EmailAccountUpdate,
    db: Session = Depends(get_db)
):
    db_account = db.query(models.EmailAccount).filter(models.EmailAccount.id == account_id).first()
    if db_account is None:
        raise HTTPException(status_code=404, detail="Email account not found")
    
    update_data = account.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_account, field, value)
    
    db.commit()
    db.refresh(db_account)
    return db_account

@router.delete("/accounts/{account_id}")
def delete_email_account(
    account_id: int,
    db: Session = Depends(get_db)
):
    db_account = db.query(models.EmailAccount).filter(models.EmailAccount.id == account_id).first()
    if db_account is None:
        raise HTTPException(status_code=404, detail="Email account not found")
    
    db.delete(db_account)
    db.commit()
    return {"message": "Email account deleted successfully"}

class EmailSettings(BaseModel):
    email: str
    imap_server: str
    imap_port: int
    username: str
    password: str

@router.post("/test-connection")
async def test_email_connection(settings: EmailSettings, db: Session = Depends(get_db)):
    """Test email connection and return recent emails"""
    try:
        # Create a temporary email account object
        account = EmailAccount(
            email=settings.email,
            imap_server=settings.imap_server,
            imap_port=settings.imap_port,
            username=settings.username,
            password=settings.password
        )
        
        # Create email service instance
        email_service = EmailService(account)
        
        # Test connection
        success, message = await email_service.test_connection()
        if not success:
            raise HTTPException(status_code=400, detail=message)
        
        # 加密密码
        encrypted_data = email_service.encrypt_email_data(settings.dict())
        
        # 检查是否已存在相同邮箱的账户
        existing_account = db.query(EmailAccount).filter(EmailAccount.email == settings.email).first()
        
        if existing_account:
            # 更新现有账户
            for key, value in encrypted_data.items():
                setattr(existing_account, key, value)
        else:
            # 创建新账户
            new_account = EmailAccount(**encrypted_data)
            db.add(new_account)
        
        db.commit()
        
        return {
            "status": "success",
            "message": message,
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 