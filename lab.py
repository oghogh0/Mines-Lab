"""
6.1010 Spring '23 Lab 7: Mines
"""

#!/usr/bin/env python3

import typing
import doctest

# NO ADDITIONAL IMPORTS ALLOWED!


def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f"{key}:")
            for inner in val:
                print(f"    {inner}")
        else:
            print(f"{key}:", val)


# HELPER FNCS
def get_coordinate_value(nd_array, coordinate):
    """
    Args:
        nd_array : n-dimension array # think of as nested lists
        coordinate : tuple/list of coordinates

    Returns:
        value at that coordinate
    """
    if not isinstance(nd_array[0], list):  # base case = 1d, could be int or str
        return nd_array[coordinate[0]]  # [coordinate[0]] is the 1st list
    else:
        return get_coordinate_value(
            nd_array[coordinate[0]], coordinate[1:]
        )  # want index of nd_array at the coordinate point


def replace_coordinate_value(nd_array, coordinate, value):
    """
    Args:
        nd_array : n-dimension array
        coordinate : tuple/list of coordinates
        value: replacement value

    Returns:
        n-dimension array with coordinates value
        replaced by given value
    """
    if not isinstance(nd_array[0], list):
        nd_array[coordinate[0]] = value
    else:
        replace_coordinate_value(nd_array[coordinate[0]], coordinate[1:], value)
    return nd_array  # return at end


def create_nd_array(dimensions, value):
    """
    Args:
        dimesnions: list of dimensions
        value: num
    Returns:
        n-d array with dimensions in 'dimensions' list with each value in the array being
        the given value
    """
    if len(dimensions) == 1:
        return [value] * dimensions[0]
    else:
        # create_nd_array(dimensions[1:], value) finds what the array you want looks like - don't store bc of aliasing
        return [create_nd_array(dimensions[1:], value) for i in range(dimensions[0])]


def get_coordinates(dimensions):
    """
    Returns all possible coords in a given board
    """
    if len(dimensions) == 1:  # base case
        result1 = []
        for i in range(dimensions[0]):
            result1.append((i,))
        return result1
    else:
        result2 = []
        for coord in get_coordinates(
            dimensions[1:]
        ):  # makes sense for 2-d case, recursion covers rest of dim
            for i in range(dimensions[0]):
                result2.append((i,) + coord)
        return result2


def get_neighbours(dimensions, coordinate):  # CHECK IF GAME IS INPUT
    """
    Args:
        dimensions: dimensions of game
        coordinate: given coordinate
    Return:
        all neighbours of the coordinate
    """
    if len(coordinate) == 1:
        result1 = []
        for i in range(coordinate[0] - 1, coordinate[0] + 2):
            if i in range(
                dimensions[0]
            ):  # avoids negative e.g. (5,13,0) - can't have coord at -1
                result1.append((i,))
        return result1
    else:
        result2 = []
        for coord in get_neighbours(dimensions[1:], coordinate[1:]):
            for i in range(coordinate[0] - 1, coordinate[0] + 2):
                if i in range(dimensions[0]):  # handles coord (0,0)
                    result2.append((i,) + coord)
        return result2


def game_state(game):
    """
    Returns state of the game: 'ongoing', 'defeat', or 'victory'
    """
    count_bomb = 0
    count_revealed = 0
    count_squares = 0

    for coord in get_coordinates(game["dimensions"]):
        count_squares += 1
        board_val = get_coordinate_value(game["board"], coord)
        hidden_val = get_coordinate_value(game["hidden"], coord)

        if board_val == "." and hidden_val == False:
            return "defeat"
        elif board_val == ".":
            count_bomb += 1
        elif hidden_val == False:
            count_revealed += 1

    if count_bomb + count_revealed == count_squares:
        return "victory"
    else:
        return "ongoing"


# 2-D IMPLEMENTATION


def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    hidden:
        [True, True, True, True]
        [True, True, True, True]
    state: ongoing
    """
    dimensions = (num_rows, num_cols)

    return new_game_nd(dimensions, bombs)





def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['hidden'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is revealed on the board after digging (i.e. game['hidden'][bomb_location]
    == False), 'victory' when all safe squares (squares that do not contain a
    bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    hidden:
        [True, False, False, False]
        [True, True, False, False]
    state: victory

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    hidden:
        [False, False, True, True]
        [True, True, True, True]
    state: defeat
    """
    coordinates = (row, col)

    return dig_nd(game, coordinates)





