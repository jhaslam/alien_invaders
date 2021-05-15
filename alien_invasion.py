#! /usr/bin/env python3.9
""" A simple game written for the purposes of 
familiarizing myself with Python
"""

from pygame.sprite import Group
from pygame.surface import Surface
from ship import Ship
from settings import Settings

import pygame.display
import game_functions as gf

def run_game():
    pygame.init()
    ai_settings: Settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    ship = Ship(ai_settings, screen)
    bullets = Group()

    while True:
        gf.check_events(ai_settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(bullets)
        gf.update_screen(ai_settings, screen, ship, bullets)
        
run_game()
