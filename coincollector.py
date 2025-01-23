import pygame
import sys
import random
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
HEADER_HEIGHT = 100  
WINDOW_HEIGHT = SCREEN_HEIGHT + HEADER_HEIGHT
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
screen = pygame.display.set_mode((SCREEN_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Multiplayer Coin Collector with Fixed Vertical Hurdles")
clock = pygame.time.Clock()
player1_size = 50
player2_size = 50
player1_pos = [SCREEN_WIDTH - player1_size, HEADER_HEIGHT] 
player2_pos = [0, SCREEN_HEIGHT + HEADER_HEIGHT - player2_size]
player_speed = 5
coin_size = 30
hurdle_positions = [
    [100, HEADER_HEIGHT + 50], [300, HEADER_HEIGHT + 100], [500, HEADER_HEIGHT + 150], [700, HEADER_HEIGHT + 200],
    [200, HEADER_HEIGHT + 250], [400, HEADER_HEIGHT + 300], [600, HEADER_HEIGHT + 350], [100, HEADER_HEIGHT + 400],
    [300, HEADER_HEIGHT + 450], [500, HEADER_HEIGHT + 500]
]
hurdle_width = 20
hurdle_height = 100
player1_score = 0
player2_score = 0
font = pygame.font.Font(None, 36)
game_time = 100 
start_ticks = pygame.time.get_ticks()


def draw_player(position: list, color, size):
    """Draw the player as a colored rectangle."""
    pygame.draw.rect(screen, color, (position[0], position[1], size, size))


def draw_coin(position):
    """Draw the coin as a yellow circle."""
    pygame.draw.circle(screen, YELLOW, (position[0] + coin_size // 2, position[1] + coin_size // 2), coin_size // 2)


def draw_hurdle(position):
    """Draw a vertical rectangular hurdle."""
    pygame.draw.rect(screen, ORANGE, (position[0], position[1], hurdle_width, hurdle_height))


def display_message(message, color, size, y_offset):
    """Display a message in the center of the screen with vertical offset."""
    message_font = pygame.font.Font(None, size)
    text = message_font.render(message, True, color)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)


def check_collision(player_rect, hurdles):
    """Check if the player collides with any hurdle."""
    for hurdle in hurdles:
        hurdle_rect = pygame.Rect(hurdle[0], hurdle[1], hurdle_width, hurdle_height)
        if player_rect.colliderect(hurdle_rect):
            return True
    return False


def check_collision_direction(player_rect, hurdles, direction):
    """Check for collisions based on movement direction."""
    temp_rect = player_rect.copy()
    if direction == "up":
        temp_rect.y -= player_speed
    elif direction == "down":
        temp_rect.y += player_speed
    elif direction == "left":
        temp_rect.x -= player_speed
    elif direction == "right":
        temp_rect.x += player_speed

    return check_collision(temp_rect, hurdles)


def generate_coin_position():
    """Generate a new position for the coin that doesn't overlap with any hurdles."""
    while True:
        coin_pos = [
            random.randint(0, SCREEN_WIDTH - coin_size),
            random.randint(HEADER_HEIGHT, WINDOW_HEIGHT - coin_size)
        ]
        coin_rect = pygame.Rect(coin_pos[0], coin_pos[1], coin_size, coin_size)
        if not check_collision(coin_rect, hurdle_positions):
            return coin_pos
coin_pos = generate_coin_position()
running = True
while running:
    screen.fill(GREEN)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    seconds_left = game_time - (pygame.time.get_ticks() - start_ticks) // 1000
    if seconds_left <= 0:
        screen.fill(GREEN)
        winner = "Player 1 Wins!" if player1_score > player2_score else "Player 2 Wins!"
        if player1_score == player2_score:
            winner = "It's a Tie!"
        display_message(f"Game Over! {winner}", WHITE, 50, -50)
        display_message(f"Scores - Player 1: {player1_score}, Player 2: {player2_score}", WHITE, 40, 50)
        running = False
        break
    keys = pygame.key.get_pressed()
    player1_rect = pygame.Rect(player1_pos[0], player1_pos[1], player1_size, player1_size)
    if keys[pygame.K_w] and player1_pos[1] > HEADER_HEIGHT and not check_collision_direction(player1_rect, hurdle_positions, "up"):
        player1_pos[1] -= player_speed
    if keys[pygame.K_s] and player1_pos[1] < WINDOW_HEIGHT - player1_size and not check_collision_direction(player1_rect, hurdle_positions, "down"):
        player1_pos[1] += player_speed
    if keys[pygame.K_a] and player1_pos[0] > 0 and not check_collision_direction(player1_rect, hurdle_positions, "left"):
        player1_pos[0] -= player_speed
    if keys[pygame.K_d] and player1_pos[0] < SCREEN_WIDTH - player1_size and not check_collision_direction(player1_rect, hurdle_positions, "right"):
        player1_pos[0] += player_speed
    player2_rect = pygame.Rect(player2_pos[0], player2_pos[1], player2_size, player2_size)
    if keys[pygame.K_UP] and player2_pos[1] > HEADER_HEIGHT and not check_collision_direction(player2_rect, hurdle_positions, "up"):
        player2_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player2_pos[1] < WINDOW_HEIGHT - player2_size and not check_collision_direction(player2_rect, hurdle_positions, "down"):
        player2_pos[1] += player_speed
    if keys[pygame.K_LEFT] and player2_pos[0] > 0 and not check_collision_direction(player2_rect, hurdle_positions, "left"):
        player2_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player2_pos[0] < SCREEN_WIDTH - player2_size and not check_collision_direction(player2_rect, hurdle_positions, "right"):
        player2_pos[0] += player_speed
    coin_rect = pygame.Rect(coin_pos[0], coin_pos[1], coin_size, coin_size)
    if player1_rect.colliderect(coin_rect):
        player1_score += 1
        coin_pos = generate_coin_position()
    if player2_rect.colliderect(coin_rect):
        player2_score += 1
        coin_pos = generate_coin_position()
    draw_player(player1_pos, RED, player1_size)
    draw_player(player2_pos, BLUE, player2_size)
    draw_coin(coin_pos)
    for hurdle in hurdle_positions:
        draw_hurdle(hurdle)
    pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, HEADER_HEIGHT))  
    player1_score_text = font.render(f"Player 1 Score: {player1_score}", True, BLACK)
    player2_score_text = font.render(f"Player 2 Score: {player2_score}", True, BLACK)
    timer_text = font.render(f"Time Left: {seconds_left}s", True, BLACK)
    screen.blit(player1_score_text, (10, 10))
    screen.blit(player2_score_text, (SCREEN_WIDTH - 220, 10))
    screen.blit(timer_text, (SCREEN_WIDTH // 2 - 50, 10))
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
sys.exit()
