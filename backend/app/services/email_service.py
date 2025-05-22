import aioimaplib
from typing import List, Dict, Any
from app.utils.security import decrypt_data

class EmailService:
    def __init__(self, account):
        self.account = account
        self.client = None

    async def connect(self):
        """Connect to IMAP server"""
        self.client = aioimaplib.IMAP4_SSL(
            host=self.account.imap_server,
            port=self.account.imap_port
        )
        await self.client.wait_hello_from_server()
        await self.client.login(
            self.account.username,
            decrypt_data(self.account.password)
        )

    async def disconnect(self):
        """Disconnect from IMAP server"""
        if self.client:
            await self.client.logout()
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

    async def get_emails(self, folder: str = "INBOX", limit: int = 50) -> List[Dict[str, Any]]:
        """Get emails from specified folder"""
        if not self.client:
            await self.connect()
        
        await self.client.select(folder)
        result, data = await self.client.search('ALL')
        if result != 'OK':
            raise Exception("Failed to search emails")
        
        email_ids = data[0].split()
        emails = []
        
        # Get the most recent emails
        for email_id in email_ids[-limit:]:
            result, data = await self.client.fetch(email_id, '(RFC822)')
            if result != 'OK':
                continue
            
            # Parse email data
            email_data = data[0][1]
            # TODO: Parse email data into structured format
            emails.append({
                'id': email_id.decode(),
                'raw_data': email_data.decode()
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