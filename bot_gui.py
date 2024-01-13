import pygame
pygame.init()

HEIGHT, WIDTH = 700, 700
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (227, 75, 75)
BLUE = (71, 132, 237)
GREEN = (37, 176, 51)
LINE_WIDTH = 10
BOARD_WIDTH = 500
XO_FONT = pygame.font.SysFont("freesansbold.ttf", 200)
TEXT_FONT = pygame.font.SysFont("freesansbold.ttf", 50)
SMALL_FONT = pygame.font.SysFont("freesansbold.ttf", 35)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe Bot")

#0 => EMPTY
#1 => X
#2 => O
board = [0, 0, 0, 0, 0, 0, 0, 0, 0]

def emptypos(board):
    pos = []
    for i in range(len(board)):
        if board[i] == 0:
            pos.append(i)
    return pos

def checkwin(board):
    win = False
    win_pos = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
    for i in win_pos:
        if board[i[0]] == board[i[1]] == board[i[2]] != 0:
            winner = board[i[0]]
            win = True
            break
    if win == False:
        winner = None 
    return winner

def minimax(board, depth, maximize, max_player, min_player):
    winner = checkwin(board)
    
    if winner == max_player:
        return 100 - depth
    elif winner == min_player:
        return -100 - depth
    elif len(emptypos(board))  == 0:
        return 0

    if maximize:
        best = -1000
        empty = emptypos(board)
        for i in empty:
            board[i] = max_player
            best = max(best, minimax(board, depth + 1, False, max_player, min_player))
            board[i] = 0
        return best
    else:
        best = 1000
        empty = emptypos(board)
        for i in empty:
            board[i] = min_player
            best = min(best, minimax(board, depth + 1, True, max_player, min_player))
            board[i] = 0
        return best
    
def bestmove(board, max_player, min_player):
    bestmove = None
    bestscore = -1000

    empty = emptypos(board)
    for i in empty:
        board[i] = max_player

        score = minimax(board, 0, False, max_player, min_player)

        board[i] = 0 
        if score > bestscore:
            bestscore = score
            bestmove = i 
    print("Best Move:", bestmove)
    print("Score:", bestscore)
    return bestmove

def listen():
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            return("quit")
        if events.type == pygame.MOUSEBUTTONDOWN:
            return("clicked")

def draw_board(win, board):
    win.fill(BLACK)
    #drawing vertical lines
    pygame.draw.line(
        win, WHITE, ((WIDTH-BOARD_WIDTH)/2 + BOARD_WIDTH/3, (HEIGHT-BOARD_WIDTH)/2), 
        ((WIDTH-BOARD_WIDTH)/2 + BOARD_WIDTH/3, HEIGHT-(HEIGHT-BOARD_WIDTH)/2), LINE_WIDTH)
    
    pygame.draw.line(
        win, WHITE, ((WIDTH-BOARD_WIDTH)/2 + 2*BOARD_WIDTH/3, (HEIGHT-BOARD_WIDTH)/2),
        ((WIDTH-BOARD_WIDTH)/2 + 2*BOARD_WIDTH/3, HEIGHT-(HEIGHT-BOARD_WIDTH)/2), LINE_WIDTH)
    
    #drawing horizontal lines
    pygame.draw.line(
        win, WHITE, ((WIDTH-BOARD_WIDTH)/2, (HEIGHT-BOARD_WIDTH)/2 + BOARD_WIDTH/3),
        (WIDTH-(WIDTH-BOARD_WIDTH)/2, (HEIGHT-BOARD_WIDTH)/2 + BOARD_WIDTH/3), LINE_WIDTH)
    
    pygame.draw.line(
        win, WHITE, ((WIDTH-BOARD_WIDTH)/2, (HEIGHT-BOARD_WIDTH)/2 + 2*BOARD_WIDTH/3),
        (WIDTH-(WIDTH-BOARD_WIDTH)/2, (HEIGHT-BOARD_WIDTH)/2 + 2*BOARD_WIDTH/3), LINE_WIDTH)
    
    #drawing Xs and Os
    at = 0
    x_start = x_xo = (WIDTH-BOARD_WIDTH)/2 + BOARD_WIDTH/6
    y_start = y_xo = (HEIGHT-BOARD_WIDTH)/2 + BOARD_WIDTH/6
    gap = BOARD_WIDTH/3
    for i in range(3):
        for j in range(3):
            if board[at] == 1:
                text = XO_FONT.render('X', True, RED)
                win.blit(text, (x_xo - text.get_width()/2, y_xo - text.get_height()/2))
            elif board[at] == 2:
                text = XO_FONT.render('O', True, BLUE)
                win.blit(text, (x_xo - text.get_width()/2, y_xo - text.get_height()/2))
            at += 1
            x_xo += gap
        y_xo += gap
        x_xo = x_start

