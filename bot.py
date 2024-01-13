#0 => EMPTY
#1 => X
#2 => O
user_player = (input("You would like to play as (X or O): ")).lower()

if user_player == "x":
    max_player = 2
    min_player = 1
else:
    max_player = 1
    min_player = 2

board = [0, 0, 0, 0, 0, 0, 0, 0, 0]

def display_board(curr_board):
    cboard = []
    for i in curr_board:
        if i == 0:
            cboard.append(" ")
        elif i == 1:
            cboard.append("X")
        elif i == 2:
            cboard.append("O")

    print(cboard[0], "|", cboard[1], "|", cboard[2])
    print("- - - - -")
    print(cboard[3], "|", cboard[4], "|", cboard[5])
    print("- - - - -")
    print(cboard[6], "|", cboard[7], "|", cboard[8])


def emptypos(board_state):
    pos = []
    for i in range(len(board_state)):
        if board_state[i] == 0:
            pos.append(i)
    return pos

def checkwin(cboard):
    win = False
    win_pos = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
    for i in win_pos:
        if cboard[i[0]] == cboard[i[1]] == cboard[i[2]] != 0:
            winner = cboard[i[0]]
            win = True
            break
    if win == False:
        winner = None 
    
    return winner

def minimax(cboard, depth, maximize, max_player, min_player):
    winner = checkwin(cboard)
    
    if winner == max_player:
        return 100 - depth
    elif winner == min_player:
        return -100 - depth
    elif len(emptypos(cboard))  == 0:
        return 0

    if maximize:
        best = -1000
        empty = emptypos(cboard)
        for i in empty:
            cboard[i] = max_player
            best = max(best, minimax(cboard, depth + 1, False, max_player, min_player))
            cboard[i] = 0
        return best
    else:
        best = 1000
        empty = emptypos(cboard)
        for i in empty:
            cboard[i] = min_player
            best = min(best, minimax(cboard, depth + 1, True, max_player, min_player))
            cboard[i] = 0
        return best

def bestmove(cboard, max_player, min_player):
    bestmove = None
    bestscore = -1000

    empty = emptypos(cboard)
    for i in empty:
        cboard[i] = max_player

        score = minimax(cboard, 0, False, max_player, min_player)

        cboard[i] = 0 
        if score > bestscore:
            bestscore = score
            bestmove = i 
    print("Best Move:", bestmove)
    print("Score:", bestscore)
    return bestmove

turn = 1
win = False
display_board(board)
while not(win):
    if turn == 1:
        if max_player == 1:
            board[bestmove(board, max_player, min_player)] = 1
        else:
            move = int(input("Enter your move position: "))
            board[move-1] = 1
        display_board(board)
        turn = 2

    elif turn == 2:
        if max_player == 2:
            board[bestmove(board, max_player, min_player)] = 2
        else:
            move = int(input("Enter your move position: "))
            board[move-1] = 2
        display_board(board)
        turn = 1
    
    winner = checkwin(board)
    if winner != None:
        win = True
        if winner == 1:
            print("X won!")
        else:
            print("O won!")

    if len(emptypos(board)) == 0:
        print("Tie!")
        break


