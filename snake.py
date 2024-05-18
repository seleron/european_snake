import pygame
import random
import json
import os

def display_score():
    score_text = font.render("Score: " + str(score), True, white)
    screen.blit(score_text, [screen_width - 150, 10])

def display_maxScore():
    max_score_text = font.render(f"Max Score: {max_score}", True, white)
    screen.blit(max_score_text, [10, 10])
    
def save_max_score(max_score):
    with open('max_score.json', 'w') as f:
        json.dump(max_score, f)

def load_max_score():
    if os.path.exists('max_score.json') and os.path.getsize('max_score.json') > 0:
        with open('max_score.json', 'r') as f:
            return json.load(f)
    else:
        return 0

# Initialize pygame
pygame.init()
# Initialize font for displaying score
font = pygame.font.SysFont(None, 40)
pygame.mixer.init()

# Set up the screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.mixer.music.load("assets/Anthem of Europe.mp3")
pygame.mixer.music.set_volume(0.10) # Set the volume to 50%
pygame.mixer.music.play(-1)
pygame.display.set_caption("Snake Game")

# Load the EU flag with transparent background
eu_flag = pygame.image.load('assets/flag.png').convert_alpha()
eu_flag = pygame.transform.scale(eu_flag, (600, 400))
eu_x = (screen_width - 600) // 2
eu_y = (screen_height - 400) // 2

# Load funny sounds
chomp_sound = pygame.mixer.Sound('assets/chomp.mp3')
bonk_sound = pygame.mixer.Sound('assets/boing.mp3')
splat_sound = pygame.mixer.Sound('assets/splat.mp3')

# Set score
score = 0

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Set up the game clock
clock = pygame.time.Clock()

# Set up the snake properties
snake_block_size = 20
snake_speed = 15

# Load the maximum score
max_score = load_max_score()

# Define direction (initially set to right)
direction = "RIGHT"

# Set up initial position of the snake
snake_list = []
snake_length = 1

# Set up initial position of the food
food_x = round(random.randrange(0, screen_width - snake_block_size) / snake_block_size) * snake_block_size
food_y = round(random.randrange(0, screen_height - snake_block_size) / snake_block_size) * snake_block_size

# Main game loop
game_over = False
game_close = False
snake_x = screen_width / 2
snake_y = screen_height / 2
snake_x_change = 0
snake_y_change = 0
snake_list = []
snake_length = 1

# Function to draw the snake
def draw_snake(snake_block_size, snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, green, [block[0], block[1], snake_block_size, snake_block_size])

while not game_over:
    while game_close:
        # Display game over message
        score = 0
        screen.fill((0, 0, 255))
        screen.blit(eu_flag, (eu_x, eu_y))
        game_over_message = font.render("Game Over! Press Q-Quit or C-Play Again", True, white)
        screen.blit(game_over_message, [screen_width / 6, screen_height / 3])
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.mixer.music.stop()
                game_close = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_over = True
                    pygame.mixer.music.stop()
                    game_close = False
                if event.key == pygame.K_c:
                    # Reset the game
                    snake_x = screen_width / 2
                    snake_y = screen_height / 2
                    snake_x_change = 0
                    snake_y_change = 0
                    snake_list = []
                    snake_length = 1
                    food_x = round(random.randrange(0, screen_width - snake_block_size) / snake_block_size) * snake_block_size
                    food_y = round(random.randrange(0, screen_height - snake_block_size) / snake_block_size) * snake_block_size
                    game_close = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            pygame.mixer.music.stop()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"
            elif event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_q:
                save_max_score(max_score)
                game_over = True
                pygame.mixer.music.stop()

    if direction == "LEFT":
        snake_x_change = -snake_block_size
        snake_y_change = 0
    elif direction == "RIGHT":
        snake_x_change = snake_block_size
        snake_y_change = 0
    elif direction == "UP":
        snake_x_change = 0
        snake_y_change = -snake_block_size
    elif direction == "DOWN":
        snake_x_change = 0
        snake_y_change = snake_block_size

    snake_x += snake_x_change
    snake_y += snake_y_change

    if snake_x >= screen_width or snake_x < 0 or snake_y >= screen_height or snake_y < 0:
        bonk_sound.play()
        game_close = True

    snake_head = [snake_x, snake_y]
    snake_list.append(snake_head)
    if len(snake_list) > snake_length:
        del snake_list[0]

    for segment in snake_list[:-1]:
        if segment == snake_head:
            splat_sound.play()
            game_close = True

    screen.fill((0, 0, 255))
    screen.blit(eu_flag, (eu_x, eu_y))
    pygame.draw.rect(screen, red, [food_x, food_y, snake_block_size, snake_block_size])

    display_score()
    display_maxScore()
    draw_snake(snake_block_size, snake_list)

    pygame.display.update()

    if snake_x == food_x and snake_y == food_y:
        chomp_sound.play()
        food_x = round(random.randrange(0, screen_width - snake_block_size) / snake_block_size) * snake_block_size
        food_y = round(random.randrange(0, screen_height - snake_block_size) / snake_block_size) * snake_block_size
        snake_length += 1
        score += 1
        if score > max_score:
            max_score = score

    clock.tick(snake_speed)

save_max_score(max_score)
pygame.quit()