def intro_page(win, listen_out):
    win.fill(BLACK)
    intro_text = TEXT_FONT.render('How would you like to play?', True, WHITE, BLUE)
    win.blit(intro_text, (WIDTH/2 - intro_text.get_width()/2, HEIGHT/3 - intro_text.get_height()/2))
    button_gap = WIDTH/10
    X_text = XO_FONT.render('X', True, RED)
    O_text = XO_FONT.render('O', True, BLUE)
    button_width = X_text.get_height()*1.2
    left_button_pos = ((WIDTH - button_gap - button_width)/2, HEIGHT/1.5 - button_width/2) # centered
    right_button_pos = ((WIDTH + button_gap + button_width)/2, HEIGHT/1.5 - button_width/2) # centered
    left_button_rect = pygame.Rect(left_button_pos[0] - button_width/2, left_button_pos[1] - button_width/2, button_width, button_width)
    right_button_rect = pygame.Rect(right_button_pos[0] - button_width/2, right_button_pos[1] - button_width/2, button_width, button_width)
    pygame.draw.rect(win, WHITE, left_button_rect, 0, 4)
    pygame.draw.rect(win, WHITE, right_button_rect, 0, 4)
    bottom_text = SMALL_FONT.render("X moves first", True, WHITE)
    win.blit(X_text, (left_button_pos[0] - X_text.get_width()/2, left_button_pos[1] - X_text.get_height()/2))
    win.blit(O_text, (right_button_pos[0] - O_text.get_width()/2, right_button_pos[1] - O_text.get_height()/2))
    win.blit(bottom_text, ((WIDTH-bottom_text.get_width())/2, HEIGHT*0.75))

    if listen_out == 'clicked':
        mouse = pygame.mouse.get_pos()
        if left_button_rect.collidepoint(mouse):
            return 1
        elif right_button_rect.collidepoint(mouse):
            return 2

def detect_clicked_box(listen_out):
    mouse = pygame.mouse.get_pos()
    gap = BOARD_WIDTH/3
    x_start = x = (WIDTH-BOARD_WIDTH)/2
    y = (HEIGHT-BOARD_WIDTH)/2
    if listen_out == 'clicked':
        for i in range(9):
            if x < mouse[0] <x+gap and y < mouse[1] < y+gap:
                return i
            x += gap
            if (i+1)%3 == 0:
                x = x_start
                y += gap

def ending_page(win, winner, min_player,tie):
    win.fill(BLACK)
    if not tie:
        if winner == min_player:
            final_text = XO_FONT.render("You Won!", True, GREEN)
        else:
            final_text = XO_FONT.render("You Lost!", True, RED)
    else:
        final_text = XO_FONT.render("Tie!", True, BLUE)
    win.blit(final_text, ((WIDTH-final_text.get_width())/2, (HEIGHT-final_text.get_height())/2))


def main():
    run = True
    min_player = None
    over = False
    turn = 1
    while run:
        listen_out = listen()
        if min_player is None:
            min_player = intro_page(WIN, listen_out)
            if min_player == 1: max_player = 2
            elif min_player == 2: max_player = 1
        else:
            draw_board(WIN, board)
            if not over:
                if turn == 1:
                    if max_player == 1:
                        board[bestmove(board, max_player, min_player)] = 1
                        turn = 2
                    else:
                        clicked_box = detect_clicked_box(listen_out)
                        if clicked_box is not None:
                            board[clicked_box] = 1
                            turn = 2

                elif turn == 2:
                    if max_player == 2 and len(emptypos(board)) != 0:
                        board[bestmove(board, max_player, min_player)] = 2
                        turn = 1
                    else:
                        clicked_box = detect_clicked_box(listen_out)
                        if clicked_box is not None:
                            board[clicked_box] = 2
                            turn = 1

            winner = checkwin(board)
            tie = len(emptypos(board)) == 0
            if winner is not None or tie:
                over = True
                ending_page(WIN, winner, min_player, tie)
  
        pygame.display.update()

        if listen_out == 'quit':
            run= False
            break
    pygame.quit()
        


if __name__ == "__main__":
    main()





