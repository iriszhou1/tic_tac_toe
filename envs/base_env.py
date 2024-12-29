"""
RL environment holding board and turn information for a classic game of tic-tac-toe
on a 3x3 board.
"""

from gymnasium import Env
import numpy as np

class BaseEnv(Env):
    """
    Environment for the classic 3x3 version of tic-tac-toe.
    """
    def __init__(self):
        """
        Initlizes environment for the classic version of tic-tac-toe.
        """
        # Board with "X", "O", and " " values
        self.board: list[list[str]] = [[" ", " ", " "],
                                       [" ", " ", " "],
                                       [" ", " ", " "]]
        self.n: int = len(self.board)

        # Array representation of board, where "X" = 1, "O" = -1, and " " = 0
        self.array_board: np.array = np.zeros((3, 3), dtype=int)

        # TODO: randomize who gets the first turn via "coin flip"
        #       OR use game of rock-paper-scissors
        self.turn_is_X: bool = True
        self.cpu: str = "X"
        self.terminated: bool = False
        self.num_moves: int = 0
        print('X goes first!')


    def step(self) -> None:
        pass


    def render(self) -> None:
        """
        Prints current state of board.
        """
        mid_line = ["---" for i in range(self.n)]
        mid_line = "-".join(mid_line)

        for i in range(self.n):
            line = f" {self.board[i][0]}"
            for j in range(1, self.n):
                line += f" | {self.board[i][j]}"

            # Print values on board and dividing line
            print(line)
            if i < self.n - 1:
                print(mid_line)


    def reset(self) -> None:
        pass


    def close(self) -> None:
        pass


    def take_turn(self, move: tuple[int]) -> None:
        """
        Given the desired board position, updates the board to reflect move for player or computer.

        :param move: tuple of (x, y) coordinate for desired move, where (0, 0) is in the top left corner,
                     and (2, 2) is in the bottom right corner. x is the row, and y is the column.
        """
        if type(move) != tuple:
            raise ValueError("Input must be a tuple of integer values representing desired position on board!")
        elif len(move) != 2:
            raise ValueError("Input must have 2 arguments (x, y) representing row and column of desired position!")
        elif type(move[0]) != int or type(move[1]) != int:
            raise ValueError("Input must be a tuple of integer values representing desired position on board!")

        if self.turn_is_X:
            player = "X"
            number = 1
        else:
            player = "O"
            number = -1

        x, y = move
        if self.move_is_valid(move):
            self.board[x][y] = player
            self.array_board[x][y] = number
            self.num_moves += 1

            self.check_if_game_over(move)
            if not self.terminated:
                self.turn_is_X = not self.turn_is_X
        else:
            raise ValueError(f"The move {move} is not a valid move. Try again.")


    def in_board(self, position: tuple[int]) -> bool:
        """
        Given tuple representing position on board, returns True if position is
        on board, and False if outside bounds of board.

        :param position: tuple of (x, y) coordinate for board position, where (0, 0) is in the top left corner,
                         and (2, 2) is in the bottom right corner. x is the row, and y is the column.
        :return: True if position is in board, False otherwise.
        """
        x, y = position
        in_height = x >= 0 and x < self.n
        in_width = y >= 0 and y < self.n
        in_board = in_height and in_width

        if not in_board:
            raise ValueError(f"The position {position} is not in the board! Input 0 <= x, y < {self.n}.")
        return in_board


    def move_is_valid(self, move: tuple[int]) -> bool:
        """
        Given desired board position, returns True if player can place their letter in the move position.
        Returns False otherwise.

        :param move: tuple of (x, y) coordinate for desired move, where (0, 0) is in the top left corner,
                     and (2, 2) is in the bottom right corner. x is the row, and y is the column.
        :return: True if move is valid, False otherwise.
        """
        x, y = move
        return self.in_board(move) and self.board[x][y] == " "


    def check_if_game_over(self, move: tuple[int]) -> None:
        """
        Given player's most recent move, returns True if player has won, False otherwise.

        :param move: tuple of (x, y) coordinate for desired move, where (0, 0) is in the top left corner,
                     and (2, 2) is in the bottom right corner. x is the row, and y is the column.
        :return: True if game is won, False otherwise.
        """
        x, y = move
        three_in_row = False

        # Check row and column of most recent move
        vertical_sum = np.sum(self.array_board[:, y])
        horizontal_sum = np.sum(self.array_board[x, :])
        sums = [vertical_sum, horizontal_sum]

        # Check diagonal (if applicable)
        if (y == x):
            diag1_sum = [np.trace(self.array_board)]
            sums.append(diag1_sum)
        if (y == -x + self.n - 1):
            diag2_sum = [np.trace(np.flip(self.array_board, axis=1))]
            sums.append(diag2_sum)
        for vals in sums:
            if (self.n in vals) or (-self.n in vals):
                three_in_row = True
                break

        # Terminate game if board is full or player has won
        if self.num_moves == 9 or three_in_row:
            self.terminated = True
            if three_in_row and self.turn_is_X:
                print(f'X has won!')
            elif three_in_row and not self.turn_is_X:
                print(f'O has won!')
            else:
                print('It\'s a draw! Game over!')
