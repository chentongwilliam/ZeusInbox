from passlib.context import CryptContext
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
import base64

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_or_create_encryption_key():
    """获取或创建加密密钥，优先从环境变量获取，其次从.env文件获取，最后生成新密钥"""
    # 1. 首先尝试从环境变量获取
    key = os.getenv("ENCRYPTION_KEY")
    if key:
        return key

    # 2. 加载.env文件
    load_dotenv()
    key = os.getenv("ENCRYPTION_KEY")
    if key:
        return key

    # 3. 生成新密钥
    key = Fernet.generate_key()
    # 将密钥转换为字符串
    key_str = base64.urlsafe_b64encode(key).decode()
    
    # 4. 保存到.env文件
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
    with open(env_path, 'a') as f:
        f.write(f'\nENCRYPTION_KEY={key_str}')
    
    return key_str

# 获取或创建加密密钥
ENCRYPTION_KEY = get_or_create_encryption_key()
# 确保密钥是字节类型
if isinstance(ENCRYPTION_KEY, str):
    ENCRYPTION_KEY = base64.urlsafe_b64decode(ENCRYPTION_KEY)
fernet = Fernet(ENCRYPTION_KEY)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def encrypt_data(data: str) -> str:
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    return fernet.decrypt(encrypted_data.encode()).decode() 