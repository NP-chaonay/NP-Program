import random
import time
# User parameters
# Table size in horizontal
X_SIZE = 25  # default: 5
# Table size in vertical
Y_SIZE = 25  # default: 5
# Amount of bomb
BOMB_AMOUNT = 140  # default: 5
# Enable bomb-indicator-number block (No one wanna disable this except if you crazy enough)
# set to 1 for enabling or else 0, set to -1 will define behaviour that if there is surrounding bombs, it will displayed as @ instead of number.
ALLOW_BOMBINDICATOR_BLOCK = 1  # default: 1
# Enable doubt-flagged block
ALLOW_DOUBT_BLOCK = False  # default: True
# Enable bomb-flagged block
ALLOW_BOMBFLAG_BLOCK = False  # default: True
# Set how number indicator works: 0=Normal, -1=Only for (top,bottom,left,right), 1=Like -1 but inversed (the other surroundings except blocks that selected by -1)
# so either -1,1 would have maximum indicator number as 4
NUM_INDICATOR_MODE = 0  # default: 0
# Allow telling remaining non-bomb block to click
ALLOW_TELL_REMAIN_NONBOMB_BLOCKS = True  # default: True
# Allow telling remaining bomb-marked block to put in
ALLOW_TELL_REMAIN_BOMBFLAG_BLOCK = True  # default: True
# Allow hint after clicked and game is changed
# if 1: The hint just tell the amount of correct/wrong placement of bomb-flag (works when ALLOW_BOMBFLAG_BLOCK is True)
# if -1: The hint tell the 1 random-bomb position
# if -2: like -1 but tell only one that hasn't marked as bomb
# if 0: do not tell the hint
ALLOW_BOMB_HINT = 0  # default: 0
# Allow telling risk after clicked and game is changed (only on single-click)
ALLOW_TELL_RISK_AFTER_CLICKEDAPPILED = True  # default: True
# Same as above but in game (tell before click a block)
ALLOW_TELL_RISK_ON_GAME = True  # default: True
# Allow game restart using same bomb positioning (The bomb position will be not tell, time/round will be separate for total attempt and current attempt)
ALLOW_RESTART = False  # default: False
# In case of allow game restarting, allow indicator of wrong position of bomb-flags
ALLOW_TELL_WRONGBOMBFLAGPOS = True  # default: False
# Allow gameover ignoring (in count), can set to infinity
GAMEOVER_IGNORING_COUNT = 1  # default: 0
# Allow hint on game-over
ALLOW_HINT_ON_GAMEOVER = True  # default: False
##

# [Todo]
# - Allow diagonal click and plus-signed click using existed around-clicking but just using extra bool
# - Confirm for very dangerous action

# [Docs]
# < Blocks Text>
# O: clickable
# X: Clicked block, not having a bomb
# {1-8}: same as X but indicate of number of surrounding bombs, depends on NUM_INDICATOR_MODE
# @: same as X, but just indicate that there is surrounding bombs with unspecified amount.
# ?: Doubt-marked
# /: may-having-bomb marked
# < also Blocks Text but displayed on game ended >
# O: Clickable, not having a bomb
# X: Clicked block, not having a bomb
# {1-8}: same as X but indicate of number of surrounding bombs, depends on NUM_INDICATOR_MODE
# @: same as X, but just indicate that there is surrounding bombs with unspecified amount.
# ?: No bomb on doubt-makred block
# /: Having bomb, and it is marked correctly
# B: shorted from "Bomb"; Having bomb on clickable block, including lastest clicked block
# !: related symbol of "?"; Having bomb on doubt-marked block
# F: shorted from "Failed marking"; Not having bomb on may-having-bomb--marked

# For check type of arg & raise exception for invalid one


def check_arg_type(varname, vardata, desired_types):
    # State var, if type checking valid
    IsCorrect = False
    for desired_type in desired_types:
        # Using globals because we want to check outer scope variable not on this function scope
        if (type(vardata) is desired_type):
            IsCorrect = True
    if not IsCorrect:
        TypeError('Invalid for parameter "{}"'.format(varname))

