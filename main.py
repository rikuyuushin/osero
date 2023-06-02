import pygame

WIDTH = 400
HEIGHT = 400
FPS = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
TEXT_COLOR = (255, 255, 255)
EMPTY = 0
BLACK_PIECE = 1
WHITE_PIECE = 2

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def draw_board(board, valid_moves):
    screen.fill(GREEN)
    for row in range(8):
        for col in range(8):
            pygame.draw.rect(screen, GREEN, (col * 50, row * 50, 50, 50))
            if board[row][col] == BLACK_PIECE:
                pygame.draw.circle(screen, BLACK, (col * 50 + 25, row * 50 + 25), 20)
            elif board[row][col] == WHITE_PIECE:
                pygame.draw.circle(screen, WHITE, (col * 50 + 25, row * 50 + 25), 20)

    for move in valid_moves:
        row, col = move
        pygame.draw.circle(screen, (0, 255, 0), (col * 50 + 25, row * 50 + 25), 5)


def initialize_board():
    board = [[EMPTY for _ in range(8)] for _ in range(8)]
    board[3][3] = WHITE_PIECE
    board[3][4] = BLACK_PIECE
    board[4][3] = BLACK_PIECE
    board[4][4] = WHITE_PIECE
    return board


def get_valid_moves(board, player):
    valid_moves = []
    for row in range(8):
        for col in range(8):
            if is_valid_move(board, row, col, player):
                valid_moves.append((row, col))
    return valid_moves


def is_valid_move(board, row, col, player):
    if board[row][col] != EMPTY:
        return False
    other_player = BLACK_PIECE if player == WHITE_PIECE else WHITE_PIECE
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for direction in directions:
        if is_valid_direction(board, row, col, direction, player, other_player):
            return True
    return False


def is_valid_direction(board, row, col, direction, player, other_player):
    dx, dy = direction
    x = row + dx
    y = col + dy
    if x < 0 or x >= 8 or y < 0 or y >= 8 or board[x][y] != other_player:
        return False
    x += dx
    y += dy
    while x >= 0 and x < 8 and y >= 0 and y < 8:
        if board[x][y] == player:
            return True
        elif board[x][y] == EMPTY:
            return False
        x += dx
        y += dy
    return False


def make_move(board, row, col, player):
    board[row][col] = player
    other_player = BLACK_PIECE if player == WHITE_PIECE else WHITE_PIECE
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for direction in directions:
        make_move_direction(board, row, col, direction, player, other_player)


def make_move_direction(board, row, col, direction, player, other_player):
    dx, dy = direction
    x = row + dx
    y = col + dy
    if x < 0 or x >= 8 or y < 0 or y >= 8 or board[x][y] != other_player:
        return
    x += dx
    y += dy
    while x >= 0 and x < 8 and y >= 0 and y < 8:
        if board[x][y] == player:
            while (x - dx) != row or (y - dy) != col:
                x -= dx
                y -= dy
                board[x][y] = player
            return
        elif board[x][y] == EMPTY:
            return
        x += dx
        y += dy


def switch_player(player):
    return BLACK_PIECE if player == WHITE_PIECE else WHITE_PIECE


def get_winner(board):
    black_count = 0
    white_count = 0
    for row in range(8):
        for col in range(8):
            if board[row][col] == BLACK_PIECE:
                black_count += 1
            elif board[row][col] == WHITE_PIECE:
                white_count += 1
    if black_count > white_count:
        return "black win"
    elif black_count < white_count:
        return "white win"
    else:
        return "tie game"


def main():
    running = True
    game_over=False
    player = BLACK_PIECE
    board = initialize_board()

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row = y // 50
                col = x // 50
                if is_valid_move(board, row, col, player):
                    make_move(board, row, col, player)
                    player = switch_player(player)

        valid_moves = get_valid_moves(board, player)

        draw_board(board, valid_moves)

        if len(valid_moves) == 0:
            player = switch_player(player)
            valid_moves = get_valid_moves(board, player)
            if len(valid_moves) == 0:
                running = False
                game_over=True
        draw_board(board,valid_moves)
        pygame.display.flip()
    if game_over:
        winner = get_winner(board)
        display_winner(winner)
        pygame.time.wait(3000)
        running=False
    pygame.quit()
def display_winner(winner):
    font = pygame.font.Font(None, 40)
    text = font.render("Winner: " + winner, True, TEXT_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

if __name__ == '__main__':
    main()






