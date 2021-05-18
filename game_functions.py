import sys
from time import sleep

import pygame
import pygame.sprite
from pygame.event import Event
from pygame.sprite import Group
from pygame.surface import Surface

from alien import Alien
from bullet import Bullet
from settings import Settings
from ship import Ship
from game_stats import GameStats


def check_events(ai_settings: Settings, stats: GameStats, screen: Surface,
                 ship: Ship, bullets: Group) -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, stats, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_keydown_events(event: Event, 
                         ai_settings: Settings, stats: GameStats,
                         screen: Surface, ship: Ship,
                         bullets: Group) -> None:
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_p:
        stats.game_paused = not stats.game_paused
    elif event.key == pygame.K_q:
        sys.exit()


def load_as_surface(filename: str) -> Surface:
    """
    Optimization: Blitting an image to the surface is much slower than
    blitting a surface to a surface, therefore pre-draw all images you
    plan on using onto their own surfaces.
    """
    image =  pygame.image.load(filename)
    rect = image.get_rect()
    surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    surface.fill((0,0,0,0))
    surface.blit(image,rect)
    return surface


def fire_bullet(ai_settings: Settings, screen: Surface,
                ship: Ship, bullets: Group) -> None:
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event: Event, ship: Ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(ai_settings: Settings, screen: Surface,
                  ship: Ship, aliens: Group, bullets: Group) -> None:
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    pygame.display.flip()


def update_bullets(ai_settings: Settings, screen: Surface,
                   ship: Ship, aliens: Group, bullets: Group) -> None:
    """Update bullet positions"""
    bullets.update()

    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)

    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    check_bullet_alien_collisions(aliens, bullets)


def check_bullet_alien_collisions(aliens: Group, bullets: Group) -> None:
    """
    Check for any bullets that have hit aliens.
    When so, get rid of both bullet an alien
    """
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)


def check_aliens_bottom(ai_settings: Settings, stats: GameStats, 
                        screen: Surface, ship: Ship, aliens: Group,
                        bullets: Group) -> None:
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break
    

def get_number_aliens_x(ai_settings: Settings, alien_width: int) -> int:
    """Determine the number of aliens that fit in a row"""
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings: Settings, ship_height: int, 
                    alien_height: int) -> int:
    available_space_y = (ai_settings.screen_height 
                         - (3 * alien_height)
                         - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings: Settings, screen: Surface, aliens: Group,
                 alien_number: int, row_number: int) -> None:
    """Create an alien and place it"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + (2 * alien_width * alien_number)
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + (2 * alien.rect.height * row_number)
    aliens.add(alien)


def create_fleet(ai_settings: Settings, screen: Surface,
                 ship: Ship, aliens: Group) -> None:
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings, 
        ship.rect.height, alien.rect.height)

    # Create a fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, 
                alien_number, row_number)


def check_fleet_edges(ai_settings: Settings, aliens: Group) -> None:
    """Respond if any aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings: Settings, aliens: Group) -> None:
    """Drop the entire fleed and change the fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings: Settings, stats: GameStats, screen: Surface,
                ship: Ship, aliens: Group, bullets: Group) -> None:
    """
    Check if a fleet is at an edge.
    Update the positions of all aliens in the fleet.
    Check for alien-ship collisions
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def ship_hit(ai_settings: Settings, stats: GameStats, screen: Surface,
                ship: Ship, aliens: Group, bullets: Group) -> None:
    """Respond to a ship being hit by an alien"""
    stats.ships_left -= 1
    if stats.ships_left > 0:
        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)

    else:
        stats.game_active =  False
