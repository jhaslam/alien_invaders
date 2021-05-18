#! /usr/bin/env python3.9
""" A simple game written for the purposes of 
familiarizing myself with Python
"""

import pygame.display
from pygame.sprite import Group
from pygame.surface import Surface

import game_functions as gf
from settings import Settings
from game_stats import GameStats
from ship import Ship


def run_game():
    pygame.init()
    ai_settings: Settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    stats = GameStats(ai_settings)
    ship = Ship(ai_settings, screen)
    aliens = Group()
    bullets = Group()

    gf.create_fleet(ai_settings, screen, ship, aliens)

    while True:
        gf.check_events(ai_settings, stats, screen, ship, bullets)
       
        if stats.game_active and not stats.game_paused: 
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, ship, aliens, bullets)
        
run_game()
