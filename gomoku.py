"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Oct. 30, 2021
"""

def is_empty(board):
    empty = True
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != ' ':
                empty = False
    return empty

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    colour = board[y_end][x_end]
    y_start = y_end - d_y * (length-1)
    x_start = x_end - d_x * (length-1)
    bounded = 0


    if (y_end + d_y == len(board) or (y_end + d_y == -1)) or \
       (x_end + d_x == len(board) or x_end + d_x == -1):
        bounded += 1
    else:
        y_bot, x_bot = y_end + d_y, x_end + d_x
        if board[y_bot][x_bot] == colour:
            return None
        if board[y_bot][x_bot] != ' ':
            bounded += 1

    if (y_start - d_y == len(board) or (y_start - d_y == -1)) or\
       (x_start - d_x == len(board) or x_start - d_x == -1):
        bounded += 1

    else:
        y_top, x_top = y_start - d_y, x_start - d_x
        if board[y_top][x_top] == colour:
            return None
        if board[y_top][x_top] != ' ':
            bounded += 1

    if bounded == 0:
        return "OPEN"
    if bounded == 1:
        return "SEMIOPEN"
    if bounded == 2:
        return "CLOSED"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open = 0
    semi = 0
    count = 0
    i = 0
    y = y_start + i*d_y
    x = x_start + i*d_x

    while y >= 0 and y <= len(board)-1 and x >= 0 and x <= len(board)-1:

        if board[y][x] == col:
            count += 1
        else:
            if count == length:
                bounded_result = is_bounded(board, y-d_y, x-d_x, length, d_y, d_x)
                if bounded_result == "OPEN":
                    open += 1
                if bounded_result == "SEMIOPEN":
                    semi += 1
            count = 0

        i += 1
        y = y_start + i*d_y
        x = x_start + i*d_x

    if count == length:
        bounded_result = is_bounded(board, y-d_y, x-d_x, length, d_y, d_x)
        if bounded_result == "OPEN":
            open += 1
        if bounded_result == "SEMIOPEN":
            semi += 1
    count = 0

    return(open,semi)


def detect_rows(board, col, length):
    open = 0
    semi = 0

    for i in range(len(board)): #vertical
        result = detect_row(board, col, 0, i, length, 1, 0)
        open += result[0]
        semi += result[1]
    for i in range(len(board)): #horizontal
        result = detect_row(board, col, i, 0, length, 0, 1)
        open += result[0]
        semi += result[1]
    for i in range(len(board)):
        result = detect_row(board, col, i, 0, length, -1, 1)
        open += result[0]
        semi += result[1]
    for i in range(1,len(board)): #don't double count longest diagonal
        result = detect_row(board, col, len(board)-1, i, length, -1, 1)
        open += result[0]
        semi += result[1]
    for i in range(len(board)):
        result = detect_row(board, col, i, 0, length, 1, 1)
        open += result[0]
        semi += result[1]
    for i in range(1,len(board)): #don't double count longest diagonal
        result = detect_row(board, col, 0, i, length, 1, 1)
        open += result[0]
        semi += result[1]

    return open, semi

def search_max(board):
    scores = {}

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == ' ':
                board[i][j] = "b"
                res = score(board)
                scores[i*10+j] = res
                board[i][j] = ' '
                highscore = max(scores, key = scores.get)
                move_y = highscore // 10
                move_x = highscore - move_y*10

            else:
                pass
    return move_y, move_x


def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

def is_win(board):

    white_win = detect_rows(board, "w", 5)
    if white_win != (0,0):
        return("White won")

    white_wins = detect_closed_rows(board,"w",5)
    if white_wins != 0:
        return("White won")

    black_win = detect_rows(board, "b", 5)
    if black_win != (0,0):
        return("Black won")

    black_wins = detect_closed_rows(board,"b",5)
    if black_wins != 0:
        return("Black won")

    for i in range(len(board)):
        if " " in board[i]:
            return "Continue playing"

    return "Draw"

def detect_closed_row(board, col, y_start, x_start, length, d_y, d_x):
    closed = 0
    count = 0
    i = 0
    y = y_start + i*d_y
    x = x_start + i*d_x

    while y >= 0 and y <= len(board)-1 and x >= 0 and x <= len(board)-1:

        if board[y][x] == col:
            count += 1
        else:
            if count == length:
                bounded_result = is_bounded(board, y-d_y, x-d_x, length, d_y, d_x)
                if bounded_result == "CLOSED":
                    closed += 1
            count = 0

        i += 1
        y = y_start + i*d_y
        x = x_start + i*d_x

    if count == length:
        bounded_result = is_bounded(board, y-d_y, x-d_x, length, d_y, d_x)
        if bounded_result == "CLOSED":
            closed += 1
    count = 0

    return(closed)


def detect_closed_rows(board, col, length):
    closed = 0

    for i in range(len(board)): #vertical
        result = detect_closed_row(board, col, 0, i, length, 1, 0)
        closed += result
    for i in range(len(board)): #horizontal
        result = detect_closed_row(board, col, i, 0, length, 0, 1)
        closed += result
    for i in range(len(board)):
        result = detect_closed_row(board, col, i, 0, length, -1, 1)
        closed += result
    for i in range(1,len(board)): #don't double count longest diagonal
        result = detect_closed_row(board, col, len(board)-1, i, length, -1, 1)
        closed += result
    for i in range(len(board)):
        result = detect_closed_row(board, col, i, 0, length, 1, 1)
        closed += result
    for i in range(1,len(board)): #don't double count longest diagonal
        result = detect_closed_row(board, col, 0, i, length, 1, 1)
        closed += result

    return closed

def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))




def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")

def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 0; y = 0; d_x = 1; d_y = 1; length = 5; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")

    print_board(board)
    if detect_rows(board, col,length) == (0,1):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0




if __name__ == '__main__':
    #play_gomoku(8)

    easy_testset_for_main_functions()

# Board:
# *0|1|2|3|4|5|6|7*
# 0 |b|b|b| | | | *
# 1 | | | | | | | *
# 2 | | | | | | | *
# 3 |b| | | | | | *
# 4 |b| | | | | | *
# 5 |b|w| | |w| | *
# 6b|b|b|b| |w| | *
# 7 |b| | | | | | *
# *****************
#
# Here is the difference between the analyses:
#
# Black stones
#   Your: Open rows of length 2: 2
# Server: Open rows of length 2: 1
#
#   Your: Semi-open rows of length 2: 1
# Server: Semi-open rows of length 2: 2
#
#   Your: Open rows of length 4: 1
# Server: Open rows of length 4: 0
#
#   Your: Semi-open rows of length 4: 0
# Server: Semi-open rows of length 4: 1



    board =   [[' ', 'b', 'b', 'b', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', 'b', ' ', ' ', ' ', ' ', ' ', ' '], [' ', 'b', ' ', ' ', ' ', ' ', ' ', ' '], [' ', 'b', 'w', ' ', ' ', 'w', ' ', ' '], ['b', 'b', 'b', 'b', ' ', 'w', ' ', ' '], [' ', 'b', ' ', ' ', ' ', ' ', ' ', ' ']]

    # print(detect_rows(board,"b",2))
    # print(detect_row(board,"b",6,0,2,-1,1))
    # print(is_bounded(board,5,1,2,-1,1))
    #print(detect_row(board,"b",7,4,2,-1,1))
    print_board(board)
    print(is_win(board))