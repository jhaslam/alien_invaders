import pygame
import pygame.draw
from pygame.sprite import Sprite
from pygame.surface import Surface

from settings import Settings
from ship import Ship


class Bullet(Sprite):
    def __init__(self, ai_settings: Settings,
                 screen: Surface, ship: Ship) -> None:
        super(Bullet, self).__init__()
        self.screen = screen

        self.rect = pygame.Rect(
            0, 0,
            ai_settings.bullet_width,
            ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store position separately as a float value
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self) -> None:
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self) -> None:
        pygame.draw.rect(self.screen, self.color, self.rect)
