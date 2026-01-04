
import cantools

def analyze_dbc_file(dbc_path: str):
    """分析DBC文件内容"""
    print(f"\n分析DBC文件: {dbc_path}")
    print("=" * 60)

    try:
        db = cantools.database.load_file(dbc_path)

        # 基本信息
        print(f"版本: {db.version}")
        print(f"节点数: {len(db.nodes)}")
        print(f"报文数: {len(db.messages)}")

        # 列出所有节点
        print("\n节点列表:")
        for node in db.nodes:
            print(f"  - {node.name}")

        # 列出所有报文
        print("\n报文列表:")
        for msg in db.messages:
            print(f"\n  ID: {hex(msg.frame_id)} ({msg.frame_id})")
            print(f"  名称: {msg.name}")
            print(f"  长度: {msg.length} 字节")
            print(f"  发送节点: {', '.join(msg.senders) if msg.senders else 'N/A'}")
            print(f"  信号数: {len(msg.signals)}")

            # 显示信号
            for signal in msg.signals:
                print(f"    * {signal.name}: {signal.start}位, {signal.length}位")
                if signal.unit:
                    print(f"      单位: {signal.unit}")
                if signal.scale != 1 or signal.offset != 0:
                    print(f"      缩放: {signal.scale}, 偏移: {signal.offset}")

        # 保存为JSON格式（可选）
        json_path = dbc_path.replace('.dbc', '_analysis.json')
        with open(json_path, 'w') as f:
            import json
            # 简化数据结构以便JSON序列化
            db_dict = {
                'version': db.version,
                'nodes': [n.name for n in db.nodes],
                'messages': [
                    {
                        'name': m.name,
                        'id': m.frame_id,
                        'length': m.length,
                        'signals': [
                            {
                                'name': s.name,
                                'start': s.start,
                                'length': s.length,
                                'unit': s.unit,
                                'scale': s.scale,
                                'offset': s.offset
                            }
                            for s in m.signals
                        ]
                    }
                    for m in db.messages
                ]
            }
            json.dump(db_dict, f, indent=2)

        print(f"\n分析结果已保存到: {json_path}")

    except Exception as e:
        print(f"分析DBC文件失败: {e}")


def create_simple_dbc_example():
    """创建简单的DBC文件示例"""
    from cantools.database import Database, Message, Signal, Node

    # 创建数据库
    db = Database()

    # 添加节点
    db.nodes.append(Node('ECU1'))
    db.nodes.append(Node('ECU2'))

    # 创建报文
    engine_msg = Message(
        name='EngineData',
        frame_id=0x100,
        length=8,
        signals=[
            Signal('EngineSpeed', start=0, length=16, scale=0.25, unit='rpm'),
            Signal('CoolantTemp', start=16, length=8, scale=0.5, offset=-40, unit='°C'),
            Signal('FuelLevel', start=24, length=8, scale=0.4, unit='%'),
        ],
        senders=['ECU1']
    )

    vehicle_msg = Message(
        name='VehicleData',
        frame_id=0x200,
        length=8,
        signals=[
            Signal('VehicleSpeed', start=0, length=16, scale=0.01, unit='km/h'),
            Signal('Odometer', start=16, length=32, scale=0.1, unit='km'),
        ],
        senders=['ECU2']
    )

    db.messages.extend([engine_msg, vehicle_msg])

    # 保存DBC文件
    dbc_content = cantools.database.dump(db)
    with open('example.dbc', 'w') as f:
        f.write(dbc_content)

    print("示例DBC文件已创建: example.dbc")


# 使用示例
if __name__ == "__main__":
    # 创建示例DBC文件
    create_simple_dbc_example()

    # 分析DBC文件
    analyze_dbc_file('example.dbc')

    # 运行主解码器（需要实际硬件）
    # main()

