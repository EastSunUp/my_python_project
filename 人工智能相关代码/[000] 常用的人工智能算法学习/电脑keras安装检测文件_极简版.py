
import sys
import os
print("=== 系统信息 ===")
print(f"Python路径: {sys.executable}")
print(f"Python版本: {sys.version}")
print(f"工作目录: {os.getcwd()}")
print(f"PATH: {os.environ.get('PATH', '')}")

print("\n=== 包检查 ===")
try:
    import tensorflow as tf
    print(f"✅ TensorFlow: {tf.__version__}")
    print(f"TensorFlow路径: {tf.__file__}")
except Exception as e:
    print(f"❌ TensorFlow导入失败: {e}")

print("\n=== 尝试不同导入方式 ===")
# 方式1
try:
    from tensorflow import keras
    print(f"✅ from tensorflow import keras 成功")
    print(f"Keras路径: {keras.__file__}")
except Exception as e:
    print(f"❌ 方式1失败: {e}")

# 方式2
try:
    import tensorflow.keras as keras
    print(f"✅ import tensorflow.keras 成功")
except Exception as e:
    print(f"❌ 方式2失败: {e}")

# 方式3
try:
    from tensorflow.keras import layers
    print(f"✅ from tensorflow.keras import layers 成功")
except Exception as e:
    print(f"❌ 方式3失败: {e}")

