
# 对于初学者，建议按以下顺序学习：
"""
    1. Python编程基础
    2. 基本的线性代数（矩阵、向量）
    3. 基础的微积分（导数）
    4. 直接开始实践CNN代码
    5. 在实践中逐步学习理论
"""

# 当前我的python版本为3.13.8,tensorflow.keras暂时不支持python3.11以上的版本.
# 2025/11/28
import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

# 1. 加载数据集（这里使用MNIST手写数字数据集）
(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()

# 2. 数据预处理
train_images = train_images.reshape((60000, 28, 28, 1)).astype('float32') / 255
test_images = test_images.reshape((10000, 28, 28, 1)).astype('float32') / 255

# 3. 构建CNN模型
model = models.Sequential([
    # 卷积层1
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),

    # 卷积层2
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    # 卷积层3
    layers.Conv2D(64, (3, 3), activation='relu'),

    # 全连接层
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')  # 10个类别（0-9）
])

# 4. 编译模型
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# 5. 训练模型
history = model.fit(train_images, train_labels,
                    epochs=5,
                    validation_data=(test_images, test_labels))

# 6. 评估模型
test_loss, test_acc = model.evaluate(test_images, test_labels)
print(f'测试准确率: {test_acc}')

# 7. 可视化训练过程
plt.plot(history.history['accuracy'], label='训练准确率')
plt.plot(history.history['val_accuracy'], label='验证准确率')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()


