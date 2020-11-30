import numpy as np
import pygame # for visualizing the game on the screen
import sys
import math


Blue = (0,0,255)
Black = (0,0,0)
Red = (255,0,0)
Yellow = (255,255,0)
Row_count = 6
Column_count = 7


def create_board():
    board = np.zeros((Row_count, Column_count))
    return board


# Now we will create more functions
def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):  # to check whether the user has entered at the right location
    return board[Row_count-1][col] == 0

def get_next_open_row(board, col):
    for r in range(Row_count):
        if board[r][col] == 0:
            return r

def print_board(board):
    # return np.flip(board, 0)
    print(np.flip(board, 0))

def wining_move(board, piece):
    # Check horizontal location for win
    for c in range(Column_count-3):
        for r in range(Row_count):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    # check vertical location for win
    for c in range(Column_count):
        for r in range(Row_count-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    # check for positively sloped diagonals
    for c in range(Column_count-3):
        for r in range(Row_count-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # check for negatively sloped diagonals
    for c in range(Column_count-3):
        for r in range(3, Row_count):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def draw_board(board):
    for c in range(Column_count):
        for r in range(Row_count):
            pygame.draw.rect(screen, Blue, (c*Square_size, r*Square_size+Square_size, Square_size, Square_size))
            pygame.draw.circle(screen, Black, (int(c*Square_size+Square_size/2), int(r*Square_size+Square_size+Square_size/2)), Radius)

    for c in range(Column_count):
        for r in range(Row_count):
            if board[r][c] == 1:
                pygame.draw.circle(screen, Red, (int(c*Square_size+Square_size/2), height-int(r*Square_size+Square_size/2)), Radius)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, Yellow, (int(c*Square_size+Square_size/2), height-int(r*Square_size+Square_size/2)), Radius)
    pygame.display.update()

# board = create_board()
# print(board)

board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init() # we have to initialize the pygame before the game loop starts
Square_size = 100
width = Column_count * Square_size
height = (Row_count+1) * Square_size # Here Row_count has been added by 1 bcz for the upper row for the ball appearing
size = (width, height)

Radius = int(Square_size/2 - 5)

screen = pygame.display.set_mode(size)

draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont('monospace', 75)

while not game_over:

    for event in pygame.event.get(): #As pygame is event based so here we are creating the pygame exit event frm pygame.event.get()
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, Black, (0,0, width, Square_size)) # it is used to avoid the whole red coloring
            pos_x = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, Red, (pos_x, int(Square_size/2)), Radius)
            else:
                pygame.draw.circle(screen, Yellow, (pos_x, int(Square_size/2)), Radius)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, Black, (0,0, width, Square_size))
            # print(event.pos)
            # Ask for player 1 input
            if turn == 0:
                pos_x = event.pos[0]
                col = int(math.floor(pos_x/Square_size)) # this is basically to get the values which lies btw 100-700
                                                      # for x in first row circles floor for max value, int to convert it
                # selection = int(input('Player 1 make your Selection (0-6):'))
                # col = int(input('Player 1 make your Selection (0-6):')) # These are basically the columns

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                # print(selection)
                # print(type(selection))
                    if wining_move(board, 1):
                        label = myfont.render('Player 1 wins!!', 1, Red)
                        screen.blit(label, (40,10))
                        # print('Player 1 wins !!!! Congrats')
                        game_over = True



             # Ask for player 2 input
            else:
                # selection = int(input('Player 2 make your Selection (0-6):'))
                pos_x = event.pos[0]
                col = int(math.floor(pos_x / Square_size))
                # col = int(input('Player 2 make your Selection (0-6):'))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if wining_move(board, 2):   # Here 2 is for player 2
                        label = myfont.render('Player 2 wins!!', 2, Yellow)
                        screen.blit(label, (40, 10))
                        # print('Player 2 wins !!!! Congrats')
                        game_over = True
                        # break
            # print(print_board(board))
            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2  #means it will return the remainder basically after dividing by 2

            if game_over:
                pygame.time.wait(3000)   # after one player win the match the screen will disappear after 3000 milliseconds