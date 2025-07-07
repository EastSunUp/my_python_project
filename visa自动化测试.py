

# 示例：用AI生成你需要的PyVISA代码（完全可用现有知识修改）
# 对AI提问："用PyVISA连接KEYSIGHT示波器，截图并保存为JSON"
import visa

rm = visa.ResourceManager()
scope = rm.open_resource('USB0::0x2A8D::0x0396::CN123456::INSTR')
scope.write(":SAVE:IMAGE 'C:/data.png'")  # AI生成的代码
# 你只需：1.修改设备地址 2.调整保存路径 → 客户方案完成！

