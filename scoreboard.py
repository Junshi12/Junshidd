#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r'''
scoreboard模块，其中包含Scoreboard类，它负责管理游戏得分和等级的记录、显示，剩余飞船数的显示等。 
'''
import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
    """ 管理和显示游戏的等级、得分等的类 """
    def __init__(self, ai_settings, screen, stats):
        """ 初始化显示得分涉及的属性 """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        # 显示得分信息时使用的字体颜色、大小等设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont('consolas', 36, bold=1)    # pygame.font.SysFont(None, 48)，这种方式打包的exe，在Windows下找不到对应字体而无法运行
        # 准备包含剩余飞船数量（飞船图像）、最高得分、当前得分和游戏等级的图像
        self.prep_scoreboard()

    def prep_scoreboard(self):
        """ 渲染得分牌图像；准备包含剩余飞船数量（飞船图像）、最高得分、当前得分和游戏等级的图像 """
        self.prep_score()    # 重置当前得分图像
        self.prep_high_score()    # 重置最高分图像
        self.prep_level()    # 重置游戏等级图像
        self.prep_ships()    # 重置剩余飞船数（飞船图像）

    def prep_score(self):
        """ 将得分转换为一幅渲染的图像 """
        rounded_score = int(round(self.stats.score, -1))    # round()函数，第二个参数为精确到的小数位数；为负数，表示将圆整到最近的10、100、1000等整数倍（p2.7round()总是返回一个小数，因此使用int()来确保为整数，而p3+可省略int()的调用）
        score_str = "{:,}".format(rounded_score)    # 将数字格式化为“,”分隔的千分位格式
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)
        # 将得分牌放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """ 将最高得分转换为渲染的图像 """
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)
        # 将最高得分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """ 将等级转换为渲染的图像 """
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)
        # 将等级放在当前得分的下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """ 显示剩余飞船数量（飞船图像） """
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """ 在屏幕上显示剩余飞船数（飞船图像）、当前得分、最高得分和游戏等级 """
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # 绘制剩余飞船数（飞船图像）
        self.ships.draw(self.screen)