import pygame
import pygame.image
from pygame.sprite import Sprite
from pygame.surface import Surface

import image_functions as img_funs
from settings import Settings


class Ship(Sprite):
    def __init__(self, ai_settings: Settings, screen: Surface) -> None:
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = img_funs.load_as_surface('images/ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Set initial position of the ship to be bottom center of screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store position separately as a float value
        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False

    def center_ship(self) -> None:
        """Center the ship on the screen"""
        self.center = self.screen_rect.centerx

    def update(self) -> None:
        """Update the ship's position based on the movement flag"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        self.rect.centerx = self.center

    def blitme(self) -> None:
        """ Draw the ship at its current location """
        self.screen.blit(self.image, self.rect)
