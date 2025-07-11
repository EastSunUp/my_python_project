

# 下列是游戏开发过程中常用的包:
# # 安装GUI库
# pip install pyqt5   # 或 pyside6
# # 安装游戏库
# pip install pygame
# pip install arcade
# pip install panda3d
# 另外, pygame是python中常用的开发游戏用的外接包

import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    screen.fill((0,0,255))  # 蓝色背景
    pygame.display.flip()

