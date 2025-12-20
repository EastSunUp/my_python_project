
# 检查TensorFlow和Keras版本
import tensorflow as tf
print(f"TensorFlow version: {tf.__version__}")

from tensorflow import keras
print(f"Keras version: {keras.__version__}")

# 简单的功能测试
model = keras.Sequential([keras.layers.Dense(units=1, input_shape=[1])])
print("Keras basic functionality works!")


