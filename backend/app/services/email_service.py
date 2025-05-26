import aioimaplib
import email
from email.header import decode_header
from typing import List, Dict, Any, Tuple
from app.utils.security import decrypt_data, encrypt_data
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self, account):
        self.account = account
        self.client = None

    def _get_imap_client(self, host: str, port: int):
        """根据端口自动选择SSL或非SSL IMAP客户端"""
        if port == 993:
            logger.info("使用SSL连接IMAP服务器 (IMAP4_SSL)")
            return aioimaplib.IMAP4_SSL(host=host, port=port)
        else:
            logger.info("使用明文连接IMAP服务器 (IMAP4)")
            return aioimaplib.IMAP4(host=host, port=port)

    async def test_connection(self) -> Tuple[bool, str]:
        """Test connection to IMAP server and return (success, message)"""
        try:
            logger.info(f"Attempting to connect to IMAP server: {self.account.imap_server}:{self.account.imap_port}")
            port = int(self.account.imap_port)
            self.client = self._get_imap_client(self.account.imap_server, port)
            logger.info("Waiting for server hello...")
            await self.client.wait_hello_from_server()
            logger.info(f"Attempting to login with username: {self.account.username}")
            await self.client.login(
                self.account.username,
                self.account.password
            )
            logger.info("Login successful")
            return True, "Login successful"
        except ConnectionRefusedError:
            error_msg = f"cannot connect to IMAP server {self.account.imap_server}:{self.account.imap_port}, please check the server address and port"
            logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"connection failed: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
        finally:
            if self.client:
                await self.disconnect()

    async def connect(self):
        """Connect to IMAP server"""
        try:
            port = int(self.account.imap_port)
            self.client = self._get_imap_client(self.account.imap_server, port)
            await self.client.wait_hello_from_server()
            await self.client.login(
                self.account.username,
                self.account.password
            )
        except Exception as e:
            logger.error(f"connection failed: {str(e)}")
            raise

    async def disconnect(self):
        """Disconnect from IMAP server"""
        if self.client:
            try:
                await self.client.logout()
            except Exception as e:
                logger.error(f"disconnect failed: {str(e)}")
            finally:
                self.client = None

    async def get_folders(self) -> List[str]:
        """Get list of email folders"""
        if not self.client:
            await self.connect()
        
        result, data = await self.client.list()
        if result != 'OK':
            raise Exception("Failed to get folders")
        
        folders = []
        for line in data:
            folder = line.decode().split('"')[-2]
            folders.append(folder)
        return folders

    def _decode_email_header(self, header: str) -> str:
        """Decode email header"""
        decoded_header = decode_header(header)
        header_parts = []
        for content, charset in decoded_header:
            if isinstance(content, bytes):
                if charset:
                    header_parts.append(content.decode(charset))
                else:
                    header_parts.append(content.decode('utf-8', errors='replace'))
            else:
                header_parts.append(content)
        return ''.join(header_parts)

    async def get_privateemail_emails(self, folder: str = "INBOX", limit: int = 10) -> List[Dict[str, Any]]:
        """专属privateemail邮箱的邮件获取方法"""
        emails = []
        await self.client.select(folder)
        result, data = await self.client.search("ALL")
        if result != 'OK':
            raise Exception("Failed to search emails")
        email_ids = data[0].split()
        for email_id in email_ids[-limit:]:
            email_id_str = email_id.decode()
            result, data = await self.client.fetch(email_id_str, "(RFC822)")
            if result == 'OK' and data:
                for item in data:
                    if isinstance(item, (bytes, bytearray)) and len(item) > 100:
                        msg = email.message_from_bytes(item)
                        subject = self._decode_email_header(msg.get("Subject", ""))
                        from_ = self._decode_email_header(msg.get("From", ""))
                        date = msg.get("Date", "")
                        emails.append({
                            'id': email_id_str,
                            'subject': subject,
                            'from': from_,
                            'date': date
                        })
        return emails

    async def get_emails(self, folder: str = "INBOX", limit: int = 10) -> List[Dict[str, Any]]:
        """Get emails from specified folder, 自动适配privateemail专属方法"""
        # 检查是否为privateemail
        if 'privateemail.com' in self.account.imap_server:
            logger.info("检测到privateemail邮箱，使用专属方法获取邮件")
            return await self.get_privateemail_emails(folder, limit)
        # 其他邮箱走通用逻辑
        if not self.client:
            await self.connect()
        await self.client.select(folder)
        result, data = await self.client.search('ALL')
        if result != 'OK':
            raise Exception("Failed to search emails")
        email_ids = data[0].split()
        emails = []
        for email_id in email_ids[-limit:]:
            result, data = await self.client.fetch(email_id, '(RFC822)')
            if result != 'OK':
                continue
            email_data = data[0][1]
            msg = email.message_from_bytes(email_data)
            subject = self._decode_email_header(msg.get('subject', ''))
            from_addr = self._decode_email_header(msg.get('from', ''))
            date = msg.get('date', '')
            emails.append({
                'id': email_id.decode(),
                'subject': subject,
                'from': from_addr,
                'date': date
            })
        return emails

    async def mark_as_read(self, email_id: str, folder: str = "INBOX"):
        """Mark email as read"""
        if not self.client:
            await self.connect()
        
        await self.client.select(folder)
        await self.client.store(email_id, '+FLAGS', '\\Seen')

    async def mark_as_unread(self, email_id: str, folder: str = "INBOX"):
        """Mark email as unread"""
        if not self.client:
            await self.connect()
        
        await self.client.select(folder)
        await self.client.store(email_id, '-FLAGS', '\\Seen') 
    
    def encrypt_email_data(self, data: dict) -> dict:
        """加密邮箱数据"""
        encrypted_data = data.copy()
        encrypted_data['password'] = encrypt_data(data['password'])
        return encrypted_data

    def decrypt_email_data(self, encrypted_password: str) -> str:
        """解密邮箱密码"""
        try:
            return decrypt_data(encrypted_password)
        except Exception as e:
            logger.error(f"Failed to decrypt password: {e}")
            return ""

    async def get_latest_email_list(self, folder: str = "INBOX", limit: int = 10) -> List[Dict[str, Any]]:
        """获取最新的邮件列表，只包含头部信息（主题、发件人、日期）
        
        Args:
            folder: 邮箱文件夹，默认为 INBOX
            limit: 获取的邮件数量，默认为10封
            
        Returns:
            List[Dict[str, Any]]: 邮件列表，每个邮件包含 id、subject、from、date 信息
        """
        if not self.client:
            await self.connect()
            
        try:
            # 选择邮箱文件夹
            await self.client.select(folder)
            
            # 搜索所有邮件
            result, data = await self.client.search('ALL')
            if result != 'OK':
                raise Exception("Failed to search emails")
                
            # 获取邮件ID列表
            email_ids = data[0].split()
            # 只取最新的limit封邮件，并反转顺序使最新的邮件在前
            recent_emails = email_ids[-limit:][::-1]
            
            emails = []
            for email_id in recent_emails:
                # 将bytes类型的email_id转换为字符串
                email_id_str = email_id.decode() if isinstance(email_id, bytes) else str(email_id)
                
                # 只获取邮件头部信息
                result, data = await self.client.fetch(email_id_str, '(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM DATE)])')
                if result == 'OK':
                    header_data = data[1]  # 获取头部数据
                    msg = email.message_from_bytes(header_data)
                    
                    # 解码并获取邮件信息
                    subject = self._decode_email_header(msg.get('Subject', ''))
                    from_addr = self._decode_email_header(msg.get('From', ''))
                    date = msg.get('Date', '')
                    
                    emails.append({
                        'id': email_id_str,
                        'subject': subject,
                        'from': from_addr,
                        'date': date
                    })
            
            return emails
            
        except Exception as e:
            logger.error(f"Failed to get latest email list: {str(e)}")
            raise 