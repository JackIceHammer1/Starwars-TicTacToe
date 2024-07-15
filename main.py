import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)

# Initialize Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Star Wars Tic-Tac-Toe')

# Board
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Draw Lines
def draw_lines():
    screen.fill(BG_COLOR)
    # Horizontal
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), 15)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), 15)
    # Vertical
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), 15)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), 15)

# Draw Figures
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, (84, 84, 84), (col * SQUARE_SIZE + 50, row * SQUARE_SIZE + 50),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - 50, row * SQUARE_SIZE + SQUARE_SIZE - 50), 15)
                pygame.draw.line(screen, (84, 84, 84), (col * SQUARE_SIZE + 50, row * SQUARE_SIZE + SQUARE_SIZE - 50),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - 50, row * SQUARE_SIZE + 50), 15)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, (239, 231, 200), 
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 60, 15)

# Check Win
def check_win(player):
    # Vertical Win Check
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True

    # Horizontal Win Check
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True

    # Ascending Diagonal Win Check
    if board[2][0] == board[1][1] == board[0][2] == player:
        return True

    # Descending Diagonal Win Check
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True

    return False

# Main Loop
player = 'X'
game_over = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]  # x
            mouseY = event.pos[1]  # y

            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if board[clicked_row][clicked_col] is None:
                board[clicked_row][clicked_col] = player
                if check_win(player):
                    game_over = True
                player = 'O' if player == 'X' else 'X'

    draw_lines()
    draw_figures()
    pygame.display.update()
