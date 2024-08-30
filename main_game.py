import pygame
import random

pygame.init()

# Set up the game window
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Chrome Dino Game")

# Set up the block
block_width = 30
block_height = 55
block_x = 100
block_y = screen_height - block_height - 10

# Constants
JUMP_HEIGHT = 15
GRAVITY = 1.5
TERMINAL_VELOCITY = 20
DUCK_HEIGHT = 20
HP = 3
GROUND_LEVEL = screen_height - 10
OBSTACLE_WIDTH = 23
OBSTACLE_HEIGHT = 30
OBSTACLE_SPEED = 5

# Initialize variables
vertical_velocity = 0
original_block_height = block_height
is_jumping = False
is_ducking = False
jumped = False
ducked = False
score = 0

# Red objects (obstacles)
red_objects = []

# Game loop
running = True
clock = pygame.time.Clock()

def reset_game():
    global block_y, vertical_velocity, is_jumping, is_ducking, jumped, ducked, score, HP, red_objects
    block_y = screen_height - block_height - 10
    vertical_velocity = 0
    is_jumping = False
    is_ducking = False
    jumped = False
    ducked = False
    score = 0
    HP = 3
    red_objects = []

reset_game()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_w or event.key == pygame.K_SPACE) and not jumped and block_y == GROUND_LEVEL - block_height:
                is_jumping = True
                jumped = True
                vertical_velocity = -JUMP_HEIGHT
            elif (event.key == pygame.K_s or event.key == pygame.K_LSHIFT) and not ducked:
                is_ducking = True
                ducked = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                is_jumping = False
                jumped = False
            elif event.key == pygame.K_s or event.key == pygame.K_LSHIFT:
                is_ducking = False
                ducked = False
        elif event.type == pygame.MOUSEBUTTONDOWN and HP <= 0:
            mouse_x, mouse_y = event.pos
            if start_button.collidepoint(mouse_x, mouse_y):
                reset_game()

    if HP > 0:
        # Update game logic
        if is_jumping or block_y < GROUND_LEVEL - block_height:
            block_y += vertical_velocity
            vertical_velocity += GRAVITY
            if vertical_velocity > TERMINAL_VELOCITY:
                vertical_velocity = TERMINAL_VELOCITY
            if block_y > GROUND_LEVEL - block_height:  # Prevent falling below ground
                block_y = GROUND_LEVEL - block_height
                vertical_velocity = 0
                is_jumping = False
        else:
            if block_y < GROUND_LEVEL - block_height:
                block_y += GRAVITY
                if block_y > GROUND_LEVEL - block_height:
                    block_y = GROUND_LEVEL - block_height

        if is_ducking:
            block_height = DUCK_HEIGHT
        else:
            block_height = original_block_height

        # Move obstacles
        for obj in red_objects:
            obj.x -= OBSTACLE_SPEED
            if obj.x < -OBSTACLE_WIDTH:
                red_objects.remove(obj)
                score += 1

        # Generate new obstacles
        if len(red_objects) == 0 or red_objects[-1].x < screen_width - random.randint(150, 300):
            if score > 200 and random.random() < 0.5:  # 50% chance to generate stacked blocks
                new_obstacle1 = pygame.Rect(screen_width, GROUND_LEVEL - OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
                new_obstacle2 = pygame.Rect(screen_width, GROUND_LEVEL - 2 * OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
                red_objects.append(new_obstacle1)
                red_objects.append(new_obstacle2)
            else:
                new_obstacle = pygame.Rect(screen_width, GROUND_LEVEL - OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
                red_objects.append(new_obstacle)

        # Check for collisions with red objects
        block_rect = pygame.Rect(block_x, block_y, block_width, block_height)
        for obj in red_objects:
            if block_rect.colliderect(obj):
                HP -= 1
                red_objects.remove(obj)
                if HP <= 0:
                    break

    # Clear screen
    screen.fill((255, 255, 255))  # Fill the screen with white

    # Draw ground
    pygame.draw.line(screen, (0, 0, 0), (0, GROUND_LEVEL), (screen_width, GROUND_LEVEL), 2)

    # Draw red objects (obstacles)
    for obj in red_objects:
        pygame.draw.rect(screen, (255, 0, 0), obj)

    # Draw block (character)
    pygame.draw.rect(screen, (0, 0, 255), (block_x, block_y, block_width, block_height))

    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Draw health
    health_text = font.render(f"Health: {HP}", True, (0, 0, 0))
    screen.blit(health_text, (10, 50))

    if HP <= 0:
        # Draw Game Over text
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (screen_width // 2 - 80, screen_height // 2 - 50))

        # Draw Start Over button
        start_button = pygame.Rect(screen_width // 2 - 50, screen_height // 2, 100, 50)
        pygame.draw.rect(screen, (0, 255, 0), start_button)
        start_text = font.render("Start Over", True, (0, 0, 0))
        screen.blit(start_text, (screen_width // 2 - 45, screen_height // 2 + 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

# Quit the game
pygame.quit()