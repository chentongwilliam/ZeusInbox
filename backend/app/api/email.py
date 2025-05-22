from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models import email_account as models
from app.schemas import email_account as schemas

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