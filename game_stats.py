#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r'''
game_stats模块，其中包含GameStats类，它负责跟踪游戏统计信息。 
'''

class GameStats():
    """ 跟踪游戏的统计信息类 """
    def __init__(self, ai_settings):
        """ 初始化统计信息 """
        self.ai_settings = ai_settings
        self.reset_stats()
        # 游戏刚启动时处于非活动状态，单击Play按钮时开始游戏
        self.game_active = False
        # 在任何情况下都不应该重置最高得分
        self.high_score = 0

    def reset_stats(self):
        """ 初始化在游戏运行期间可能变化的统计信息 """
        self.ships_left = self.ai_settings.ship_limit    # (玩家拥有的)剩余飞船数量
        self.score = 0    # 游戏得分
        self.level = 1    # 游戏等级