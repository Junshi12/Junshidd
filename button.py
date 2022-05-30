#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r'''
button模块，其中包含Button类，它负责管理和创建带标签的实心矩形按钮。 
'''
import pygame.font

class Button():
    """ 管理和创建带标签的实心矩形按钮 """
    def __init__(self, ai_settings, screen, msg):
        """ 初始化按钮是属性 """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        # 设置按钮的尺寸大小、背景颜色、字体大小等属性
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)    # 亮绿色
        self.text_color = (255, 255, 255)    # 白色
        self.font = pygame.font.SysFont('consolas', 36, bold=1)    # pygame.font.SysFont(None, 48)，这种方式打包的exe，在Windows下找不到对应字体而无法运行
        # 创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        # 按钮的标签只需创建一次
        self.prep_msg(msg)    # 将msg渲染为图像，并使其在按钮上居中
    
    def prep_msg(self, msg):
        """ 将msg渲染为图像，并使其在按钮上居中 """
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """ 绘制一个用颜色填充的按钮，再绘制文本 """
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
