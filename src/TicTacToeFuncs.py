from turtle import down


letter_to_row_dict = {'a': 1, 'b': 2, 'c': 3}


def make_move(move_string: str, current_game_string: str, moving_player_char: str) -> str:
    ''' 
        Make the move specified by move string and then update the current game string.
        We assume that where this is being called we have checked whether the move is valid
    '''

    y_coord = letter_to_row_dict[move_string[0]]
    x_coord = int(move_string[1])

    index_to_change = 3 * (y_coord - 1) + (x_coord - 1) 

    list_of_game_string = list(current_game_string)
    list_of_game_string[index_to_change] = moving_player_char

    if(list_of_game_string[-1] == 'A'):
        list_of_game_string[-1] = 'B'
    else:
        list_of_game_string[-1] = 'A'

    return ''.join(list_of_game_string)



def move_legal(move_string: str, current_game_string: str) -> bool:
    
    if not bounds_check(move_string): # First check that the move string is valid
        return False

    # These terms correspond to if we viewed the game string as a 2D matrix, in actuality, its
    # a 1D string that we will find the index of by the simple calculation of index_to_change
    y_coord = letter_to_row_dict[move_string[0]]
    x_coord = int(move_string[1])

    # We use 1 indexing for row numbering
    index_to_change = 3 * (y_coord - 1) + (x_coord - 1)

    if current_game_string[index_to_change] == '-': # Check if the space is open
        return True


    return False


def test_string_for_win(string_to_test: str, player_char_to_test: str) -> bool:

    for char in string_to_test:
        if(char != player_char_to_test):
            return False 

    return True


def has_player_won(game_string: str, player_char_to_test: str) -> bool:
    '''
        Basic function for checking whether or not a player with a given character has won.
        There are the three rows to check, three cols to check, and two diagonals 
    '''

    for row_index in range(3):
        test_string = game_string[3*row_index] + game_string[3*row_index + 1] \
                        + game_string[3*row_index + 2]

        if(test_string_for_win(test_string, player_char_to_test)):
            return True

    for col_index in range(3):
        test_string = game_string[col_index] + game_string[col_index + 3] + game_string[col_index + 6]

        if(test_string_for_win(test_string, player_char_to_test)):
            return True 


    down_right_diag = game_string[0] + game_string[4] + game_string[8]
    up_right_diag = game_string[6] + game_string[4] + game_string[2]   

    if(test_string_for_win(down_right_diag, player_char_to_test)):
        return True 

    if(test_string_for_win(up_right_diag, player_char_to_test)):
        return True 


    return False


def bounds_check(move_string: str) -> bool:
    '''
        Moves are of the form [a-c][1-3] where rows are represented by a through c and columns are represented by 1 through 3
    '''

    valid_row_chars = "abc"
    valid_col_chars = "123"

    if(len(move_string) != 2):
        return False

    if move_string[0] in valid_row_chars and move_string[1] in valid_col_chars:
        return True 

    return False


def is_game_a_draw(current_game_string: str) -> bool:
    return True


def format_game_string_for_output(current_game_string: str) -> str:
    return_string = ""

    for index in range(len(current_game_string)):

        if current_game_string[index] == '-':
            return_string += '⬜'
        elif current_game_string[index] == 'x':
            return_string += '❌'
        elif current_game_string[index] == 'o':
            return_string += '🅾️'

        if (index + 4) % 3 == 0:
            return_string += '\n'

    return return_string
