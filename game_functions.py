import sys
from time import sleep

import pygame
import pygame.mouse
import pygame.sprite
from pygame.event import Event
from pygame.sprite import Group
from pygame.surface import Surface

from alien import Alien
from bullet import Bullet
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship


def check_events(ai_settings: Settings, stats: GameStats,
                 scoreboard: Scoreboard, screen: Surface, play_button: Button,
                 ship: Ship, aliens: Group, bullets: Group) -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, stats, screen,
                                 scoreboard, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, scoreboard,
                              play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings: Settings, screen: Surface, stats: GameStats,
                      scoreboard: Scoreboard, play_button: Button,
                      ship: Ship, aliens: Group, bullets: Group,
                      mouse_x: int, mouse_y: int) -> None:
    """Start a new game when the player clicks Play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        reset_game(ai_settings, screen, stats,
                   scoreboard, ship, aliens, bullets)


def reset_game(ai_settings: Settings, screen: Surface, stats: GameStats,
               scoreboard: Scoreboard, ship: Ship, aliens: Group,
               bullets: Group) -> None:
    if not stats.game_active:
        # Reset the game statistics
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images
        scoreboard.reset()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)

        stats.game_active = True


def check_keydown_events(event: Event,
                         ai_settings: Settings, stats: GameStats,
                         screen: Surface, scoreboard: Scoreboard,
                         ship: Ship, aliens: Group, bullets: Group) -> None:
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        if stats.game_active:
            fire_bullet(ai_settings, screen, ship, bullets)
        else:
            reset_game(ai_settings, screen, stats, scoreboard,
                       ship, aliens, bullets)
    elif event.key == pygame.K_p:
        stats.game_paused = not stats.game_paused
    elif event.key == pygame.K_q:
        sys.exit()


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
                  stats: GameStats, scoreboard: Scoreboard,
                  ship: Ship, aliens: Group, bullets:
                  Group, play_button: Button) -> None:
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    scoreboard.show_score()

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()


def update_bullets(ai_settings: Settings, screen: Surface,
                   stats: GameStats, scoreboard: Scoreboard,
                   ship: Ship, aliens: Group, bullets: Group) -> None:
    """Update bullet positions"""
    bullets.update()
    check_bullet_alien_collisions(ai_settings, screen, stats, scoreboard,
                                  ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings: Settings, screen: Surface,
                                  stats: GameStats, scoreboard: Scoreboard,
                                  ship: Ship, aliens: Group,
                                  bullets: Group) -> None:
    """
    Check for any bullets that have hit aliens.
    When so, get rid of both bullet an alien
    """
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points
        scoreboard.prep_score()
        check_high_score(stats, scoreboard)

    if len(aliens) == 0:
        # If the entire alien fleet is destroyed start a new level
        bullets.empty()
        ai_settings.increase_speed()

        stats.level += 1
        scoreboard.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def check_high_score(stats: GameStats, scoreboard: Scoreboard) -> None:
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()


def check_aliens_bottom(ai_settings: Settings, screen: Surface,
                        stats: GameStats, scoreboard: Scoreboard,
                        ship: Ship, aliens: Group, bullets: Group) -> None:
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, scoreboard,
                     ship, aliens, bullets)
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


def update_aliens(ai_settings: Settings, screen: Surface, stats: GameStats,
                  scoreboard: Scoreboard, ship: Ship, aliens: Group,
                  bullets: Group) -> None:
    """
    Check if a fleet is at an edge.
    Update the positions of all aliens in the fleet.
    Check for alien-ship collisions
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, scoreboard,
                 ship, aliens, bullets)
    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, screen, stats, scoreboard, ship,
                        aliens, bullets)


def ship_hit(ai_settings: Settings, screen: Surface, stats: GameStats,
             scoreboard: Scoreboard, ship: Ship, aliens: Group,
             bullets: Group) -> None:
    """Respond to a ship being hit by an alien"""
    stats.ships_left -= 1
    scoreboard.prep_ships_left()

    if stats.ships_left > 0:
        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
