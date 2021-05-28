import pygame
import pygame.image
from pygame.sprite import Sprite
from pygame.surface import Surface

import image_functions as img_funs
from settings import Settings


class Alien(Sprite):
    def __init__(self, ai_settings: Settings,  screen: Surface) -> None:
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = img_funs.load_as_surface('images/alien.png')
        self.rect = self.image.get_rect()

        # Start each new alien near the top-left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact float position
        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.x += (self.ai_settings.alien_speed_factor
                   * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self) -> bool:
        """Return true if the alien is at the edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        else:
            return False
