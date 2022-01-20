import time
from random import choice, randint
from sys import exit

import pygame
from pygame import locals as L

import constants as C

pygame.init()

# Screen
screen = pygame.display.set_mode((C.W_WIDTH, C.W_HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

font = pygame.font.SysFont('arial', 20, bold=True, italic=True)

# Sound
main_soundtrack = pygame.mixer.music.load("./assets/main_soundtrack.wav")
pygame.mixer.music.play(-1)

eat_sound = pygame.mixer.Sound("./assets/crunch.wav")
fail_sound = pygame.mixer.Sound("./assets/fail.wav")

# Helpers


def random_color():
    return (randint(50, 255), randint(50, 255), randint(50, 255))


def drop_food():
    x_spots = range(0, C.W_WIDTH, C.BLOCK)
    y_spots = range(0, C.W_HEIGHT, C.BLOCK)

    return (
        choice(x_spots),
        choice(y_spots),
    )


def game_over(screen):
    fail_sound.play()
    game_over_text = font.render(f"Game Over", True, C.RED)
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

food = drop_food()

while True:
    clock.tick(C.FPS)
    screen.fill(C.BLACK)

    # write all text
    points_text = font.render(f"points: {points}", True, C.WHITE)
    time_text = font.render(
        f"time: {int(time.perf_counter() - start_time)}", True, C.WHITE
    )

    screen.blit(points_text, (20, 10))
    screen.blit(time_text, (20, 40))

    # check events
    for event in pygame.event.get():
        if event.type == L.QUIT:
            pygame.quit()
            exit()

    if not gaming:
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
        C.WHITE,
        (*head, C.BLOCK, C.BLOCK)
    )

    if (head[0] < 0 or head[0] > C.W_WIDTH) or (head[1] < 0 or head[1] > C.W_HEIGHT):
        gaming = False
        game_over(screen)

    for i, (_x, _y) in enumerate(snake):
        _body = pygame.draw.rect(screen, C.WHITE, (_x, _y, C.BLOCK, C.BLOCK))
        if i > 1 and _body.colliderect(_head):
            gaming = False
            game_over(screen)

    _food = pygame.draw.rect(screen, random_color(), (*food, C.BLOCK, C.BLOCK))

    if _food.colliderect(_head):
        food = drop_food()
        points += 1
        eat_sound.play()
    else:
        snake.pop()

    for i, (_x, _y) in enumerate(snake[1:]):
        _body = pygame.draw.rect(screen, C.WHITE, (_x, _y, C.BLOCK, C.BLOCK))
        if i > 1 and _body.colliderect(_head):
            gaming = False
            game_over(screen)


    pygame.display.flip()
