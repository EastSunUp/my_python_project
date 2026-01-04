# email_client.py - SMTP邮件客户端
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from datetime import datetime


class EmailClient:
    """邮件客户端"""

    def __init__(self, smtp_server, smtp_port, username, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.connection = None

    def connect(self):
        """连接到SMTP服务器"""
        try:
            # 创建SSL上下文
            context = ssl.create_default_context()

            # 连接到SMTP服务器
            if self.smtp_port == 465:
                # SSL连接
                self.connection = smtplib.SMTP_SSL(
                    self.smtp_server,
                    self.smtp_port,
                    context=context
                )
            else:
                # STARTTLS连接
                self.connection = smtplib.SMTP(self.smtp_server, self.smtp_port)
                self.connection.starttls(context=context)

            # 登录
            self.connection.login(self.username, self.password)
            print(f"✅ 成功连接到邮件服务器 {self.smtp_server}")
            return True

        except Exception as e:
            print(f"❌ 连接失败: {e}")
            return False

    def send_email(self, to_email, subject, body,
                   html_body=None, attachments=None, cc=None):
        """发送邮件"""
        if not self.connection:
            print("❌ 请先连接到邮件服务器")
            return False

        try:
            # 创建邮件
            msg = MIMEMultipart('alternative')
            msg['From'] = self.username
            msg['To'] = ', '.join(to_email) if isinstance(to_email, list) else to_email
            msg['Subject'] = subject
            msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')

            if cc:
                msg['Cc'] = ', '.join(cc) if isinstance(cc, list) else cc

            # 添加纯文本内容
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            # 添加HTML内容（如果有）
            if html_body:
                msg.attach(MIMEText(html_body, 'html', 'utf-8'))

            # 添加附件（如果有）
            if attachments:
                for attachment in attachments:
                    with open(attachment, 'rb') as f:
                        part = MIMEApplication(
                            f.read(),
                            Name=os.path.basename(attachment)
                        )
                        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
                        msg.attach(part)

            # 发送邮件
            recipients = to_email if isinstance(to_email, list) else [to_email]
            if cc:
                recipients += cc if isinstance(cc, list) else [cc]

            self.connection.sendmail(self.username, recipients, msg.as_string())
            print(f"✅ 邮件发送成功！收件人: {', '.join(recipients)}")
            return True

        except Exception as e:
            print(f"❌ 邮件发送失败: {e}")
            return False

    def send_batch_emails(self, email_list):
        """批量发送邮件"""
        success_count = 0
        fail_count = 0

        for email_data in email_list:
            to_email = email_data.get('to')
            subject = email_data.get('subject', '无主题')
            body = email_data.get('body', '')

            if self.send_email(to_email, subject, body):
                success_count += 1
            else:
                fail_count += 1

        print(f"📊 批量发送完成: 成功 {success_count} 封，失败 {fail_count} 封")
        return success_count, fail_count

    def disconnect(self):
        """断开连接"""
        if self.connection:
            self.connection.quit()
            print("👋 断开邮件服务器连接")


class EmailTemplate:
    """邮件模板"""

    @staticmethod
    def create_html_template(title, content, footer=None):
        """创建HTML邮件模板"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4CAF50; color: white; padding: 10px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .footer {{ margin-top: 20px; padding: 10px; text-align: center; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{title}</h1>
                </div>
                <div class="content">
                    {content}
                </div>
                {f'<div class="footer">{footer}</div>' if footer else ''}
            </div>
        </body>
        </html>
        """
        return html


# 使用示例
if __name__ == "__main__":
    # 配置SMTP服务器信息(以QQ邮箱为例)  # 需要配置您的SMTP信息:
    SMTP_SERVER = "smtp.qq.com"
    SMTP_PORT = 587  # 或 465
    USERNAME = "your_email@qq.com"
    PASSWORD = "your_authorization_code"  # 授权码，不是登录密码

    # 创建邮件客户端
    email_client = EmailClient(SMTP_SERVER, SMTP_PORT, USERNAME, PASSWORD)

    # 连接到邮件服务器
    if email_client.connect():
        # 创建HTML内容
        html_content = EmailTemplate.create_html_template(
            title="测试邮件",
            content="<p>这是一封测试邮件，包含HTML格式。</p>"
                    "<p><strong>重要通知：</strong>请查收附件。</p>"
                    "<a href='https://example.com'>点击这里访问网站</a>",
            footer="本邮件为自动发送，请勿回复。"
        )

        # 发送邮件
        email_client.send_email(
            to_email=["recipient1@example.com", "recipient2@example.com"],
            subject="测试邮件主题",
            body="这是纯文本内容",
            html_body=html_content,
            cc=["cc@example.com"]
            # attachments=["file1.pdf", "file2.jpg"]  # 可以添加附件
        )

        # 批量发送示例
        # batch_emails = [
        #     {'to': 'user1@example.com', 'subject': '邮件1', 'body': '内容1'},
        #     {'to': 'user2@example.com', 'subject': '邮件2', 'body': '内容2'}
        # ]
        # email_client.send_batch_emails(batch_emails)

        email_client.disconnect()
