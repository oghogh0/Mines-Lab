<h1>Image Processing Lab</h1>
<h2>Description</h2>
Mines is a game played on a rectangular n×m board (where n = num of rows and m = num of cols), covered with 1×1 square tiles. Some of these tiles hide secretly buried mines; all the other squares are safe. On each turn, the player removes one tile. The player wins when all safe tiles have been removed, without revealing a single mine, and loses if a mine is revealed. When a safe square is revealed, that square is additionally inscribed with a number between 0 and 8, indicating the number of surrounding mines (when rendering the board, 0 is replaced by a blank). Additionally, any time a 0 is revealed (a square surrounded by no mines), the surrounding squares are also automatically revealed, as they are safe).<br />

Initially, the lab considered only 2-D arrays before expanding to N-D arrays. After implementing some functions with multiple for loops and realise how unfeasible that would be for an N-D array, I rewrote my code recursively.<br />

<h2>Languages and Environments Used</h2>

- <b>Python</b> 
- <b>VS code</b>

<h2>Program walk-through</h2>

<p align="left">
Create useful HELPER FUNCTIONS:<br/>
1. get_coordinate_value: returns the value at a given coordinate in an N-D array.<br/>
2. replace_coordinate_value: returns the N-D array given after replacing the value at the specified coordinate with another value.<br/>
3. create_nd_array: creates an N-D array with each value being the input value.<br/>
4. get_coordinates: returns all possible coords in a given board.<br/>
5. get_neighbours: returns a list of all neighbouring coordinates of the given coordinate.<br/>

<br/>
<p align="left">
Create function to determine the GAME STATE:<br/>
This function returns state of the game. There are 3 game states: 'ongoing', 'defeat', or 'victory'. The state of an ongoing game is represented as a dictionary consisting of 4 keys:<br/>
- 'dimensions': (nrows, ncolumns).<br/>
- 'board': an n-dimensional array of integers and strings, implemented using nested lists --> game['board'][r][c] is '.' if square (r,c) contains a bomb, and it is a number indicating the number of neighbouring bombs otherwise.<br/>
- 'hidden': an n-dimensional array of Booleans, implemented using nested lists --> game['hidden'][r][c] indicates whether the contents of square (r,c) are hidden to the player.<br/>
- 'state': a string containing the state of the game.<br/>

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

<br/>
<p align="left">
Implement HYPERMINES game:<br/>
There are 4 functions involved in doing so, including: <br/>

1. new_game_nd: this function starts a new game and returns a game state dictionary, with the keys having values that are adequately initialised. The inputs are the game dimensions and the position of the bombs. <br/>

For example: <br/>
Calling new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)]) should return this dictionary.<br/>
<br/>
{<br/>
board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]],<br/>
dimensions: (2, 4, 2),<br/>
hidden: [[True, True], [True, True], [True, True], [True, True]]
        [[True, True], [True, True], [True, True], [True, True]], <br/>
state: ongoing<br/>
}

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
<br/>

2. dig_nd: this function recursively digs up square at coordinates and its neighboring squares. Also,  it updates 'hidden' to reveal square at coordinates; then recursively reveal its neighbours, as long as coordinates does not contain and is not adjacent to a
bomb. As well as updating the state to 'defeat' when at least one bomb is revealed on the board after digging, or 'victory' when all squares are safe and no bombs are revealed, and 'ongoing' otherwise. It should return the number of squares revealed. If the incoming game state is not 'ongoing', no action should be taken and 0 returned. <br/>

For example, given this game: <br/>
g = {
     'dimensions': (2, 4, 2), <br/>
     'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],<br/>
               [['.', 3], [3, '.'], [1, 1], [0, 0]]],<br/>
     'hidden': [[[True, True], [True, False], [True, True],
               [True, True]],<br/>
               [[True, True], [True, True], [True, True],<br/>
               [True, True]]],<br/>
     'state': 'ongoing'<br/>
     }<br/>
<br/>
dig_nd(g, (0, 0, 1)) returns 1<br/>

dump(g) shows the game state:<br/>
board:
    [[3, '.'], [3, 3], [1, 1], [0, 0]]
    [['.', 3], [3, '.'], [1, 1], [0, 0]]
dimensions: (2, 4, 2)
hidden:
    [[True, False], [True, False], [True, True], [True, True]]
    [[True, True], [True, True], [True, True], [True, True]]
state: defeat
<br/>
    
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
