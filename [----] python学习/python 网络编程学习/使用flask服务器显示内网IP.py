import socket
from flask import Flask

app = Flask(__name__)

@app.route('/ip')
def show_ip():
    """显示服务器内网IP"""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return f"内网IP: {local_ip}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
