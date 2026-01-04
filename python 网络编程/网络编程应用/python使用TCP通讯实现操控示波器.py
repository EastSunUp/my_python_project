# instrument_control.py - 仪器控制模拟
import socket
import time
import struct
import numpy as np


class OscilloscopeController:
    """模拟示波器控制器"""

    # 命令定义
    COMMANDS = {
        'START': b'START',
        'STOP': b'STOP',
        'GET_WAVEFORM': b'GET_WAVE',
        'SET_TIMEBASE': b'SET_TB',
        'SET_VOLTAGE': b'SET_VOLT',
        'AUTO_SETUP': b'AUTO'
    }

    def __init__(self, host='192.168.1.100', port=4000):
        self.host = host
        self.port = port
        self.socket = None
        self.is_connected = False

    def connect(self):
        """连接示波器"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)  # 5秒超时
            self.socket.connect((self.host, self.port))
            self.is_connected = True
            print(f"✅ 成功连接示波器 {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            return False

    def send_command(self, command, params=None):
        """发送命令到示波器"""
        if not self.is_connected:
            print("❌ 未连接示波器")
            return None

        try:
            # 发送命令
            self.socket.send(command)

            # 如果有参数，发送参数
            if params:
                if isinstance(params, (int, float)):
                    # 对于数值参数，转换为字节
                    param_bytes = struct.pack('f', float(params))
                    self.socket.send(param_bytes)
                elif isinstance(params, str):
                    self.socket.send(params.encode('utf-8'))

            # 接收响应
            response = self.socket.recv(4096)
            return response

        except socket.timeout:
            print("⏰ 命令超时")
            return None
        except Exception as e:
            print(f"❌ 命令执行失败: {e}")
            return None

    def capture_waveform(self, channel=1):
        """捕获波形数据"""
        print(f"📈 正在捕获通道 {channel} 的波形...")

        # 发送捕获命令
        command = self.COMMANDS['GET_WAVEFORM']
        response = self.send_command(command, str(channel))

        if response:
            # 模拟解析波形数据
            # 实际中这里会解析二进制数据
            time_points = np.linspace(0, 1, 1000)
            amplitude = np.sin(2 * np.pi * 50 * time_points)  # 50Hz正弦波
            noise = np.random.normal(0, 0.1, 1000)
            waveform = amplitude + noise

            return {
                'time': time_points.tolist(),
                'voltage': waveform.tolist(),
                'channel': channel,
                'sampling_rate': 1000
            }
        return None

    def set_timebase(self, time_per_division):
        """设置时基"""
        print(f"⏱️ 设置时基: {time_per_division}s/div")
        return self.send_command(self.COMMANDS['SET_TIMEBASE'], time_per_division)

    def set_voltage_scale(self, voltage_per_division):
        """设置电压标度"""
        print(f"⚡ 设置电压标度: {voltage_per_division}V/div")
        return self.send_command(self.COMMANDS['SET_VOLTAGE'], voltage_per_division)

    def auto_setup(self):
        """自动设置"""
        print("🔧 执行自动设置...")
        response = self.send_command(self.COMMANDS['AUTO_SETUP'])
        time.sleep(2)  # 模拟自动设置时间
        print("✅ 自动设置完成")
        return response

    def disconnect(self):
        """断开连接"""
        if self.socket:
            self.socket.close()
            self.is_connected = False
            print("👋 断开示波器连接")


# 模拟示波器服务器
class MockOscilloscope:
    """模拟示波器服务器"""

    def __init__(self, port=4000):
        self.port = port
        self.running = False

    def start(self):
        """启动模拟示波器"""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('127.0.0.1', self.port))
        server.listen(1)

        print(f"📡 模拟示波器启动在端口 {self.port}")
        self.running = True

        while self.running:
            client, addr = server.accept()
            print(f"🔌 客户端连接: {addr}")

            # 处理客户端命令
            while True:
                try:
                    data = client.recv(1024)
                    if not data:
                        break

                    # 处理命令
                    response = self.process_command(data)
                    client.send(response)

                except ConnectionResetError:
                    break

            client.close()

        server.close()

    def process_command(self, data):
        """处理客户端命令"""
        # 这里简化处理，实际会有更复杂的协议
        if data.startswith(b'GET_WAVE'):
            # 返回模拟的波形数据
            return b'WAVEFORM_DATA'
        elif data.startswith(b'SET_TB'):
            return b'TIMEBASE_SET'
        elif data.startswith(b'SET_VOLT'):
            return b'VOLTAGE_SET'
        elif data.startswith(b'AUTO'):
            return b'AUTO_SETUP_COMPLETE'
        else:
            return b'UNKNOWN_COMMAND'


# 使用示例
if __name__ == "__main__":
    # 启动模拟示波器（在一个终端运行）
    # scope = MockOscilloscope()
    # scope.start()

    # 控制示波器（在另一个终端运行）
    controller = OscilloscopeController('127.0.0.1', 4000)

    if controller.connect():
        # 自动设置
        controller.auto_setup()

        # 设置参数
        controller.set_timebase(0.001)  # 1ms/div
        controller.set_voltage_scale(1.0)  # 1V/div

        # 捕获波形
        waveform = controller.capture_waveform(channel=1)
        if waveform:
            print(f"📊 捕获到 {len(waveform['voltage'])} 个数据点")
            print(f"📐 采样率: {waveform['sampling_rate']} Hz")

        controller.disconnect()
        