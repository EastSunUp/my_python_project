# tcp_server.py - 基础TCP服务器
import socket
import threading
import json
from datetime import datetime


class TCPServer:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = {}

    def start(self):
        """启动TCP服务器"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        print(f"✅ TCP服务器启动在 {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"📡 客户端连接: {client_address}")

            # 为每个客户端创建新线程
            client_thread = threading.Thread(
                target=self.handle_client,
                args=(client_socket, client_address)
            )
            client_thread.daemon = True
            client_thread.start()

    def handle_client(self, client_socket, client_address):
        """处理客户端连接"""
        client_id = f"{client_address[0]}:{client_address[1]}"
        self.clients[client_id] = {
            'socket': client_socket,
            'address': client_address,
            'connected_time': datetime.now()
        }

        try:
            while True:
                # 接收数据
                data = client_socket.recv(1024)
                if not data:
                    break

                # 解码并处理数据
                message = data.decode('utf-8')
                print(f"📨 来自 {client_id}: {message}")

                # 发送响应
                response = self.process_message(message)
                client_socket.send(response.encode('utf-8'))

        except ConnectionResetError:
            print(f"❌ 客户端 {client_id} 异常断开")
        finally:
            client_socket.close()
            del self.clients[client_id]
            print(f"👋 客户端 {client_id} 断开连接")

    def process_message(self, message):
        """处理客户端消息"""
        try:
            # 尝试解析JSON命令
            cmd = json.loads(message)
            command = cmd.get('command', '')

            if command == 'time':
                return json.dumps({
                    'status': 'success',
                    'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
            elif command == 'echo':
                return json.dumps({
                    'status': 'success',
                    'data': cmd.get('text', '')
                })
            else:
                return json.dumps({
                    'status': 'error',
                    'message': f'未知命令: {command}'
                })
        except json.JSONDecodeError:
            # 如果不是JSON，原样返回
            return f"ECHO: {message}"

    def stop(self):
        """停止服务器"""
        if self.server_socket:
            self.server_socket.close()
            print("🛑 服务器已停止")


# tcp_client.py - 基础TCP客户端
import socket
import json
import time


class TCPClient:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        """连接到服务器"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        print(f"✅ 连接到服务器 {self.host}:{self.port}")

    def send_command(self, command, **kwargs):
        """发送命令到服务器"""
        if not self.socket:
            print("❌ 请先连接服务器")
            return

        # 构造JSON命令
        cmd = {'command': command, **kwargs}
        message = json.dumps(cmd)

        # 发送数据
        self.socket.send(message.encode('utf-8'))

        # 接收响应
        response = self.socket.recv(1024).decode('utf-8')

        try:
            return json.loads(response)
        except:
            return response

    def disconnect(self):
        """断开连接"""
        if self.socket:
            self.socket.close()
            print("👋 断开服务器连接")


# 使用示例
if __name__ == "__main__":
    # 先在一个终端运行服务器
    # server = TCPServer()
    # server.start()

    # 然后在另一个终端运行客户端
    client = TCPClient()
    client.connect()

    # 发送echo命令
    response = client.send_command('echo', text='Hello, TCP!')
    print(f"服务器响应: {response}")

    # 发送时间请求
    response = client.send_command('time')
    print(f"服务器时间: {response}")

    client.disconnect()
