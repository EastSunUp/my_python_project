

import tensorflow as tf
from tensorflow.keras import layers


def create_efficient_cnn(input_shape, num_classes, depth_level='medium'):
    """
    创建不同深度的CNN，平衡效率与性能
    """
    model = tf.keras.Sequential()

    if depth_level == 'shallow':
        # 浅层网络 - 高效率
        model.add(layers.Conv2D(32, 3, activation='relu', input_shape=input_shape)) # 卷积
        model.add(layers.MaxPooling2D(2))   # 池化
        model.add(layers.Conv2D(64, 3, activation='relu'))
        model.add(layers.MaxPooling2D(2))
        model.add(layers.Flatten())
        model.add(layers.Dense(128, activation='relu'))

    elif depth_level == 'medium':
        # 中等深度 - 平衡选择
        model.add(layers.Conv2D(32, 3, activation='relu', input_shape=input_shape))
        model.add(layers.Conv2D(32, 3, activation='relu'))
        model.add(layers.MaxPooling2D(2))
        model.add(layers.Conv2D(64, 3, activation='relu'))
        model.add(layers.Conv2D(64, 3, activation='relu'))
        model.add(layers.MaxPooling2D(2))
        model.add(layers.Conv2D(128, 3, activation='relu'))
        model.add(layers.GlobalAveragePooling2D())
        model.add(layers.Dense(256, activation='relu'))

    elif depth_level == 'deep':
        # 深层网络 - 高精度
        # 使用残差块避免梯度消失
        model.add(layers.Conv2D(64, 7, strides=2, activation='relu', input_shape=input_shape))
        model.add(layers.MaxPooling2D(3, strides=2))

        # 残差块1
        for _ in range(3):
            model.add(layers.Conv2D(64, 3, padding='same', activation='relu'))

        model.add(layers.Conv2D(128, 3, strides=2, activation='relu'))

        # 残差块2
        for _ in range(4):
            model.add(layers.Conv2D(128, 3, padding='same', activation='relu'))

        model.add(layers.GlobalAveragePooling2D())
        model.add(layers.Dense(512, activation='relu'))

    # 输出层
    model.add(layers.Dense(num_classes, activation='softmax'))

    return model


# 测试不同深度的模型
shallow_model = create_efficient_cnn((32, 32, 3), 10, 'shallow')
medium_model = create_efficient_cnn((32, 32, 3), 10, 'medium')
deep_model = create_efficient_cnn((32, 32, 3), 10, 'deep')

print("浅层网络参数量:", shallow_model.count_params())
print("中等网络参数量:", medium_model.count_params())
print("深层网络参数量:", deep_model.count_params())

