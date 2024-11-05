import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 邮件服务器地址和端口号
smtp_server = 'smtp.163.com'
smtp_port = 25

# 发件人邮箱地址和密码
sender_email = '18381002338@163.com'  # 这里替换为您自己的发件人邮箱地址
sender_password = 'DEmuvwKH4Ebdc4Ch'  # 这里是你的授权码？ 非邮箱登录密码

# 收件人邮箱地址
recipient_email = '2488708698@qq.com'

# 创建一封邮件，文本内容为 "Hello, World!"
message = MIMEText('This is test! Hello, World!', 'plain', 'utf-8')
message['From'] = Header('BS <{}>'.format(sender_email), 'utf-8')  # 设置发件人昵称
message['To'] = Header('ZJU <{}>'.format(recipient_email), 'utf-8')  # 设置收件人昵称
message['Subject'] = Header('邮件主题', 'utf-8')  # 设置邮件主题

try:
    # 连接邮件服务器并登录
    smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
    smtp_connection.login(sender_email, sender_password)

    # 发送邮件
    smtp_connection.sendmail(sender_email, recipient_email, message.as_string())

    # 关闭连接
    smtp_connection.quit()

    print("邮件发送成功！")

except Exception as e:
    print("邮件发送失败：", e)
