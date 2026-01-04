
# !/usr/bin/env python3
"""
CAN报文DBC解析完整示例
使用前请安装: pip install cantools
"""

import os
import sys
import cantools
from datetime import datetime
from typing import Dict, List, Optional, Any


class CANParser:
    """CAN报文解析器类"""

    def __init__(self, dbc_path: str, debug: bool = False):
        """
        初始化CAN解析器

        参数:
            dbc_path: DBC文件路径
            debug: 是否启用调试模式
        """
        self.debug = debug
        self.db = None
        self.dbc_path = dbc_path
        self.message_cache = {}  # 缓存已解析的报文ID

        # 加载DBC数据库
        self.load_database()

        if self.debug:
            print(f"[INFO] CAN解析器初始化完成，加载 {len(self.db.messages)} 条报文定义")

    def load_database(self) -> None:
        """加载DBC数据库文件"""
        try:
            # 方法1: 使用绝对路径确保文件正确加载
            abs_path = os.path.abspath(self.dbc_path)

            if self.debug:
                print(f"[DEBUG] 尝试加载DBC文件: {abs_path}")
                print(f"[DEBUG] 文件是否存在: {os.path.exists(abs_path)}")

            if not os.path.exists(abs_path):
                print(f"[ERROR] DBC文件不存在: {abs_path}")

                # 尝试在项目目录中查找
                script_dir = os.path.dirname(os.path.abspath(__file__))
                alt_path = os.path.join(script_dir, "..", "..", "drivers", "BLECAN.dbc")
                alt_path = os.path.normpath(alt_path)

                if os.path.exists(alt_path):
                    print(f"[INFO] 找到备选路径: {alt_path}")
                    abs_path = alt_path
                else:
                    raise FileNotFoundError(f"无法找到DBC文件: {self.dbc_path}")

            # 加载DBC文件
            self.db = cantools.database.load_file(abs_path)

            if self.debug:
                print(f"[SUCCESS] DBC文件加载成功: {abs_path}")
                self.print_database_summary()

        except Exception as e:
            print(f"[ERROR] 加载DBC文件失败: {e}")
            sys.exit(1)

    def print_database_summary(self) -> None:
        """打印数据库摘要信息"""
        print("\n" + "=" * 60)
        print("DBC数据库摘要信息")
        print("=" * 60)
        print(f"版本: {self.db.version if hasattr(self.db, 'version') else 'N/A'}")
        print(f"总线类型: {self.db.bus_type if hasattr(self.db, 'bus_type') else 'N/A'}")
        print(f"报文定义数量: {len(self.db.messages)}")
        print(f"节点数量: {len(self.db.nodes) if hasattr(self.db, 'nodes') else 'N/A'}")

        # 打印前10条报文定义
        print("\n报文定义 (前10条):")
        print("-" * 60)
        for i, message in enumerate(list(self.db.messages)[:10]):
            print(f"  [{i + 1}] ID: 0x{message.frame_id:X} ({message.frame_id}), "
                  f"名称: {message.name}, "
                  f"长度: {message.length}字节, "
                  f"信号数: {len(message.signals)}")

        # 特别检查ID 281的报文
        print("\n检查ID 281的报文:")
        print("-" * 60)
        try:
            msg_281 = self.db.get_message_by_frame_id(281)
            print(f"  找到报文: {msg_281.name}")
            print(f"  信号列表:")
            for signal in msg_281.signals:
                signal_info = f"    - {signal.name} ({signal.start}:{signal.length}位)"
                if signal.choices:
                    signal_info += f", 枚举值: {signal.choices}"
                print(signal_info)
        except KeyError:
            print("  未找到ID 281的报文定义")

        print("=" * 60 + "\n")

    def decode_raw_frame(self, can_id: int, data: bytes, timestamp: float = None) -> Dict[str, Any]:
        """
        解码原始CAN帧

        参数:
            can_id: CAN ID (十进制或十六进制)
            data: CAN数据字节
            timestamp: 时间戳 (可选)

        返回:
            解析后的数据字典
        """
        try:
            # 确保数据是bytes类型
            if isinstance(data, list):
                data = bytes(data)
            elif isinstance(data, bytearray):
                data = bytes(data)

            # 解码报文
            decoded = self.db.decode_message(can_id, data)

            # 构建结果
            result = {
                "timestamp": timestamp or datetime.now().timestamp(),
                "can_id": can_id,
                "can_id_hex": f"0x{can_id:X}",
                "raw_data": data.hex(),
                "signals": decoded,
                "message_name": self.get_message_name(can_id),
                "length": len(data),
                "success": True
            }

            if self.debug:
                self._print_decoded_frame(result)

            return result

        except KeyError:
            print(f"[WARNING] 未知CAN ID: 0x{can_id:X} ({can_id})")
            return {
                "timestamp": timestamp,
                "can_id": can_id,
                "raw_data": data.hex() if hasattr(data, 'hex') else str(data),
                "success": False,
                "error": f"未知CAN ID: 0x{can_id:X}"
            }
        except Exception as e:
            print(f"[ERROR] 解码失败 (ID: 0x{can_id:X}): {e}")
            return {
                "timestamp": timestamp,
                "can_id": can_id,
                "raw_data": data.hex() if hasattr(data, 'hex') else str(data),
                "success": False,
                "error": str(e)
            }

    def get_message_name(self, can_id: int) -> str:
        """获取报文名称"""
        try:
            return self.db.get_message_by_frame_id(can_id).name
        except:
            return "UNKNOWN"

    def _print_decoded_frame(self, frame: Dict[str, Any]) -> None:
        """打印解码后的帧信息"""
        if not frame["success"]:
            print(f"[DECODE] 解码失败: {frame.get('error', 'Unknown error')}")
            return

        print(f"\n[DECODE] 报文: {frame['message_name']} (ID: {frame['can_id_hex']})")
        print(f"        时间: {datetime.fromtimestamp(frame['timestamp']).strftime('%H:%M:%S.%f')[:-3]}")
        print(f"        原始数据: {frame['raw_data'].upper()}")
        print(f"        信号解析:")

        for signal_name, signal_value in frame["signals"].items():
            signal_info = f"          - {signal_name}: {signal_value}"

            # 尝试获取信号单位
            try:
                msg = self.db.get_message_by_frame_id(frame["can_id"])
                for signal in msg.signals:
                    if signal.name == signal_name and signal.unit:
                        signal_info += f" {signal.unit}"
                        break
            except:
                pass

            print(signal_info)

    def decode_multiple_frames(self, frames: List[tuple]) -> List[Dict[str, Any]]:
        """
        批量解码CAN帧

        参数:
            frames: CAN帧列表，每个元素为 (can_id, data, timestamp) 格式

        返回:
            解析结果列表
        """
        results = []
        for frame in frames:
            if len(frame) == 2:
                can_id, data = frame
                timestamp = None
            else:
                can_id, data, timestamp = frame

            result = self.decode_raw_frame(can_id, data, timestamp)
            results.append(result)

        return results

    def find_signal_in_database(self, signal_name: str) -> List[Dict]:
        """
        在数据库中查找信号

        参数:
            signal_name: 信号名称或部分名称

        返回:
            包含该信号的报文列表
        """
        results = []
        for message in self.db.messages:
            for signal in message.signals:
                if signal_name.lower() in signal.name.lower():
                    results.append({
                        "message_id": message.frame_id,
                        "message_name": message.name,
                        "signal_name": signal.name,
                        "signal_start": signal.start,
                        "signal_length": signal.length,
                        "signal_choices": signal.choices if hasattr(signal, 'choices') else None
                    })

        return results


