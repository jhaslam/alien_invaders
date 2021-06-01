import pygame
import pygame.transform
from pygame.surface import Surface


def load_as_surface(filename: str) -> Surface:
    """
    Optimization: Blitting an image to the surface is much slower than
    blitting a surface to a surface, therefore pre-draw all images you
    plan on using onto their own surfaces.
    """
    image = pygame.image.load(filename)
    rect = image.get_rect()
    surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))
    surface.blit(image, rect)
    return surface


def resize(image: Surface, new_height: int) -> Surface:
    old_width = image.get_width()
    old_height = image.get_height()
    new_width = int(old_width * (new_height / old_height))
    return pygame.transform.scale(image, (new_width, new_height))
