#! /usr/bin/env python3.9
""" A simple game written for the purposes of 
familiarizing myself with Python
"""

import pygame.display
from pygame.sprite import Group
from pygame.surface import Surface

import game_functions as gf
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship


def run_game():
    pygame.init()
    ai_settings: Settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    play_button = Button(ai_settings, screen, "Play")
    stats = GameStats(ai_settings)
    scoreboard = Scoreboard(ai_settings, screen, stats)
    ship = Ship(ai_settings, screen)
    aliens = Group()
    bullets = Group()

    gf.create_fleet(ai_settings, screen, ship, aliens)

    while True:
        gf.check_events(ai_settings, stats, scoreboard, screen,
                        play_button, ship, aliens, bullets)

        if stats.game_active and not stats.game_paused:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, scoreboard,
                              ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, scoreboard,
                             ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, scoreboard, ship,
                         aliens, bullets, play_button)


run_game()