def main():
    """主函数示例"""
    print("CAN报文解析示例")
    print("=" * 60)

    # 配置参数
    # 方式1: 使用绝对路径
    DBC_FILE = r"E:\UwbProject\host\btkey_host\drivers\BLECAN.dbc"

    # 方式2: 使用相对路径（基于当前脚本位置）
    # script_dir = os.path.dirname(os.path.abspath(__file__))
    # DBC_FILE = os.path.join(script_dir, "..", "..", "drivers", "BLECAN.dbc")

    # 创建解析器实例
    parser = CANParser(DBC_FILE, debug=True)

    # 示例1: 查找特定信号
    print("\n查找信号 'btkey_loc_area':")
    search_results = parser.find_signal_in_database("btkey_loc_area")
    for result in search_results:
        print(f"  在报文 {result['message_name']} (ID: 0x{result['message_id']:X}) 中找到信号: {result['signal_name']}")
        if result['signal_choices']:
            print(f"    枚举值: {result['signal_choices']}")

    # 示例2: 解码示例CAN帧
    print("\n" + "=" * 60)
    print("解码示例CAN帧")
    print("=" * 60)

    # 准备示例数据 (ID 281的示例数据)
    example_frames = [
        # (CAN_ID, 数据字节, 时间戳)
        (281, [0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00], 1698300000.123),  # 信号值 4
        (281, [0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00], 1698300000.456),  # 信号值 2
        (281, [0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0x00], 1698300000.789),  # 信号值 6
        (0x100, [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08], 1698300001.000),  # 未知ID示例
    ]

    # 批量解码
    results = parser.decode_multiple_frames(example_frames)

    # 统计结果
    success_count = sum(1 for r in results if r["success"])
    print(f"\n解析完成: {success_count}/{len(results)} 帧成功解码")

    # 示例3: 实时解析模拟
    print("\n" + "=" * 60)
    print("实时解析模拟 (每秒1帧)")
    print("=" * 60)

    import time
    import random

    for i in range(5):
        # 模拟随机数据
        random_value = random.choice([0, 1, 2, 3, 4, 5, 6])
        can_data = bytes([0x00, 0x00, 0x00, random_value, 0x00, 0x00, 0x00, 0x00])

        result = parser.decode_raw_frame(281, can_data)

        if result["success"] and "btkey_loc_area" in result["signals"]:
            value = result["signals"]["btkey_loc_area"]
            print(f"  时间: {datetime.now().strftime('%H:%M:%S')}, "
                  f"btkey_loc_area = {value}")

        time.sleep(1)


if __name__ == "__main__":
    main()