# def render_2d_locations(game, xray=False):
#     """
#     Prepare a game for display.

#     Returns a two-dimensional array (list of lists) of '_' (hidden squares),
#     '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
#     bombs).  game['hidden'] indicates which squares should be hidden.  If
#     xray is True (the default is False), game['hidden'] is ignored and all
#     cells are shown.

#     Parameters:
#        game (dict): Game state
#        xray (bool): Whether to reveal all tiles or just those that are not
#                     game['hidden']

#     Returns:
#        A 2D array (list of lists)

#     >>> render_2d_locations({'dimensions': (2, 4),
#     ...         'state': 'ongoing',
#     ...         'board': [['.', 3, 1, 0],
#     ...                   ['.', '.', 1, 0]],
#     ...         'hidden':  [[True, False, False, True],
#     ...                   [True, True, False, True]]}, False)
#     [['_', '3', '1', '_'], ['_', '_', '1', '_']]

#     >>> render_2d_locations({'dimensions': (2, 4),
#     ...         'state': 'ongoing',
#     ...         'board': [['.', 3, 1, 0],
#     ...                   ['.', '.', 1, 0]],
#     ...         'hidden':  [[True, False, True, False],
#     ...                   [True, True, True, False]]}, True)
#     [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
#     """
#     rendered_layout = []
#     board_list = game["board"] # do i need to copy?

#     for row, keylst in enumerate(game["hidden"]): # each row
#         new_layout = []

#         for indx, item in enumerate(keylst): # True/False
#             key = board_list[row][indx]
#             if xray == False:
#                 if item == True: # hidden
#                     new_layout.append("_")
#                 else:
#                     if key == 0:
#                         new_layout.append(" ")
#                     else:
#                         new_layout.append(str(key))
#             else: # xray == True - reveal all
#                 if key == 0:
#                         new_layout.append(" ")
#                 else:
#                     if key == ".":
#                         new_layout.append(".")
#                     else:
#                         new_layout.append(str(key))

#         rendered_layout.append(new_layout)

#     return rendered_layout


def render_2d_locations(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  game['hidden'] indicates which squares should be hidden.  If
    xray is True (the default is False), game['hidden'] is ignored and all
    cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just those that are not
                    game['hidden']

    Returns:
       A 2D array (list of lists)

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, False, True],
    ...                   [True, True, False, True]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, True, False],
    ...                   [True, True, True, False]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    return render_nd(game, xray)


