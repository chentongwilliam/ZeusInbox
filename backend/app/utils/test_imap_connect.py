import imaplib
import email
import time
from email.header import decode_header
from datetime import datetime
import email.parser
import email.policy

# 配置信息（请根据你的实际邮箱信息填写）
IMAP_SERVER = 'mail.privateemail.com'  # 你的IMAP服务器
IMAP_PORT = 993                        # 993为SSL端口，143为明文端口
EMAIL = ''
PASSWORD = ''

def decode_str(s):
    """解码邮件头部字段"""
    decoded = decode_header(s)
    return ''.join([
        part.decode(charset or 'utf-8') if isinstance(part, bytes) else part
        for part, charset in decoded
    ])

def get_email_list(mail, email_ids):
    """快速获取邮件列表（只包含基本信息）"""
    email_list = []
    for email_id in email_ids:
        # 只获取邮件头部信息
        status, data = mail.fetch(email_id, '(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM DATE)])')
        if status == 'OK':
            header_data = data[0][1]
            msg = email.message_from_bytes(header_data)
            
            email_info = {
                'id': email_id.decode(),
                'subject': decode_str(msg.get('Subject', '')),
                'from': decode_str(msg.get('From', '')),
                'date': msg.get('Date', '')
            }
            email_list.append(email_info)
    return email_list

def get_email_content(mail, email_id):
    """获取完整邮件内容"""
    status, data = mail.fetch(email_id, '(RFC822)')
    if status == 'OK':
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        return msg, len(raw_email)
    return None, 0

def get_email_content_types(msg):
    """获取邮件内容类型"""
    content_types = set()
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            content_type = part.get_content_type()
            content_types.add(content_type)
    else:
        content_types.add(msg.get_content_type())
    return content_types

def format_size(size):
    """格式化文件大小显示"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f}{unit}"
        size /= 1024
    return f"{size:.2f}GB"

def main():
    start_time = time.time()
    print(f"开始执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 根据端口选择SSL或非SSL方式
        if IMAP_PORT == 993:
            print("使用SSL方式连接IMAP服务器...")
            connect_start = time.time()
            mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
            print(f"服务器连接耗时: {time.time() - connect_start:.2f}秒")
        else:
            print("使用明文方式连接IMAP服务器...")
            connect_start = time.time()
            mail = imaplib.IMAP4(IMAP_SERVER, IMAP_PORT)
            print("尝试升级为加密连接（STARTTLS）...")
            mail.starttls()  # 关键步骤
            print(f"服务器连接耗时: {time.time() - connect_start:.2f}秒")

        print("连接服务器成功！")

        # 登录
        login_start = time.time()
        mail.login(EMAIL, PASSWORD)
        print(f"登录耗时: {time.time() - login_start:.2f}秒")
        print("登录成功！")

        # 选择INBOX
        select_start = time.time()
        mail.select('INBOX')
        print(f"选择邮箱耗时: {time.time() - select_start:.2f}秒")

        # 搜索所有邮件
        search_start = time.time()
        status, messages = mail.search(None, 'ALL')
        email_ids = messages[0].split()
        print(f"搜索邮件耗时: {time.time() - search_start:.2f}秒")
        print(f"共找到{len(email_ids)}封邮件，显示最近10封：")

        # 1. 快速获取邮件列表
        list_start = time.time()
        email_list = get_email_list(mail, email_ids[-10:])
        print(f"\n获取邮件列表耗时: {time.time() - list_start:.2f}秒")
        print("\n邮件列表:")
        for email_info in email_list:
            print(f"\n邮件ID: {email_info['id']}")
            print(f"标题: {email_info['subject']}")
            print(f"发件人: {email_info['from']}")
            print(f"时间: {email_info['date']}")

        # 2. 按需获取邮件内容
        print("\n开始获取邮件内容...")
        content_start = time.time()
        total_size = 0
        for email_info in email_list:
            email_start = time.time()
            msg, size = get_email_content(mail, email_info['id'].encode())
            if msg:
                content_types = get_email_content_types(msg)
                total_size += size
                
                email_time = time.time() - email_start
                print(f"\n邮件ID: {email_info['id']}")
                print(f"标题: {email_info['subject']}")
                print(f"发件人: {email_info['from']}")
                print(f"时间: {email_info['date']}")
                print(f"大小: {format_size(size)}")
                print(f"内容类型: {', '.join(content_types)}")
                print(f"处理耗时: {email_time:.2f}秒")

        print(f"\n获取邮件内容总耗时: {time.time() - content_start:.2f}秒")
        print(f"10封邮件总大小: {format_size(total_size)}")
        print(f"平均每封邮件大小: {format_size(total_size/10)}")

        # 退出
        logout_start = time.time()
        mail.logout()
        print(f"登出耗时: {time.time() - logout_start:.2f}秒")
        print("已断开连接。")

    except Exception as e:
        print(f"发生错误: {str(e)}")
        print(f"错误类型: {type(e).__name__}")
    finally:
        total_time = time.time() - start_time
        print(f"\n总耗时: {total_time:.2f}秒")
        print(f"结束执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()