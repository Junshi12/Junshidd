#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r'''
settings模块，其中包含一个名为Settings 的类，用于将所有设置存储在一个地方，以免在代码中到处添加设置。
这样，我们就能传递一个设置对象，而不是众多不同的设置。另外，这让函数调用更简单，且在项目增大时修改游戏的外观更容易：
要修改游戏，只需修改settings.py中的一些值，而无需查找散布在文件中的不同设置。 
'''

class Settings():
    """ 存储《外星人入侵》所有设置的类 """
    def __init__(self):
        """ 初始化游戏的静态设置 """
        # 屏幕设置
        self.screen_width = 1200    # 屏幕宽
        self.screen_height = 800    # 屏幕高
        self.bg_color = (230, 230, 230)    # 屏幕背景颜色

        # 飞船的设置
        self.ship_limit = 3    # （玩家拥有的）最大飞船数

        # 子弹设置
        self.bullet_width = 3    # 子弹宽
        self.bullet_height = 15    # 子弹高
        self.bullet_color = 60, 60, 60    # 子弹颜色（深灰色）
        self.bullets_allowed = 3    # 屏幕上允许最大的子弹个数（未消失的）

        # 外星人(群)设置
        self.fleet_drop_speed = 10    # 外星人撞到屏幕边缘时，外星人群向下移动速度
        
        # 以什么样的速度加快游戏节奏
        # 用于控制游戏节奏的加快速度：1 表示游戏节奏始终不变；2 表示玩家每提高一个等级，游戏的节奏就翻倍。将其设置为1.1能够将游戏节奏提高到够快，让游戏既有难度，又并非不可完成。
        self.speedup_scale = 1.1
        # 外星人点数的提高速度（因为玩家每提高一个等级，游戏都变得更难，因此处于高等级时，外星人的点数更高）
        self.score_scale = 1.5

        # 初始化随游戏进行而变化的属性
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """ 初始化随游戏进行而变化的属性 """
        self.ship_speed_factor = 1.5    # 飞船速度
        self.bullet_speed_factor = 3    # 子弹速度，子弹的速度比飞船稍低
        self.alien_speed_factor = 1    # 外星人速度

        self.fleet_direction = 1    # fleet_direction为1表示向右移，为-1表示向左移
        # 记分，消灭一个外星人记录的点数；为确保每次开始新游戏时这个值都会被重置，因此放在init*方法中
        self.alien_points = 50

    def increase_speed(self):
        """ 提高速度设置和设置外星人点数 """
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        # 设置外星人点数(只取整数)
        self.alien_points = int(self.alien_points * self.score_scale)