def render_2d_board(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function
        render_2d_locations(game)

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       A string-based representation of game

    >>> render_2d_board({'dimensions': (2, 4),
    ...                  'state': 'ongoing',
    ...                  'board': [['.', 3, 1, 0],
    ...                            ['.', '.', 1, 0]],
    ...                  'hidden':  [[False, False, False, True],
    ...                            [True, True, False, True]]})   # for False
    '.31_\\n__1_'
    """
    rendered_board_layout = str()

    for keylst in render_nd(game, xray):

        for key in keylst:
            rendered_board_layout += key
        rendered_board_layout += "\n"

    return rendered_board_layout[:-1]  # w/o space at end


# N-D IMPLEMENTATION


def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of tuples, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, True], [True, True], [True, True], [True, True]]
        [[True, True], [True, True], [True, True], [True, True]]
    state: ongoing
    """

    board_array = create_nd_array(dimensions, 0)  # create array of 0

    for coord in get_coordinates(dimensions):
        if coord in bombs:
            new_board_array = replace_coordinate_value(
                board_array, coord, "."
            )  # assign bombs
            for neighbour in get_neighbours(dimensions, coord):  # bomb neighbours
                if neighbour != coord:  # get_neighbours includes coord
                    neighbour_val = get_coordinate_value(new_board_array, neighbour)
                    if isinstance(neighbour_val, int):  # not bomb
                        neighbour_val += 1
                        replace_coordinate_value(
                            board_array, neighbour, neighbour_val
                        )  # updates val

    return {
        "dimensions": dimensions,
        "board": board_array,
        "hidden": create_nd_array(dimensions, True),
        "state": "ongoing",
    }


def dig_nd(game, coordinates, previous_val=None):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the hidden to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is revealed on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [True, True],
    ...                [True, True]],
    ...               [[True, True], [True, True], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, True], [True, False], [False, False], [False, False]]
        [[True, True], [True, True], [False, False], [False, False]]
    state: ongoing
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [True, True],
    ...                [True, True]],
    ...               [[True, True], [True, True], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, False], [True, False], [True, True], [True, True]]
        [[True, True], [True, True], [True, True], [True, True]]
    state: defeat
    """

    if (game["state"] != "ongoing"
        or get_coordinate_value(game["hidden"], coordinates) == False):  # when nothing is revealed
        return 0
    else:
        value = get_coordinate_value(game["board"], coordinates)
        replace_coordinate_value(game["hidden"], coordinates, False)  # revealed

        if value != 0 and isinstance(value, int):
            if previous_val != 0:  # only victory check for non-recursive case
                game["state"] = game_state(game)  # updates esp for victory
            return 1
        elif value == ".":
            game["state"] = "defeat"
            return 1
        else:  # 0
            counter = 1
            for neighbour in get_neighbours(game["dimensions"], coordinates):  # digs only hidden
                counter += dig_nd(game, neighbour, previous_val=0)
            if previous_val != 0:  # only victory check for non-recursive case - saves time
                game["state"] = game_state(game)  # reassigns esp for victory case
            return counter


def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  The game['hidden'] array indicates which squares should be
    hidden.  If xray is True (the default is False), the game['hidden'] array
    is ignored and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [False, False],
    ...                [False, False]],
    ...               [[True, True], [True, True], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    rendered_layout = create_nd_array(game["dimensions"], " ")

    for coord in get_coordinates(game["dimensions"]):
        coord_val = get_coordinate_value(game["board"], coord)

        if xray == False:
            if get_coordinate_value(game["hidden"], coord) == True:
                replace_coordinate_value(rendered_layout, coord, "_")
            elif coord_val == ".":  # bomb case
                replace_coordinate_value(rendered_layout, coord, ".")
            else:
                if (isinstance(coord_val, int) 
                    and coord_val > 0):  # compare 2 ints so check it's an int
                    replace_coordinate_value(rendered_layout, coord, str(coord_val))
        else:
            if coord_val == ".":
                replace_coordinate_value(rendered_layout, coord, ".")
            elif isinstance(coord_val, int) and coord_val > 0:
                replace_coordinate_value(rendered_layout, coord, str(coord_val))
    return rendered_layout




if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d_locations or any other function you might want.  To
    # do so, comment out the above line, and uncomment the below line of code.
    # This may be useful as you write/debug individual doctests or functions.
    # Also, the verbose flag can be set to True to see all test results,
    # including those that pass.
    #
    # doctest.run_docstring_examples(
    #    render_2d_locations,
    #    globals(),
    #    optionflags=_doctest_flags,
    #    verbose=False
    # )

    # render_2d_locations({'dimensions': (2, 4),
    #          'state': 'ongoing',
    #          'board': [['.', 3, 1, 0],
    #                   ['.', '.', 1, 0]],
    #         'hidden':  [[True, False, True, False],
    #                   [True, True, True, False]]}, True)
    # [['.', '3', '1', ' '], ['.', '.', '1', ' ']]

    # render_nd(
    #     {
    #         "dimensions": (2, 4),
    #         "state": "ongoing",
    #         "board": [[".", 3, 1, 0], [".", ".", 1, 0]],
    #         "hidden": [[False, False, False, True], [True, True, False, True]],
    #     }
    # )

    # board_to_hidden({'dimensions': (2, 4),
    #          'state': 'ongoing',
    #          'board': [['.', 3, 1, 0],
    #                   ['.', '.', 1, 0]],
    #         'hidden':  [[True, False, True, False],
    #                   [True, True, True, False]]})

    # render_2d_board({'dimensions': (2, 4),
    #          'state': 'ongoing',
    #          'board': [['.', 3, 1, 0],
    #                   ['.', '.', 1, 0]],
    #         'hidden':  [[False, False, False, True],
    #                   [True, True, False, True]]})

    # print(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    # print(new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)]))
    # print(get_neighbours((0,0)))

    # TEST CASES (1-d, 2-d, 3-d)

    # 1. get_coordinate_value
    # one_d_array = [1, ".", 3, 0] # dim = (4,)
    # print(get_coordinate_value(one_d_array, (2,)))
    # first_expect = 3

    # two_d_array = [[2,4,3],  # dim = (2,3) / 2x3
    #                [1,2,1]]
    # print(get_coordinate_value(two_d_array, (0, 1)))
    # second_expect = 4

    # three_d_array = [[[2,1],[4,1],[3,1]]] # dim = (1, 3, 2) / 1x3x2
    # print(get_coordinate_value(three_d_array, (0, 2, 0)))
    # third_expect = 3

    # 2. replace_coordinate_value
    # one_d_array = [1, ".", 3, 0]
    # print(replace_coordinate_value(one_d_array, (2,), 6))
    # first_expect = [1, ".", 6, 0]

    # two_d_array = [[2,4,3],
    #                [1,2,1]]
    # print(replace_coordinate_value(two_d_array, (0, 1), 6))
    # second_expect = [[2,6,3],
    #                [1,2,1]]

    # three_d_array = [[[2,1],[4,1],[3,1]]]
    # print(replace_coordinate_value(three_d_array, (0, 2, 0), 6))
    # third_expect = [[[2,1],[4,1],[6,1]]]

    # 3. create_nd_array
    # print(create_nd_array([2], 0))
    # first_expect = [0, 0]

    # print(create_nd_array([2, 3], 0))
    # second_expect = [[0,0,0],
    #                  [0,0,0]]

    # print(create_nd_array([2, 3, 1], 0))
    # third_expect = [[[0],[0],[0]],
    #                  [[0],[0],[0]]]

    # 4. get_coordinates
    # print(get_coordinates((5,)))
    # first_expect = [(0,),(1,),(2,),(3,),(4,)]

    # print(get_coordinates((3,5)))
    # second_expect = [(0,0),(0,1),(0,2),(0,3),(0,4),
    #                  (1,0),(1,1),(1,2),(1,3),(1,4),
    #                  (2,0),(2,1),(2,2),(2,3),(2,4)]

    # 5. get_neigbours
    # print(get_neighbours((10,),(5,)))
    # first_expect = [(4,),(5,),(6,)]

    # # edge cases
    # print(get_neighbours((3,),(0,)))
    # expect = [(1,)]
    # print(get_neighbours((10,20),(9,0)))
    # expect = [(8,0),(9,0),(8,1),(9,1)]

    # print(get_neighbours((10,20),(5,13)))
    # second_expect = [(4,12), (4,13) , (4,14) ,
    #                  (5,12), (5,13), (5,14),
    #                  (6,12), (6,13) , (6,14)]

    # print(get_neighbours((10, 20,3),(5,13,0)))
    # third_expect = [(4,12,0), (4,13,0) , (4,14,0) ,
    #                 (5,12,0), (5,13,0), (5,14,0),
    #                 (6,12,0), (6,13,0) , (6,14,0),
    #                 (4,12,1), (4,13,1) , (4,14,1) ,
    #                 (5,12,1), (5,13,1), (5,14,1),
    #                 (6,12,1), (6,13,1) , (6,14,1) ]

    # 6. game_state
    # game_2d= {
    # 'dimensions': (4, 3),
    # 'board': [[1,  '.',  2], [1,   2,  '.'], [1,   2,   1], ['.', 1,   0]],
    # 'hidden': [[False, True, False], [False, False, True], [False, False, False], [True, False, False]],
    # 'state': 'ongoing',
    # }
    # print(game_state(game_2d))

    # dig2d
    # game = {'dimensions': (2, 4),
    #          'board': [['.', 3, 1, 0],
    #                    ['.', '.', 1, 0]],
    #         'hidden': [[True, False, True, True],
    #                  [True, True, True, True]],
    #          'state': 'ongoing'}
    # print(dig_2d(game, 0, 3))
    # expect = 4

    # game = {'dimensions': [2, 4],
    #          'board': [['.', 3, 1, 0],
    #                    ['.', '.', 1, 0]],
    #          'hidden': [[True, False, True, True],
    #                   [True, True, True, True]],
    #          'state': 'ongoing'}
    # print(dig_2d(game, 0, 0))
    # expected=1

    # dignd
    # g = {'dimensions': (2, 4, 2),
    #       'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    #                 [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    #      'hidden': [[[True, True], [True, False], [True, True],
    #                [True, True]],
    #               [[True, True], [True, True], [True, True],
    #                 [True, True]]],
    #      'state': 'ongoing'}
    # dig_nd(g, (0, 3, 0))
    # expected=8
