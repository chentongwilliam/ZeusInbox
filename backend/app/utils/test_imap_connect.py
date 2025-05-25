import imaplib

# 配置信息（请根据你的实际邮箱信息填写）
IMAP_SERVER = 'mail.privateemail.com'  # 你的IMAP服务器
IMAP_PORT = 143                        # 993为SSL端口，143为明文端口
EMAIL = ''
PASSWORD = ''  # 填写你的邮箱密码

try:
    # 根据端口选择SSL或非SSL方式
    if IMAP_PORT == 993:
        print("使用SSL方式连接IMAP服务器...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    else:
        print("使用明文方式连接IMAP服务器...")
        mail = imaplib.IMAP4(IMAP_SERVER, IMAP_PORT)
        print("尝试升级为加密连接（STARTTLS）...")
        mail.starttls()  # 关键步骤

    print("连接服务器成功！")

    # 登录
    mail.login(EMAIL, PASSWORD)
    print("登录成功！")

    # 获取邮箱列表
    status, mailboxes = mail.list()
    print("邮箱文件夹列表：", mailboxes)

    # 退出
    mail.logout()
    print("已断开连接。")

except Exception as e:
    print("连接或登录失败：", str(e))