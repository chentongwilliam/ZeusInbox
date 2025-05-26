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
import email

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
    update_interval: int

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

@router.get("/settings")
async def get_email_settings(db: Session = Depends(get_db)):
    """Get the first active email account settings"""
    try:
        # 获取第一个邮箱账户
        account = db.query(EmailAccount).first()
        if not account:
            return None
            
        # 创建 EmailService 实例来解密密码
        email_service = EmailService(account)
        
        # 返回解密后的设置
        return {
            "email": account.email,
            "imap_server": account.imap_server,
            "imap_port": account.imap_port,
            "username": account.username,
            "password": email_service.decrypt_email_data(account.password)
        }
    except Exception as e:
        # 如果发生任何错误，返回 None
        print(f"Error getting email settings: {e}")
        return None

@router.post("/save-settings")
async def save_email_settings(settings: EmailSettings):
    """Save email settings and update .env file"""
    try:
        update_email_settings(
            email=settings.email,
            imap_server=settings.imap_server,
            imap_port=settings.imap_port,
            username=settings.username,
            password=settings.password,
            update_interval=settings.update_interval
        )
        return {"status": "success", "message": "Settings updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/emails/latest")
async def get_latest_emails(limit: int = 15, db: Session = Depends(get_db)):
    """
    获取最新邮件列表，包含摘要
    """
    account = db.query(EmailAccount).first()
    if not account:
        print("no account")
        raise HTTPException(status_code=404, detail="mail.connectionFailed")
    # 解密密码
    email_service_tmp = EmailService(account)
    decrypted_password = email_service_tmp.decrypt_email_data(account.password)
    # 构造解密后的 account 对象
    from app.models.email_account import EmailAccount as AccountModel
    account_data = {
        "email": account.email,
        "imap_server": account.imap_server,
        "imap_port": account.imap_port,
        "username": account.username,
        "password": decrypted_password
    }
    account_obj = AccountModel(**account_data)
    # print(f"account_obj: {account_obj.imap_server, account_obj.imap_port, account_obj.username, account_obj.password}")
    email_service = EmailService(account_obj)
    try:
        await email_service.connect()
        emails = await email_service.get_emails(limit=limit)
        # 增加摘要字段
        for mail in emails:
            try:
                result, data = await email_service.client.fetch(mail['id'], '(RFC822)')
                if result == 'OK':
                    msg = email.message_from_bytes(data[0][1])
                    snippet = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                snippet = part.get_payload(decode=True).decode(errors='ignore')[:300]
                                break
                    else:
                        snippet = msg.get_payload(decode=True).decode(errors='ignore')[:300]
                    mail['snippet'] = snippet
                else:
                    mail['snippet'] = ""
            except Exception:
                mail['snippet'] = ""
        return emails
    except Exception as e:
        raise HTTPException(status_code=500, detail="mail.connectionFailed")

@router.get("/emails/latest-list")
async def get_latest_email_list(limit: int = 20, db: Session = Depends(get_db)):
    """
    获取最新邮件列表，只包含头部信息（主题、发件人、日期）
    """
    account = db.query(EmailAccount).first()
    if not account:
        raise HTTPException(status_code=404, detail="mail.connectionFailed")
        
    # 解密密码
    email_service_tmp = EmailService(account)
    decrypted_password = email_service_tmp.decrypt_email_data(account.password)
    
    # 构造解密后的 account 对象
    from app.models.email_account import EmailAccount as AccountModel
    account_data = {
        "email": account.email,
        "imap_server": account.imap_server,
        "imap_port": account.imap_port,
        "username": account.username,
        "password": decrypted_password
    }
    account_obj = AccountModel(**account_data)
    
    email_service = EmailService(account_obj)
    try:
        await email_service.connect()
        emails = await email_service.get_latest_email_list(limit=limit)
        return emails
    except Exception as e:
        raise HTTPException(status_code=500, detail="mail.connectionFailed")
    finally:
        await email_service.disconnect() 