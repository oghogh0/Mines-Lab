<h1>Image Processing Lab</h1>
<h2>Description</h2>
Mines is a game played on a rectangular n×m board (where n = num of rows and m = num of cols), covered with 1×1 square tiles. Some of these tiles hide secretly buried mines; all the other squares are safe. On each turn, the player removes one tile. The player wins when all safe tiles have been removed, without revealing a single mine, and loses if a mine is revealed. When a safe square is revealed, that square is additionally inscribed with a number between 0 and 8, indicating the number of surrounding mines (when rendering the board, 0 is replaced by a blank). Additionally, any time a 0 is revealed (a square surrounded by no mines), the surrounding squares are also automatically revealed, as they are safe).<br />

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