# For receive arg-value-checking bools & raise exception for invalid one


def check_arg_value(varname, bools):
    if not bools:
        raise ValueError('Invalid for parameter "{}"'.format(varname))

# Convert indexable value into position of x,y


def indexval_to_posval(index):
    # Type&Val checking
    check_arg_type('index', index, (int,))
    check_arg_value('index', 0 <= index < (X_SIZE*Y_SIZE))
    ##
    return (index % X_SIZE)+1, (index//X_SIZE)+1

# Convert position of x,y into indexable value


def posval_to_indexval(x, y):
    # Type&Val checking
    check_arg_type('x', x, (int,))
    check_arg_type('y', y, (int,))
    check_arg_value('x', 1 <= x <= X_SIZE)
    check_arg_value('y', 1 <= y <= Y_SIZE)
    ##
    return (x+(y-1)*X_SIZE)-1

# Function to print the board, required paramter blocks_text for instance of using in print_finishedgame_board.


def print_board(blocks_text):
    # Type&Val checking
    check_arg_type('blocks_text', blocks_text, (list,))
    check_arg_value('blocks_text', len(blocks_text) == (X_SIZE*Y_SIZE))
    ##
    # Calculate spacing of numberic word
    num_placeholder = (Y_SIZE//10+1)
    # Print header
    print(' '*num_placeholder, end='')
    for i in range(X_SIZE):
        print('{}'.format(i+1).rjust(num_placeholder+1), end='')
    print()
    ##
    # Loop through y axis
    for i in range(Y_SIZE):
        # Defining stepping value for setting the slice
        stepping_val = i*X_SIZE
        # Print the board on given Y-axis, with vertical header
        print('{}'.format(i+1).rjust(num_placeholder), end='')
        for block in blocks_text[stepping_val:X_SIZE+stepping_val]:
            print(' '+block.rjust(num_placeholder), end='')
        print()
        ##

# Function to convert seconds into minutes:seconds


def secs_to_minsec(secs):
    # Type&Val checking
    check_arg_type('secs', secs, (int, float))
    check_arg_value('secs', secs >= 0)
    ##
    # return value, note that int() required to send data as integer, so no further converting.
    return int(secs//60), int(secs % 60)

# Function to ask user for x,y position of block, returns indexable value or error value


def get_block_pos():
    # For error state
    IsError = False
    try:
        xpos = int(input('X position (1-{}): '.format(X_SIZE)))
        ypos = int(input('Y position (1-{}): '.format(Y_SIZE)))
        if 1 <= xpos <= X_SIZE and 1 <= ypos <= Y_SIZE:
            pass
        else:
            IsError = True
    except ValueError:
        IsError = True
    if IsError:
        print('(Error) Please type number in range. Returning to the game...')
        return None
    else:
        return xpos, ypos

# Function to print the board when game finished


def print_finishedgame_board():
    # Even this is end point of game, this is our practice, to preserve original list, and using this instead to temporarily compute the game-ended board.
    tmp_blocks_text = blocks_text.copy()
    # Loop for each blocks to determine the flag displaying
    for i, flag in enumerate(tmp_blocks_text):
        if i in bomb_entries and (not ALLOW_RESTART):
            if flag == '?':
                tmp_blocks_text[i] = '!'
            elif flag == 'O':
                tmp_blocks_text[i] = 'B'
        else:
            if flag == '/' and (ALLOW_TELL_WRONGBOMBFLAGPOS or (not ALLOW_RESTART)):
                tmp_blocks_text[i] = 'F'
    print_board(tmp_blocks_text)

# Function to change the flag of given block, if fail returns False else True; supports only some operation (bomb-flag and doubt-flag), since the others is too complex and may offtopic.


def change_block_state(requested_flag, xpos, ypos):
    # Type&Val checking
    check_arg_type('requested_flag', requested_flag, (str,))
    check_arg_type('xpos', xpos, (int,))
    check_arg_type('ypos', ypos, (int,))
    check_arg_value('requested_flag', len(
        requested_flag) == 1 and (requested_flag in '?/'))
    check_arg_value('xpos', 1 <= xpos <= X_SIZE)
    check_arg_value('ypos', 1 <= ypos <= Y_SIZE)
    ##
    if requested_flag == '?':
        if blocks_text[posval_to_indexval(xpos, ypos)] in 'O/':
            blocks_text[posval_to_indexval(xpos, ypos)] = '?'
            return True
        elif blocks_text[posval_to_indexval(xpos, ypos)] in '?':
            blocks_text[posval_to_indexval(xpos, ypos)] = 'O'
            return True
        # For Non-clickable block
        else:
            return False
    elif requested_flag == '/':
        if blocks_text[posval_to_indexval(xpos, ypos)] in 'O?':
            blocks_text[posval_to_indexval(xpos, ypos)] = '/'
            return True
        elif blocks_text[posval_to_indexval(xpos, ypos)] in '/':
            blocks_text[posval_to_indexval(xpos, ypos)] = 'O'
            return True
        # For Non-clickable block
        else:
            return False

# Function for clicking a block, return {-2,-1,1,2} for {Bomb-flagged-block,Non-clickable-block,ClickedOnNonBomb,ClickedOnBomb} respectively


def click_block(xpos, ypos):
    # Type&Val checking
    check_arg_type('xpos', xpos, (int,))
    check_arg_type('ypos', ypos, (int,))
    check_arg_value('xpos', 1 <= xpos <= X_SIZE)
    check_arg_value('ypos', 1 <= ypos <= Y_SIZE)
    ##
    block_index = posval_to_indexval(xpos, ypos)
    if blocks_text[block_index] in 'O?':
        if block_index in bomb_entries:
            return 2
        else:
            # For getting indicator number for clicked block
            if ALLOW_BOMBINDICATOR_BLOCK != 0:
                num_indicator = 0
                no = block_index+1
                # Checking bomb on surrounding blocks
                if (xpos > 1) and (block_index-1 in bomb_entries) and (NUM_INDICATOR_MODE <= 0):
                    num_indicator += 1
                if (xpos < X_SIZE) and (block_index+1 in bomb_entries) and (NUM_INDICATOR_MODE <= 0):
                    num_indicator += 1
                if (ypos > 1) and (block_index-X_SIZE in bomb_entries) and (NUM_INDICATOR_MODE <= 0):
                    num_indicator += 1
                if (ypos < Y_SIZE) and (block_index+X_SIZE in bomb_entries) and (NUM_INDICATOR_MODE <= 0):
                    num_indicator += 1
                if (xpos > 1 and ypos > 1) and (block_index-1-X_SIZE in bomb_entries) and (NUM_INDICATOR_MODE >= 0):
                    num_indicator += 1
                if (xpos < X_SIZE and ypos > 1) and (block_index+1-X_SIZE in bomb_entries) and (NUM_INDICATOR_MODE >= 0):
                    num_indicator += 1
                if (xpos > 1 and ypos < Y_SIZE) and (block_index-1+X_SIZE in bomb_entries) and (NUM_INDICATOR_MODE >= 0):
                    num_indicator += 1
                if (xpos < X_SIZE and ypos < Y_SIZE) and (block_index+1+X_SIZE in bomb_entries) and (NUM_INDICATOR_MODE >= 0):
                    num_indicator += 1
                ##
                if num_indicator == 0:
                    blocks_text[block_index] = 'X'
                else:
                    if ALLOW_BOMBINDICATOR_BLOCK == 1:
                        blocks_text[block_index] = '{}'.format(num_indicator)
                    else:
                        blocks_text[block_index] = '@'
            else:
                blocks_text[block_index] = 'X'
            return 1
    elif blocks_text[block_index] in '/':
        return -2
    # For non-clickable block
    else:
        return -1

# Function for determining whether the inputted position is valid


def isvalid_pos(xpos, ypos):
    # Type&Val checking
    check_arg_type('xpos', xpos, (int,))
    check_arg_type('ypos', ypos, (int,))
    ##
    try:
        check_arg_value('xpos', 1 <= xpos <= X_SIZE)
        check_arg_value('ypos', 1 <= ypos <= Y_SIZE)
    except ValueError:
        return False
    return True

# Function tell remaining clickable blocks


def get_clickable_blocks_num():
    count = 0
    count += blocks_text.count('X')
    count += blocks_text.count('@')
    count += blocks_text.count('1')
    count += blocks_text.count('2')
    count += blocks_text.count('3')
    count += blocks_text.count('4')
    count += blocks_text.count('5')
    count += blocks_text.count('6')
    count += blocks_text.count('7')
    count += blocks_text.count('8')
    count = table_length-count
    return count

# This function telling hint on sucessful clicked (including game-over)


def tell_hint():
    if ALLOW_BOMB_HINT == 1 and ALLOW_BOMBFLAG_BLOCK:
        correct_bombmarked_count = 0
        wrong_bombmarked_count = 0
        for i in bomb_entries:
            if blocks_text[i] == '/':
                correct_bombmarked_count += 1
        wrong_bombmarked_count = blocks_text.count(
            '/')-correct_bombmarked_count
        print('Hint: Correct/Wrong bomb-flag: {},{}'.format(
            correct_bombmarked_count, wrong_bombmarked_count))
    elif ALLOW_BOMB_HINT == -1:
        index = random.choice(bomb_entries)
        pos = indexval_to_posval(index)
        print('Hint: Bomb position on X,Y={},{}'.format(*pos))
    elif ALLOW_BOMB_HINT == -2:
        # Find any bomb blocks that hasn't marked as bomb, and add their index
        available_bombs = []
        for i in bomb_entries:
            if blocks_text[i] != '/':
                available_bombs.append(i)
        if available_bombs:
            index = random.choice(available_bombs)
            pos = indexval_to_posval(index)
            print('Hint: Bomb position on X,Y={},{}'.format(*pos))
        else:
            print('Hint: No any bomb that hasn\'t marked as bomb.')
    else:
        pass

# Execute when game is over (both having ignore count or not), return True if no usable ignore count


def game_over_action():
    global GameOverCount, game_ended_timerec
    print('\nGAME OVER! You stepped on a bomb.')
    if GameOverCount >= GAMEOVER_IGNORING_COUNT:
        game_ended_timerec = time.time()
        print_finishedgame_board()
        return True
    else:
        print('Luckily, how have {} game-over ignoring counts lefted, now it has been used one.'.format(
            GAMEOVER_IGNORING_COUNT-GameOverCount))
        GameOverCount += 1
        # Undo action made by multiple-selected-blocks operation
        print('Game has undoed due to bomb clicked, but have ignore count for it.')
        for i in range(table_length):
            blocks_text[i] = before_blocks_text[i]
        return False


# Welcoming message
print('Minesweeper Game (by NP-chaonay)')
# Print first-start remark for user
print('Remark: command options is case-sensitive.')
print('Remark: if want to cancel the operation while in x,y position inputting, just put invalid data.')
print()
###
##
# Table length
table_length = X_SIZE*Y_SIZE
# Used for minimum value of randomization of table length
tmp_minvalforrandom_tablelength = -((table_length-1)//2)
# Used for maximum value of randomization of table length
tmp_maxvalforrandom_tablelength = (table_length)//2
# Contains entry in table, that marked as having-bomb
bomb_entries = []
# Loop until bomb_entries has amount of marking-entry as BOMB_AMOUNT specified
while len(bomb_entries) < BOMB_AMOUNT:
    # Randomizing from table length but with normalized value (negative to postitive, to be balanced randomization as most as possible); also subtracted by tmp_minvalforrandom_tablelength later, because to restore normalized value into index-convenient value (instead of converting to 1-N, on length of table.)
    tmp_rand_result = random.randint(
        tmp_minvalforrandom_tablelength, tmp_maxvalforrandom_tablelength)-tmp_minvalforrandom_tablelength
    if tmp_rand_result in bomb_entries:
        pass
    else:
        bomb_entries.append(tmp_rand_result)
# sum-record of all attempts (in case of allow restarting)
allattempts_time = 0
allattempts_round = 0
##
# Set all game attempts started time record
allattempts_started_timerec = time.time()
while True:
    # List contains text for each blocks, initialized by flag "O"
    blocks_text = ['O']*table_length
    # For undoing system
    before_blocks_text = blocks_text.copy()
    # Init round of game
    game_count = 1
    # Init game state
    GameChanged = False
    tmp_GameOver = False
    tmp_GameFinishing = False
    GameOverCount = 0
    ##
    # Set command_msg for message of available command
    # Bombflag is required to ensure that user knows that what block contains a bomb, so this command only works on ALLOW_BOMBFLAG_BLOCK
    if ALLOW_BOMBFLAG_BLOCK and ALLOW_DOUBT_BLOCK:
        command_msg = '[a] Click-Only-Around (Doubt-flagged excluded) [s] Click [d] (Un)Doubt-Flag [f] (Un)Bomb-Flag [x]: Click-Entire-Board-Without-Click-On-Doubt [z]: Finishing-Game/Click-Entire-Board [q]: Surrender/Quit'
    elif ALLOW_BOMBFLAG_BLOCK:
        command_msg = '[a] Click-Only-Around [s] Click [f] (Un)Bomb-Flag [z]: Finishing-Game/Click-Entire-Board [q]: Surrender/Quit'
    elif ALLOW_DOUBT_BLOCK:
        command_msg = '[a] Click-Only-Around (Doubt-flagged excluded) [s] Click [d] (Un)Doubt-Flag [x]: Click-Entire-Board-Without-Click-On-Doubt [q]: Surrender/Quit'
    else:
        command_msg = '[a] Click-Only-Around (Becareful!) [s] Click [q]: Surrender/Quit'
    # Set game attempt started time record
    game_started_timerec = time.time()
    # Loop until manually break because of game-over or winning-a-game
    while True:
        # Main Interface 1
        print('Minesweeper ({}X{} with {} bombs)\nRound #{} | Time passed: {}m:{}s'.format(
            X_SIZE, Y_SIZE, BOMB_AMOUNT, game_count, *secs_to_minsec(time.time()-game_started_timerec)))
        # For counting blocks on each type
        if ALLOW_TELL_REMAIN_NONBOMB_BLOCKS:
            tmp_count = get_clickable_blocks_num()-BOMB_AMOUNT
        else:
            tmp_count = 'NA'
        if ALLOW_BOMBFLAG_BLOCK and ALLOW_TELL_REMAIN_BOMBFLAG_BLOCK:
            tmp_count1 = BOMB_AMOUNT-blocks_text.count('/')
            print(
                'Remaining to-click/to-bomb-marked blocks: {},{}'.format(tmp_count, tmp_count1))
        else:
            print('Remaining non-bomb/bomb-marked blocks: {},{}'.format(tmp_count, 'NA'))
        print('Remaining game-over ignore count: {}/{}'.format(
            GAMEOVER_IGNORING_COUNT-GameOverCount, GAMEOVER_IGNORING_COUNT))
        if ALLOW_TELL_RISK_ON_GAME:
            tmp_count = get_clickable_blocks_num()
            print('The risk of next click is about {}/{} ({:.1f}%).'.format(
                BOMB_AMOUNT, tmp_count, 100*BOMB_AMOUNT/tmp_count))
        print_board(blocks_text)
        print(command_msg)
        user_command = input('Command: ')
        ##
        # User Command Part
        if user_command == 'q':
            user_command = input(
                'Are you sure? Type y then enter or else returning to the game: ')
            if user_command == 'y':
                # Since the count is not gameplay operation but quitting, so reduce it
                game_count -= 1
                game_ended_timerec = time.time()
                print('\nYOU SURRENDERED!')
                print_finishedgame_board()
                break
            else:
                pass
        elif user_command == 'd' and ALLOW_DOUBT_BLOCK:
            tmp_block_pos = get_block_pos()
            if tmp_block_pos is None:
                pass
            else:
                # Call function and determine sucess-state
                if change_block_state('?', *tmp_block_pos):
                    GameChanged = True
                else:
                    print('(Error) The block is already clicked.')
        elif user_command == 'f' and ALLOW_BOMBFLAG_BLOCK:
            tmp_block_pos = get_block_pos()
            if tmp_block_pos is None:
                pass
            else:
                # Call function and determine sucess-state
                if change_block_state('/', *tmp_block_pos):
                    GameChanged = True
                else:
                    print('(Error) The block is already clicked.')
        elif user_command == 's':
            tmp_block_pos = get_block_pos()
            if tmp_block_pos is None:
                pass
            else:
                # do clicking of given block and then save the state value
                tmp_state = click_block(*tmp_block_pos)
                if tmp_state > 0 and ALLOW_TELL_RISK_AFTER_CLICKEDAPPILED:
                    if tmp_state == 1:
                        # add 1 to include the previous clicked that have been done (clicking is not done if clicks on bomb)
                        tmp_count = get_clickable_blocks_num()+1
                    else:
                        tmp_count = get_clickable_blocks_num()
                    print('The risk of this click is about {}/{} ({:.1f}%).'.format(BOMB_AMOUNT,
                                                                                    tmp_count, 100*BOMB_AMOUNT/tmp_count))
                if tmp_state == 2:
                    if ALLOW_HINT_ON_GAMEOVER:
                        tell_hint()
                    if game_over_action():
                        break
                elif tmp_state == 1:
                    tell_hint()
                    GameChanged = True
                elif tmp_state == -2:
                    print(
                        '(Error) The block is flag as having-bomb, cancel the flag first.')
                elif tmp_state == -1:
                    print('(Error) The block is already clicked.')
        elif user_command == 'a':
            tmp_block_pos = get_block_pos()
            if tmp_block_pos is None:
                pass
            else:
                # asking for dangerous action confirmation, only in case of specific user settings
                if not (ALLOW_BOMBFLAG_BLOCK or ALLOW_DOUBT_BLOCK):
                    user_command = input(
                        'Confirm? (type yes to confirm, otherwise cancel it): ')
                    if user_command == 'yes':
                        tmp_allowaction = True
                    else:
                        tmp_allowaction = False
                else:
                    tmp_allowaction = True
                if tmp_allowaction:
                    # loop through increment for x-axis and y-axis, in order to point each surrounding blocks, but skip the operation when it is the center surrounding blocks.
                    for i in [-1, 0, 1]:
                        for j in [-1, 0, 1]:
                            if i == 0 and j == 0:
                                continue
                            tmp_surroundblock_pos = (
                                tmp_block_pos[0]+i, tmp_block_pos[1]+j)
                            # Check if the surrounding block is existed using the value given by increment algorithm
                            if isvalid_pos(*tmp_surroundblock_pos):
                                # Check if block is not in either of these flags
                                if blocks_text[posval_to_indexval(*tmp_surroundblock_pos)] in '?/X@12345678':
                                    pass
                                else:
                                    # do clicking of given block and then save the state value
                                    tmp_state = click_block(
                                        *tmp_surroundblock_pos)
                                    if tmp_state == 2:
                                        tmp_GameOver = True
                                    elif tmp_state == 1:
                                        GameChanged = True
                    if tmp_GameOver:
                        if ALLOW_HINT_ON_GAMEOVER:
                            tell_hint()
                        if game_over_action():
                            break
                        else:
                            tmp_GameOver = False
                    if GameChanged:
                        tell_hint()
        elif user_command == 'z' and ALLOW_BOMBFLAG_BLOCK:
            # asking for dangerous action confirmation
            user_command = input(
                'Confirm? (type yes to confirm, otherwise cancel it): ')
            if user_command == 'yes':
                tmp_allowaction = True
            else:
                tmp_allowaction = False
            if tmp_allowaction:
                # set state to request finishing game
                tmp_GameFinishing = True
                # loop through all blocks
                for i in range(1, X_SIZE+1):
                    for j in range(1, Y_SIZE+1):
                        tmp_block_pos = (i, j)
                        # Check if block is not in either of these flags
                        if blocks_text[posval_to_indexval(*tmp_block_pos)] in '/X@12345678':
                            pass
                        else:
                            # do clicking of given block and then save the state value
                            tmp_state = click_block(*tmp_block_pos)
                            if tmp_state == 2:
                                tmp_GameOver = True
                            elif tmp_state == 1:
                                GameChanged = True
                if tmp_GameOver:
                    # set state to init value (cannot finished because game-over)
                    tmp_GameFinishing = False
                    if ALLOW_HINT_ON_GAMEOVER:
                        tell_hint()
                    if game_over_action():
                        break
                    else:
                        tmp_GameOver = False
        elif user_command == 'x' and ALLOW_DOUBT_BLOCK:
            # asking for dangerous action confirmation
            user_command = input(
                'Confirm? (type yes to confirm, otherwise cancel it): ')
            if user_command == 'yes':
                tmp_allowaction = True
            else:
                tmp_allowaction = False
            if tmp_allowaction:
                # loop through all blocks
                for i in range(1, X_SIZE+1):
                    for j in range(1, Y_SIZE+1):
                        tmp_block_pos = (i, j)
                        # Check if block is not in either of these flags
                        if blocks_text[posval_to_indexval(*tmp_block_pos)] in '/?X@12345678':
                            pass
                        else:
                            # do clicking of given block and then save the state value
                            tmp_state = click_block(*tmp_block_pos)
                            if tmp_state == 2:
                                tmp_GameOver = True
                            elif tmp_state == 1:
                                GameChanged = True
                if tmp_GameOver:
                    if ALLOW_HINT_ON_GAMEOVER:
                        tell_hint()
                    if game_over_action():
                        break
                    else:
                        tmp_GameOver = False
                if GameChanged:
                    tell_hint()
        else:
            print('(Error) Invalid option.')
        ##
        # If program passes to this point, means not game-over, so successful operation, so prepare the undoing operation
        for i in range(table_length):
            before_blocks_text[i] = blocks_text[i]
        # If game is changed but not game-over or surrender
        if GameChanged:
            # Init-value for state var: if game is completed
            tmp_gamecomplete_check = True
            # Check if all non-bomb blocks was clicked
            for i, tmp_flag in enumerate(blocks_text):
                if (tmp_flag not in 'X@12345678') and (i not in bomb_entries):
                    tmp_gamecomplete_check = False
                    break
            if tmp_gamecomplete_check:
                game_ended_timerec = time.time()
                print('\nYou has won the game!')
                print_finishedgame_board()
                break
            game_count += 1
        # In case user requests finishing game, but it is not possible because the point above that if you are able to finish the game, the program should not pass to here
        if tmp_GameFinishing:
            print('Sorry, you have clickable block behind bomb-flagged block.')
            if GameChanged:
                tell_hint()
            # set state to init
            tmp_GameFinishing = False
        if not GameChanged:
            print('Game unchanged.')
        # Separating passage
        print()
        # set state to init value
        GameChanged = False
    # Ending message
    print("Game attempt has ended. Round and Time used: {}, {}m:{}s; Ignore count remaining: {}".format(
        game_count, *secs_to_minsec(game_ended_timerec-game_started_timerec), GAMEOVER_IGNORING_COUNT-GameOverCount))
    if ALLOW_RESTART:
        allattempts_time += game_ended_timerec-game_started_timerec
        allattempts_round += game_count
        user_command = input(
            'Restarting? Type n then enter to exit or else returning to the game: ')
        if user_command == 'n':
            # Set all game attempts ended time record
            allattempts_ended_timerec = time.time()
            # Separating passage
            print()
            # Set this in order print_finishedgame_board to show bombs position
            ALLOW_RESTART = False
            print('Solved board:')
            print_finishedgame_board()
            # Ending message
            print("Entire gameplay has ended. Round and Time used by all attempts summed up: {}, {}m:{}s; All gameplay time: {}m:{}s;".format(
                allattempts_round, *secs_to_minsec(allattempts_time), *secs_to_minsec(allattempts_ended_timerec-allattempts_started_timerec)))
            break
        else:
            # Separating passage
            print()
    else:
        break
