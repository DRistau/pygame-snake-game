import time
from random import choice, randint
from sys import exit

import pygame
from pygame import locals as L

import constants as C
from objects import Food, FoodController, SpecialFood
from utils import get_randon_position

pygame.init()

# Screen
screen = pygame.display.set_mode((C.W_WIDTH, C.W_HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

font = pygame.font.SysFont('arial', 20, bold=True, italic=True)

# Sound
main_soundtrack = pygame.mixer.music.load("./assets/main_soundtrack.wav")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

eat_sound = pygame.mixer.Sound("./assets/crunch.wav")
fail_sound = pygame.mixer.Sound("./assets/fail.wav")

# Helpers


def game_over(screen):
    fail_sound.play()
    game_over_text = font.render(f"Game Over", True, C.Colors.RED)
    x_pos = (C.W_WIDTH / 2) - (game_over_text.get_width() / 2)
    y_pos = (C.W_HEIGHT / 2) - (game_over_text.get_height() / 2)
    screen.blit(game_over_text, (x_pos, y_pos))


# Game
gaming = True
points = 0
start_time = time.perf_counter()
x = int(C.W_WIDTH / 2)
y = int(C.W_HEIGHT / 2)

speed = C.BLOCK
x_speed = speed
y_speed = 0

snake = [(x, y)]

food_controller = FoodController()

rocks = [
    get_randon_position()
    for i in range(5)
]

while True:
    clock.tick(C.FPS)
    screen.fill(C.Colors.BLACK)

    # write all text
    points_text = font.render(f"points: {points}", True, C.Colors.WHITE)
    time_text = font.render(
        f"time: {int(time.perf_counter() - start_time)}", True, C.Colors.WHITE
    )

    screen.blit(points_text, (20, 10))
    screen.blit(time_text, (20, 40))

    # check events
    for event in pygame.event.get():
        if event.type == L.QUIT:
            pygame.quit()
            exit()

    if not gaming:
        if pygame.key.get_pressed()[L.K_RETURN]:
            gaming = True
            points = 0
            start_time = time.perf_counter()
            x = int(C.W_WIDTH / 2)
            y = int(C.W_HEIGHT / 2)

            speed = C.BLOCK
            x_speed = speed
            y_speed = 0

            snake = [(x, y)]

            food_controller.renew()
        else:
            continue

    # controls
    if pygame.key.get_pressed()[L.K_a] and y_speed:
        x_speed = -speed
        y_speed = 0
    elif pygame.key.get_pressed()[L.K_d] and y_speed:
        x_speed = speed
        y_speed = 0
    elif pygame.key.get_pressed()[L.K_w] and x_speed:
        x_speed = 0
        y_speed = -speed
    elif pygame.key.get_pressed()[L.K_s] and x_speed:
        x_speed = 0
        y_speed = speed

    # update head snake position
    head = (snake[0][0] + x_speed, snake[0][1] + y_speed)
    snake.insert(0, head)

    _head = pygame.draw.rect(
        screen,
        C.Colors.WHITE,
        (*head, C.BLOCK, C.BLOCK)
    )

    if (head[0] < 0 or head[0] > C.W_WIDTH) or (head[1] < 0 or head[1] > C.W_HEIGHT):
        gaming = False
        game_over(screen)

    _food = food_controller.food.update(screen)

    _rocks = [
        pygame.draw.rect(
            screen,
            C.Colors.RED,
            (x, y, C.BLOCK, C.BLOCK)
        )
        for x, y in rocks
    ]

    for _rock in _rocks:
        if _head.colliderect(_rock):
            gaming = False
            game_over(screen)

    if _head.colliderect(_food):
        points += food_controller.food.points
        food_controller.renew()
        eat_sound.play()
    else:
        snake.pop()

    for i, (_x, _y) in enumerate(snake[1:]):
        _body = pygame.draw.rect(
            screen, C.Colors.WHITE, (_x, _y, C.BLOCK, C.BLOCK))
        if i > 1 and _body.colliderect(_head):
            gaming = False
            game_over(screen)

    pygame.display.flip()
