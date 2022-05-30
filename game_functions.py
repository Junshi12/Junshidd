#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r'''
模块game_functions，可避免alien_invasion.py太长，并使其逻辑更容易理解。 
隔离事件，可将事件管理与游戏的其他方面（如 更新屏幕）分离。
'''
import os
import sys
from time import sleep
import pygame
import configparser

from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ 响应键按下事件 """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:    # 按空格键发射子弹
        if stats.game_active:    # 游戏处于活动状态时才能发射子弹
            fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_p:    # 按下p键开始游戏
        if not stats.game_active:    # 游戏处于非活动状态时，按下p键才重新开始游戏
            start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)
    elif event.key == pygame.K_q:    # 按下q键退出程序
        write_config(stats)    # 退出程序前将获取到的最高分更新到配置文件中
        sys.exit()

def check_keyup_events(event, ship):
    """ 响应键松开事件 """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """ 响应按键和鼠标事件 """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            write_config(stats)    # 退出程序前将获取到的最高分更新到配置文件中
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets)                
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """ 在玩家单击Play按钮时开始新游戏 """
    # 鼠标是否单击了按钮矩形区域
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    # 加上game_active=False的判断，是为了防止Play按钮不可见，但单击其所在区域时游戏依然会做出响应的问题。
    if button_clicked and not stats.game_active:        
        # 重新开始游戏
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)

def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ 重新开始游戏 """
    # 开始游戏后，隐藏鼠标光标
    pygame.mouse.set_visible(False)
    # 重置游戏设置（重新开始游戏时，将发生变化的属性重置为初始值，否则新游戏开始，速度设置等将是前一次的增加值。）
    ai_settings.initialize_dynamic_settings()    
    # 重置游戏统计信息
    stats.reset_stats()
    stats.game_active = True
    # 重置记分牌图像信息
    sb.prep_scoreboard()
    # 清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()
    # 创建一群新的外星人，并让飞船居中
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """ 更新屏幕上的图像，并切换到新屏幕 """
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # 在指定位置绘制飞船
    ship.blitme()
    # 绘制一群外星人
    aliens.draw(screen)
    # 显示得分牌
    sb.show_score()
    # 如果游戏处于非活动状态，就绘制Play按钮；
    # 为让Play按钮位于其他所有屏幕元素上面，我们在绘制其他所有游戏元素后再绘制这个按钮，然后切换到新屏幕。
    if not stats.game_active:
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ 更新子弹的位置，并删除已消失的子弹（移除对象，将其从内存中销毁） """
    # 更新子弹的位置
    bullets.update()
    # 删除已消失的子弹；移除对象，将其从内存中销毁
    for bullet in bullets.copy():    # 不应从列表或编组中删除条目，因此必须遍历编组的副本
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print('有效子弹数：%d' % (len(bullets)))
    # 检查子弹和外星人是否发生碰撞，将发生碰撞的两者删除；全部外星人被射杀完后再创建一批
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
    """ 检查是否诞生了新的最高得分 """
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ 检查响应子弹和外星人的碰撞 """
    # 检查是否有子弹击中了外星人
    # 如果有被击中（两者发生了碰撞），就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # 记录消灭外星人的得分，并显示
    if collisions:
        for aliens in collisions.values():    # 修复计分方式（一个子弹消灭多个外星人，或者一个外星人被多个子弹消灭），确保将消灭的每个外星人的点数都被计入得分
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)    # （每次射击后）检查是否诞生了新的最高分
    # 外星人被射杀完后并提高一个等级，再创建一批外星人
    if len(aliens) == 0:
        # 删除现有的子弹，加快游戏节奏，并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()    # 在整群外星人被消灭后，加快游戏节奏，再创建一群新的外星人
        # 提高等级
        start_new_level(stats, sb)
        # 创建一批外星人
        create_fleet(ai_settings, screen, ship, aliens)

def start_new_level(stats, sb):
    """ 当外星人群被消灭完时，开始新的等级 """
    # 提高等级
    stats.level += 1
    sb.prep_level()

def check_fleet_edges(ai_settings, aliens):
    """ 有外星人到达屏幕边缘时采取相应的措施（整体下移并改变它们的方向） """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """ 将整群外星人下移，并改变它们的方向 """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ 响应被外星人撞到的飞船 """
    if stats.ships_left > 0:
        # 将ships_left（(玩家拥有的)剩余飞船数量）减1
        stats.ships_left -= 1
        # 更新记分牌中剩余飞船数（飞船图像）
        sb.prep_ships()
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群外星人，并将飞船复位到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # 暂停0.5s
        sleep(0.5)
    else:   # 在玩家的飞船都用完后将game_active设置为False，表示游戏结束
        stats.game_active = False
        # 游戏结束后，重新显示鼠标光标（由于游戏开始时将鼠标光标隐藏了）
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ 检查是否有外星人到达屏幕底端，如果有按飞船被撞击到一样处理 """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 有外星人到达屏幕底端，按飞船被撞击到一样处理
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ 检查是否有外星人位于屏幕边缘，并更新整群外星人的位置 """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # 检查外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def fire_bullet(ai_settings, screen, ship, bullets):
    """ 如果屏幕中未到达子弹限制，就发射一颗子弹 """
    # 创建新子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    """ 计算每行可容纳多少个外星人 """
    available_space_x = ai_settings.screen_width - 2 * alien_width    # 可容纳外星人的水平宽度
    number_aliens_x = int(available_space_x / (2 * alien_width))    # 一行可容纳的外星人个数
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """ 计算屏幕可容纳多少行外星人 """
    available_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """ 创建一个外星人，并将其放在当前行 """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien_height + 2 * alien_height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """ 创建外星人群 """
    # 创建一个外星人，并计算一行可容纳多少个外星人
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_cur_path():
    """ 获取文件的当前绝对路径 """
    # 获取文件的当前路径（绝对路径）
    # cur_path = os.path.dirname(os.path.realpath(__file__))    # 这种方式打包的exe无法运行
    cur_path = os.getcwd()
    return cur_path

def get_prnt_path():
    """ 获取当前文件路径的父路径 """
    prnt_path = os.path.abspath(os.path.join(get_cur_path(), '..'))
    return prnt_path

def read_config(stats):
    """ 读取配置文件的【已经获得的最高分】属性值 """
    conf = configparser.ConfigParser()
    common_conf_file = os.path.join(os.path.join(get_cur_path(), 'data'), 'common.conf')
    conf.read(common_conf_file, encoding='utf-8')    # r'E:\PythonWorkspace\alien_invasion\data\common.conf'
    got_high_score = conf.get('score', 'got_high_score')
    stats.high_score = int(got_high_score)

def write_config(stats):
    """ 将【已经获得的最高分】属性值写到配置文件中 """
    try:
        conf = configparser.ConfigParser()
        conf.add_section('score')
        rounded_score = int(round(stats.high_score, -1))
        conf.set('score', 'got_high_score', str(rounded_score))
    except configparser.DuplicateSectionError:
        print("Section 'score' already exists")
    common_conf_file = os.path.join(os.path.join(get_cur_path(), 'data'), 'common.conf')
    conf.write(open(common_conf_file, 'w', encoding='utf-8'))    # r'E:\PythonWorkspace\alien_invasion\data\common.conf'
