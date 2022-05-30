#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r'''
游戏《外星人入侵》基本框架

'''
import sys
import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from alien import Alien
import game_functions as gf

def run_game():
    # 初始化游戏平创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")
    # 创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    gf.read_config(stats)    # 读取已获得最高分的配置文件，一定要放于sb=Scoreboard(...)定义前，否则无法初始化加载
    # 创建记分牌
    sb = Scoreboard(ai_settings, screen, stats)
    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    # 创建一个用于存储子弹的编组
    # 用于存储所有有效的子弹，以便能够管理发射出去的所有子弹。这个编组将是pygame.sprite.Group类的一个实例；pygame.sprite.Group类类似于列表，但提供了有助于开发游戏的额外功能。
    bullets = Group()
    # 创建一个外星人编组
    aliens = Group()
    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)
    
    # 开始游戏的主循环
    while True:
        # 监听键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:    # 游戏处于活动状态时运行的程序
            # 更新飞船位置
            ship.update()
            # 更新未消失的子弹位置，并移除无效子弹
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            # 更新外星人位置
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
        # 设置背景颜色，每次循环时都重绘屏幕
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

# 主程序运行
if __name__ == '__main__':
    run_game()

