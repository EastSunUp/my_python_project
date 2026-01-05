# email_manager.py - IMAP邮件管理器
import imaplib
import email
from email.header import decode_header
import os
import json
from datetime import datetime, timedelta


class EmailManager:
    """邮件管理器（IMAP）"""

    def __init__(self, imap_server, username, password):
        self.imap_server = imap_server
        self.username = username
        self.password = password
        self.imap = None
        self.connected = False

    def connect(self):
        """连接到IMAP服务器"""
        try:
            # 连接到IMAP服务器
            self.imap = imaplib.IMAP4_SSL(self.imap_server)

            # 登录
            self.imap.login(self.username, self.password)
            self.connected = True

            print(f"✅ 成功连接到邮件服务器 {self.imap_server}")
            return True

        except Exception as e:
            print(f"❌ 连接失败: {e}")
            return False

    def list_folders(self):
        """列出所有邮箱文件夹"""
        if not self.connected:
            print("❌ 请先连接到邮件服务器")
            return []

        try:
            # 列出所有文件夹
            status, folders = self.imap.list()
            if status == 'OK':
                folder_list = []
                for folder in folders:
                    # 解码文件夹名称
                    folder_name = folder.decode().split(' "/" ')[-1]
                    folder_list.append(folder_name)

                return folder_list
            return []

        except Exception as e:
            print(f"❌ 获取文件夹列表失败: {e}")
            return []

    def select_folder(self, folder='INBOX'):
        """选择邮箱文件夹"""
        if not self.connected:
            print("❌ 请先连接到邮件服务器")
            return False

        try:
            status, messages = self.imap.select(folder)
            if status == 'OK':
                print(f"✅ 已选择文件夹: {folder}")
                return True
            return False

        except Exception as e:
            print(f"❌ 选择文件夹失败: {e}")
            return False

    def search_emails(self, criteria='ALL'):
        """搜索邮件"""
        if not self.connected:
            print("❌ 请先连接到邮件服务器")
            return []

        try:
            # 搜索邮件
            status, message_ids = self.imap.search(None, criteria)
            if status == 'OK':
                # 返回邮件ID列表
                return message_ids[0].split()
            return []

        except Exception as e:
            print(f"❌ 搜索邮件失败: {e}")
            return []

    def fetch_email(self, message_id, download_attachments=False):
        """获取邮件内容"""
        try:
            # 获取邮件
            status, msg_data = self.imap.fetch(message_id, '(RFC822)')
            if status != 'OK':
                return None

            # 解析邮件
            raw_email = msg_data[0][1]
            email_message = email.message_from_bytes(raw_email)

            # 解码邮件头信息
            subject = self._decode_header(email_message['Subject'])
            from_addr = self._decode_header(email_message['From'])
            to_addr = self._decode_header(email_message['To'])
            date = email_message['Date']

            # 提取邮件内容
            email_info = {
                'id': message_id.decode(),
                'subject': subject,
                'from': from_addr,
                'to': to_addr,
                'date': date,
                'body': '',
                'attachments': []
            }

            # 解析邮件正文和附件
            if email_message.is_multipart():
                for part in email_message.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    # 获取文本内容
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        email_info['body'] = part.get_payload(decode=True).decode()

                    # 处理附件
                    elif "attachment" in content_disposition and download_attachments:
                        filename = part.get_filename()
                        if filename:
                            filename = self._decode_header(filename)

                            # 保存附件
                            attachment_data = part.get_payload(decode=True)
                            email_info['attachments'].append({
                                'filename': filename,
                                'size': len(attachment_data)
                            })
            else:
                # 非多部分邮件
                email_info['body'] = email_message.get_payload(decode=True).decode()

            return email_info

        except Exception as e:
            print(f"❌ 获取邮件失败: {e}")
            return None

    def fetch_recent_emails(self, days=7, limit=10):
        """获取最近几天的邮件"""
        # 计算日期
        date_since = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")

        # 搜索最近邮件
        criteria = f'(SINCE "{date_since}")'
        message_ids = self.search_emails(criteria)

        emails = []
        # 获取最近的limit封邮件
        for msg_id in message_ids[-limit:]:
            email_info = self.fetch_email(msg_id)
            if email_info:
                emails.append(email_info)

        return emails

    def _decode_header(self, header):
        """解码邮件头"""
        if header is None:
            return ""

        decoded_parts = decode_header(header)
        decoded_header = ""
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                if encoding:
                    decoded_header += part.decode(encoding)
                else:
                    decoded_header += part.decode()
            else:
                decoded_header += part

        return decoded_header

    def save_emails_to_json(self, emails, filename='emails.json'):
        """保存邮件到JSON文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(emails, f, ensure_ascii=False, indent=2)
            print(f"✅ 邮件已保存到 {filename}")
            return True
        except Exception as e:
            print(f"❌ 保存邮件失败: {e}")
            return False

    def disconnect(self):
        """断开连接"""
        if self.imap:
            self.imap.logout()
            self.connected = False
            print("👋 断开邮件服务器连接")


# 使用示例
if __name__ == "__main__":
    # 配置IMAP服务器信息（以QQ邮箱为例）
    IMAP_SERVER = "imap.qq.com"
    USERNAME = "your_email@qq.com"
    PASSWORD = "your_authorization_code"

    # 创建邮件管理器
    email_manager = EmailManager(IMAP_SERVER, USERNAME, PASSWORD)

    # 连接到邮件服务器
    if email_manager.connect():
        # 列出所有文件夹
        folders = email_manager.list_folders()
        print("📁 邮箱文件夹:")
        for folder in folders:
            print(f"  - {folder}")

        # 选择收件箱
        if email_manager.select_folder('INBOX'):
            # 获取最近7天的邮件
            recent_emails = email_manager.fetch_recent_emails(days=7, limit=5)

            print(f"\n📧 最近 {len(recent_emails)} 封邮件:")
            for i, email_info in enumerate(recent_emails, 1):
                print(f"\n{i}. 主题: {email_info['subject']}")
                print(f"   发件人: {email_info['from']}")
                print(f"   时间: {email_info['date']}")
                print(f"   正文预览: {email_info['body'][:100]}...")

            # 保存邮件到文件
            email_manager.save_emails_to_json(recent_emails)

        email_manager.disconnect()

