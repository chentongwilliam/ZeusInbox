import asyncio
import aioimaplib
import email
from email.header import decode_header

IMAP_SERVER = 'mail.privateemail.com'
IMAP_PORT = 993  # 993为SSL端口，143为明文端口， only use 993
EMAIL = ''
PASSWORD = ''

def decode_str(s):
    """解码邮件头部字段"""
    decoded = decode_header(s)
    return ''.join([
        part.decode(charset or 'utf-8') if isinstance(part, bytes) else part
        for part, charset in decoded
    ])

async def main():
    # 根据端口选择SSL或非SSL方式
    if IMAP_PORT == 993:
        print("使用SSL方式连接IMAP服务器...")
        client = aioimaplib.IMAP4_SSL(host=IMAP_SERVER, port=IMAP_PORT)
    else:
        print("使用明文方式连接IMAP服务器...")
        client = aioimaplib.IMAP4(host=IMAP_SERVER, port=IMAP_PORT)
        await client.wait_hello_from_server()
        
    
    print("等待服务器响应...")
    await client.wait_hello_from_server()

    print("尝试登录...")
    await client.login(EMAIL, PASSWORD)
    print("登录成功！")

    # 选择INBOX
    await client.select("INBOX")
    # 搜索所有邮件
    result, data = await client.search("ALL")
    email_ids = data[0].split()
    print(f"共找到{len(email_ids)}封邮件，显示最近10封：")

    # 获取最近10封邮件
    for email_id in email_ids[-10:]:
        email_id_str = email_id.decode()
        result, data = await client.fetch(email_id_str, "(RFC822)")
        # print(f"fetch result: {result}, data: {data}")
        if result == 'OK' and data:
            for item in data:
                # 只处理字节类型且长度较大的项（通常是邮件内容）
                if isinstance(item, (bytes, bytearray)) and len(item) > 100:
                    msg = email.message_from_bytes(item)
                    subject = decode_str(msg.get("Subject", ""))
                    from_ = decode_str(msg.get("From", ""))
                    print(f"邮件ID: {email_id_str} | 标题: {subject} | 发件人: {from_}")

    await client.logout()
    print("已断开连接。")

if __name__ == '__main__':
    asyncio.run(main())