import sys
import os
import time
import pygame

from bullet import Bullet
from alien import Alien
from stats import GameStats



def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True # Переместить корабль вправо
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True # Переместить корабль влево
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets):
    # Создание новой пули и включение её в группу bullets
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        # сброс игровой статистики
        stats.reset_stats()
        stats.game_active = True

        # Сбросить динамические настройки на начальные значения
        ai_settings.initialize_dynamic_settings()

        # очистка списков пришельцев и пуль
        aliens.empty()
        bullets.empty()

        # создание нового флота и размещение корабля в центре
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button):
    # При каждом проходе цикла перерисовывается экран
    screen.fill(ai_settings.bg_color)

    # Все пули выводятся позади изображений корабля пришельцев
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()

    aliens.draw(screen)

    # Кнопка Play отображается в том случае, если игра неактивна
    if not stats.game_active:
        play_button.draw_button()

    # Отрисовка статистики
    draw_stats(ai_settings, screen, stats)

    # Отображение последнего прорисованного экрана
    pygame.display.flip()


def draw_stats(ai_settings, screen, stats):
    font = pygame.font.SysFont(None, 48)

    # Жизни (Ships Left)
    lives_text = font.render(f"Корабли: {stats.ships_left}", True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))

    # Отображаем уровень
    level_text = font.render(f"Уровень: {stats.level}", True, (255, 255, 255))
    screen.blit(level_text, (ai_settings.screen_width - level_text.get_width() - 10, 10))  # В правом верхнем углу

    # Текущий счёт (Current Score)
    score_text = font.render(f"Счёт: {stats.score}", True, (255, 255, 255))
    score_rect = score_text.get_rect()
    score_rect.topright = (ai_settings.screen_width - 10, 60)  # В правом верхнем углу
    screen.blit(score_text, score_rect)


def update_bullets(ai_settings, screen, stats, ship, aliens, bullets):

    bullets.update()

    # Удалить пули, вышедшие за пределы экрана
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    # Проверить попадания
    check_bullet_alien_collisions(ai_settings, screen, stats, ship, aliens, bullets)

    # Проверить, уничтожен ли весь флот
    check_fleet_cleared(ai_settings, stats, screen, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, ship, aliens, bullets):
    # Проверка попаданий пуль по инопланетянам
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)


    if not aliens:
        bullets.empty()
        ai_settings.increase_speed()  # Увеличение скорости инопланетян и корабля
        stats.level += 1  # Увеличение уровня
        create_fleet(ai_settings, screen, ship, aliens) # Создаем новый флот пришельцев



def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    availible_space_y = (ai_settings.screen_height -
                       (3 * alien_height) - ship_height)
    number_rows = int(availible_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # создание флота пришельцев
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen,
                         aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):

    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()


    # Проверка столкновений "пришелец - корабль"
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    # Проверка, добрались ли пришельцы до нижнего края
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            if stats.shield_active:
                # Уничтожить пришельца, если щит активен
                aliens.remove(alien)
            else:
                # Обработка столкновения при отсутствии щита
                ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
                break


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    if stats.ships_left > 0:
        # Уменьшение количества оставшихся кораблей
        stats.ships_left -= 1

        # Очистка списка пришельцев и пуль
        aliens.empty()
        bullets.empty()

        # Создание нового флота и размещение корабля в центре
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Пауза
        time.sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_fleet_cleared(ai_settings, stats, screen, ship, aliens, bullets):
    if not aliens:
        bullets.empty() # Очистить оставшиеся пули
        level_up(stats) # Увеличить уровень через функцию level_up
        create_fleet(ai_settings, screen, ship, aliens) # Создать новый флот

def level_up(stats):
    stats.ai_settings.increase_speed()
    stats.level += 1


# Функция для получения пути к ресурсу
def resource_path(relative_path):
    """Определяет абсолютный путь к ресурсу, независимо от того, где запущен файл."""

    base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
