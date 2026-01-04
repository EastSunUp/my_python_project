

# TODO: 使用周立功自带的ddl文件对输入到电脑的can高低电平解码成can报文等信息
#!/usr/bin/env python3
"""
周立功CAN盒接收与DBC解析完整示例
前置工作：
1. 将官方提供的 `zlgcan.dll` 和 `zlgcan.py` 放在此脚本同级目录。
2. 安装 cantools 库: pip install cantools
"""

import time
import cantools
from zlgcan import ZCAN, DEVICE_TYPE, CAN_FRAME     # 周立功解码

class ZlgCanWithDbcDecoder:
    def __init__(self, dbc_file_path):
        """
        初始化CAN设备和DBC数据库
        :param dbc_file_path: DBC文件路径
        """
        # 1. 加载DBC数据库
        print(f"[INFO] 正在加载DBC数据库: {dbc_file_path}")
        try:
            self.db = cantools.database.load_file(dbc_file_path)
            print(f"[SUCCESS] DBC加载成功，共 {len(self.db.messages)} 条报文定义。")
        except Exception as e:
            print(f"[ERROR] 无法加载DBC文件: {e}")
            raise

        # 2. 初始化周立功CAN设备
        print("[INFO] 正在初始化ZLG CAN设备...")
        self.zcan = ZCAN()

        # 打开设备，设备类型根据你的硬件型号修改，例如：DEVICE_TYPE.ZCAN_USBCANFD_200U
        device_type = DEVICE_TYPE.ZCAN_USBCAN2  # 请修改为你的设备型号
        device_index = 0  # 第一台设备
        self.device_handle = self.zcan.OpenDevice(device_type, device_index, 0)
        if self.device_handle == 0:
            print("[ERROR] 打开CAN设备失败!")
            raise RuntimeError("打开CAN设备失败")
        print(f"[SUCCESS] 设备打开成功，句柄: {self.device_handle}")

        # 3. 初始化CAN通道参数 (以CAN20标准，500k波特率为例)
        self.channel = 0  # 使用通道0
        self.init_can_channel(baudrate=500000)

    def init_can_channel(self, baudrate=500000):
        """初始化指定CAN通道"""
        # 周立功的CAN解码的ddl文件
        from zlgcan import ZCAN_CHANNEL_INIT_CONFIG
        config = ZCAN_CHANNEL_INIT_CONFIG()
        config.can_type = 0  # 标准CAN
        config.config.can.acc_code = 0x00000000
        config.config.can.acc_mask = 0xFFFFFFFF
        config.config.can.mode = 0  # 正常模式
        config.config.can.baud_rate = baudrate

        self.channel_handle = self.zcan.InitCAN(self.device_handle, self.channel, config)
        if self.channel_handle == 0:
            print(f"[ERROR] 初始化CAN通道{self.channel}失败!")
            self.zcan.CloseDevice(self.device_handle)
            raise RuntimeError("初始化CAN通道失败")
        print(f"[SUCCESS] 通道{self.channel}初始化成功，句柄: {self.channel_handle}")

        # 启动CAN通道
        if not self.zcan.StartCAN(self.channel_handle):
            print(f"[ERROR] 启动CAN通道{self.channel}失败!")
            self.zcan.CloseDevice(self.device_handle)
            raise RuntimeError("启动CAN通道失败")
        print(f"[INFO] 通道{self.channel}已启动。")

    def receive_and_decode(self, timeout_ms=1000):
        """
        接收并解码一帧CAN报文
        :param timeout_ms: 接收超时时间（毫秒）
        :return: (成功标志, 解码后的信息字典)
        """
        # 1. 接收原始CAN帧
        frames = self.zcan.Receive(self.channel_handle, 1, timeout_ms)
        if not frames:
            return False, {"error": f"接收超时 (>{timeout_ms}ms)或无数据"}

        frame = frames[0]  # 取第一帧
        can_id = frame.can_id
        can_data = bytes(frame.data[:frame.can_dlc])  # 转换为bytes

        # 2. 使用DBC解码
        try:
            decoded_signals = self.db.decode_message(can_id, can_data)
            message_name = self.db.get_message_by_frame_id(can_id).name

            result = {
                "timestamp": time.time(),
                "can_id": can_id,
                "can_id_hex": f"0x{can_id:X}",
                "message_name": message_name,
                "raw_data": can_data.hex().upper(),
                "signals": decoded_signals,
                "success": True
            }
            return True, result

        except KeyError:
            # DBC中未找到该ID的定义
            result = {
                "timestamp": time.time(),
                "can_id": can_id,
                "raw_data": can_data.hex().upper(),
                "success": False,
                "error": f"DBC中未找到ID 0x{can_id:X} 的定义"
            }
            return True, result  # 接收到数据但解码失败
        except Exception as e:
            result = {
                "timestamp": time.time(),
                "can_id": can_id,
                "raw_data": can_data.hex().upper(),
                "success": False,
                "error": f"解码过程出错: {e}"
            }
            return True, result

    def run_receive_loop(self, max_frames=50):
        """简单的接收循环示例"""
        print(f"\n[INFO] 开始监听CAN总线，最多接收 {max_frames} 帧... (按Ctrl+C退出)")
        frame_count = 0

        while frame_count < max_frames:
            received, frame_info = self.receive_and_decode(timeout_ms=100)

            if not received:
                # 超时是正常的，继续循环
                continue

            frame_count += 1
            self._print_frame_info(frame_count, frame_info)

        print(f"\n[INFO] 已接收 {frame_count} 帧，监听结束。")

    def _print_frame_info(self, seq, info):
        """打印帧信息"""
        print(f"\n--- 帧 #{seq} ---------------------------------")
        print(f"  时间: {time.strftime('%H:%M:%S', time.localtime(info['timestamp']))}")
        print(f"  CAN ID: {info['can_id_hex']} ({info.get('message_name', 'UNKNOWN')})")
        print(f"  原始数据: {info['raw_data']}")

        if info['success'] and info['signals']:
            print(f"  信号解析:")
            for signal, value in info['signals'].items():
                print(f"    - {signal}: {value}")
        else:
            print(f"  [注意] {info.get('error', '未知错误')}")

    def cleanup(self):
        """清理资源"""
        print("\n[INFO] 正在关闭设备释放资源...")
        if hasattr(self, 'zcan') and self.device_handle:
            self.zcan.ResetCAN(self.channel_handle)
            self.zcan.CloseDevice(self.device_handle)
            print("[INFO] 设备已关闭。")

def main():
    # ====== 用户配置区域 ======
    # 1. 你的DBC文件路径
    DBC_FILE_PATH = "path/to/your/BLECAN.dbc"  # 请务必修改为正确的路径，可使用绝对路径

    # 2. 设备型号常量 (根据你的硬件在zlgcan.py的DEVICE_TYPE中查找)
    # 例如: ZCAN_USBCAN2, ZCAN_USBCANFD_200U, ZCAN_PCIECANFD_400U 等
    # =========================

    decoder = None
    try:
        # 创建解码器实例
        decoder = ZlgCanWithDbcDecoder(DBC_FILE_PATH)

        # 运行接收循环示例
        decoder.run_receive_loop(max_frames=20)

    except KeyboardInterrupt:
        print("\n[INFO] 用户中断。")
    except Exception as e:
        print(f"\n[ERROR] 程序运行出错: {e}")
    finally:
        if decoder:
            decoder.cleanup()

if __name__ == "__main__":
    main()






