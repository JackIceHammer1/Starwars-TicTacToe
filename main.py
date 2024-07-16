import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)
WHITE = (255, 255, 255)

# Load Sounds
x_sound = pygame.mixer.Sound('x_sound.wav')
o_sound = pygame.mixer.Sound('o_sound.wav')

# Load Background Image
background_image = pygame.image.load('star_wars_background.jpg')

# Load Font
font = pygame.font.Font('Starjedi.ttf', 40)

# Initialize Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Star Wars Tic-Tac-Toe')

# Board
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Draw Lines
def draw_lines():
    screen.blit(background_image, (0, 0))
    # Horizontal
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), 15)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), 15)
    # Vertical
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), 15)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), 15)

# Animate Move
def animate_move(row, col, player):
    start_time = time.time()
    duration = 0.5  # Animation duration in seconds
    initial_scale = 0.1
    final_scale = 1.0

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            break

        scale = initial_scale + (final_scale - initial_scale) * (elapsed_time / duration)
        screen.blit(background_image, (0, 0))
        draw_lines()
        draw_figures(exclude=(row, col))

        center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        size = int(60 * scale)

        if player == 'X':
            draw_scaled_cross(center_x, center_y, size)
        elif player == 'O':
            pygame.draw.circle(screen, CIRCLE_COLOR, (center_x, center_y), size, 15)

        pygame.display.update()

    if player == 'X':
        x_sound.play()
    else:
        o_sound.play()

# Draw Scaled Cross
def draw_scaled_cross(center_x, center_y, size):
    half_size = size // 2
    pygame.draw.line(screen, CROSS_COLOR, (center_x - half_size, center_y - half_size),
                     (center_x + half_size, center_y + half_size), 15)
    pygame.draw.line(screen, CROSS_COLOR, (center_x - half_size, center_y + half_size),
                     (center_x + half_size, center_y - half_size), 15)

# Draw Figures
def draw_figures(exclude=None):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if (row, col) == exclude:
                continue
            if board[row][col] == 'X':
                draw_scaled_cross(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2, 60)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, 
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 60, 15)

# Check Win
def check_win(player):
    # Vertical Win Check
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] == player:
            animate_winning_line('vertical', col, player)
            return True

    # Horizontal Win Check
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] == player:
            animate_winning_line('horizontal', row, player)
            return True

    # Ascending Diagonal Win Check
    if board[2][0] == board[1][1] == board[0][2] == player:
        animate_winning_line('asc_diagonal', None, player)
        return True

    # Descending Diagonal Win Check
    if board[0][0] == board[1][1] == board[2][2] == player:
        animate_winning_line('desc_diagonal', None, player)
        return True

    return False

# Animate Winning Line
def animate_winning_line(direction, index, player):
    start_time = time.time()
    duration = 1.0  # Animation duration in seconds
    color = CIRCLE_COLOR if player == 'O' else CROSS_COLOR

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            break

        progress = elapsed_time / duration
        screen.blit(background_image, (0, 0))
        draw_lines()
        draw_figures()

        if direction == 'vertical':
            posX = index * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.line(screen, color, (posX, 15), (posX, int(HEIGHT * progress)), 15)
        elif direction == 'horizontal':
            posY = index * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.line(screen, color, (15, posY), (int(WIDTH * progress), posY), 15)
        elif direction == 'asc_diagonal':
            pygame.draw.line(screen, color, (15, HEIGHT - 15), 
                             (int(WIDTH * progress), HEIGHT - int(HEIGHT * progress)), 15)
        elif direction == 'desc_diagonal':
            pygame.draw.line(screen, color, (15, 15), (int(WIDTH * progress), int(HEIGHT * progress)), 15)

        pygame.display.update()

# Reset Board
def reset_board():
    start_time = time.time()
    duration = 0.5  # Animation duration in seconds

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            break

        progress = elapsed_time / duration
        screen.fill(BG_COLOR)
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col]:
                    center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                    center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                    size = int(60 * (1 - progress))
                    if board[row][col] == 'X':
                        draw_scaled_cross(center_x, center_y, size)
                    elif board[row][col] == 'O':
                        pygame.draw.circle(screen, CIRCLE_COLOR, (center_x, center_y), size, 15)
        pygame.display.update()

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = None

# AI Move using Minimax Algorithm
def ai_move():
    best_score = -float('inf')
    best_move = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                board[row][col] = 'O'
                score = minimax(board, False)
                board[row][col] = None
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    if best_move:
        board[best_move[0]][best_move[1]] = 'O'
        animate_move(best_move[0], best_move[1], 'O')

def minimax(board, is_maximizing):
    if check_win('O'):
        return 1
    if check_win('X'):
        return -1
    if all(board[row][col] is not None for row in range(BOARD_ROWS) for col in range(BOARD_COLS)):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] is None:
                    board[row][col] = 'O'
                    score = minimax(board, False)
                    board[row][col] = None
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] is None:
                    board[row][col] = 'X'
                    score = minimax(board, True)
                    board[row][col] = None
                    best_score = min(score, best_score)
        return best_score

# Main Loop
player = 'X'
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if board[clicked_row][clicked_col] is None:
                board[clicked_row][clicked_col] = player
                animate_move(clicked_row, clicked_col, player)
                if check_win(player):
                    game_over = True
                player = 'O' if player == 'X' else 'X'
                if player == 'O' and not game_over:
                    ai_move()
                    if check_win('O'):
                        game_over = True
                    player = 'X'

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_board()
                player = 'X'
                game_over = False

    screen.blit(background_image, (0, 0))
    draw_lines()
    draw_figures()
    pygame.display.update()
