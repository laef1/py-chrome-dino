import pygame
import random

pygame.init()

screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Chrome Dino Game Bot")

block_width = 30
block_height = 40
block_x = 100
block_y = screen_height - block_height - 10

JUMP_HEIGHT = 15
GRAVITY = 1.5
TERMINAL_VELOCITY = 20
DUCK_HEIGHT = 20
GROUND_LEVEL = screen_height - 10
OBSTACLE_WIDTH = 23
OBSTACLE_HEIGHT = 30
OBSTACLE_SPEED = 5

vertical_velocity = 0
original_block_height = block_height
is_jumping = False
is_ducking = False
jumped = False
ducked = False
score = 0
health = 3

red_objects = []
new_generation_objects = []

font = pygame.font.Font(None, 36)


def detect_obstacles():
    global is_jumping, is_ducking, vertical_velocity, block_height, block_y, health
    for obstacle in red_objects:
        if (
            obstacle["x"] < block_x + block_width + 40
            and obstacle["x"] + OBSTACLE_WIDTH > block_x
        ):
            if not is_jumping:
                is_jumping = True
                vertical_velocity = -JUMP_HEIGHT
            if (
                block_x < obstacle["x"] + OBSTACLE_WIDTH
                and block_x + block_width > obstacle["x"]
                and block_y < obstacle["y"] + OBSTACLE_HEIGHT
                and block_y + block_height > obstacle["y"]
            ):
                health -= 1
                red_objects.remove(obstacle)
                if health <= 0:
                    pygame.quit()
                    exit()

    for obstacle in new_generation_objects:
        if (
            obstacle["x"] < block_x + block_width + 40
            and obstacle["x"] + OBSTACLE_WIDTH > block_x
        ):
            if not is_ducking:
                is_ducking = True
                block_height = DUCK_HEIGHT
                block_y = GROUND_LEVEL - DUCK_HEIGHT
            if (
                block_x < obstacle["x"] + OBSTACLE_WIDTH
                and block_x + block_width > obstacle["x"]
                and block_y < obstacle["y"] + OBSTACLE_HEIGHT
                and block_y + block_height > obstacle["y"]
            ):
                health -= 1
                new_generation_objects.remove(obstacle)
                if health <= 0:
                    pygame.quit()
                    exit()


def spawn_obstacle():
    obstacle_x = screen_width
    obstacle_y = GROUND_LEVEL - OBSTACLE_HEIGHT
    red_objects.append({"x": obstacle_x, "y": obstacle_y})


def spawn_new_generation_obstacle():
    obstacle_x = screen_width
    obstacle_y = GROUND_LEVEL - OBSTACLE_HEIGHT - 102.5 
    new_generation_objects.append({"x": obstacle_x, "y": obstacle_y})


running = True
clock = pygame.time.Clock()
obstacle_timer = 0
new_generation_timer = 0
obstacle_interval = 1500
new_generation_interval = 3000

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    detect_obstacles()

    if is_jumping:
        block_y += vertical_velocity
        vertical_velocity += GRAVITY
        if block_y >= GROUND_LEVEL - block_height:
            block_y = GROUND_LEVEL - block_height
            is_jumping = False
            vertical_velocity = 0
    elif is_ducking:
        block_height = original_block_height
        block_y = GROUND_LEVEL - block_height
        is_ducking = False

    if pygame.time.get_ticks() - obstacle_timer > obstacle_interval:
        spawn_obstacle()
        obstacle_timer = pygame.time.get_ticks()

    if pygame.time.get_ticks() - new_generation_timer > new_generation_interval:
        spawn_new_generation_obstacle()
        new_generation_timer = pygame.time.get_ticks()

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), (block_x, block_y, block_width, block_height))
    for obstacle in red_objects:
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (obstacle["x"], obstacle["y"], OBSTACLE_WIDTH, OBSTACLE_HEIGHT),
        )
        obstacle["x"] -= OBSTACLE_SPEED
        if obstacle["x"] < -OBSTACLE_WIDTH:
            red_objects.remove(obstacle)
            score += 1

    for obstacle in new_generation_objects:
        pygame.draw.rect(
            screen,
            (0, 0, 255),
            (obstacle["x"], obstacle["y"], OBSTACLE_WIDTH, OBSTACLE_HEIGHT),
        )
        obstacle["x"] -= OBSTACLE_SPEED
        if obstacle["x"] < -OBSTACLE_WIDTH:
            new_generation_objects.remove(obstacle)
            score += 1

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    health_text = font.render(f"Health: {health}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 50))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
