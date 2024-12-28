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

        # Array representation of board, where "X" = 1, "O" = -1, and " " = 0
        self.array_board: np.array = np.zeros((3, 3), dtype=int)

        # TODO: randomize who gets the first turn via "coin flip"
        #       OR use game of rock-paper-scissors
        self.turn_is_X: bool = True
        self.cpu: str = "X"
        self.terminated: bool = False

        self.neighbors = []
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if not (x == 0 and y == 0):
                    self.neighbors.append((x, y))
        # print(self.neighbors)

        print('X goes first!')


    def step(self) -> None:
        pass


    def render(self) -> None:
        """
        Renders current state of board.
        """
        mid_line = ["---" for i in range(len(self.board))]
        mid_line = "-".join(mid_line)

        for i in range(len(self.board)):
            line = f" {self.board[i][0]}"
            for j in range(1, len(self.board)):
                line += f" | {self.board[i][j]}"

            # Print values on board and dividing line
            print(line)
            if i < len(self.board) - 1:
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
            self.turn_is_X = not self.turn_is_X
        else:
            raise ValueError(f"The move {move} is not a valid move. Try again.")

        self.check_if_won(move)


    def in_board(self, position: tuple[int]) -> bool:
        """
        Given tuple representing position on board, returns True if position is
        on board, and False if outside bounds of board.

        :param position: tuple of (x, y) coordinate for board position, where (0, 0) is in the top left corner,
                         and (2, 2) is in the bottom right corner. x is the row, and y is the column.
        :return: True if position is in board, False otherwise.
        """
        x, y = position
        in_height = x >= 0 and x < len(self.board)
        in_width = y >= 0 and y < len(self.board)
        in_board = in_height and in_width

        if not in_board:
            raise ValueError(f"The position {position} is not in the board!")
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


    def check_if_won(self, move: tuple[int]) -> None:
        """
        Given player's most recent move, returns True if player has won, False otherwise.

        :param move: tuple of (x, y) coordinate for desired move, where (0, 0) is in the top left corner,
                     and (2, 2) is in the bottom right corner. x is the row, and y is the column.
        :return: True if game is won, False otherwise.
        """
        # Check if 3 in a row, update self.game_over
        # TODO: optimize checks-- only need to check the lines that the move is on
        vertical_sum = np.sum(self.array_board, axis=0)
        horizontal_sum = np.sum(self.array_board, axis=1)
        diag1_sum = [np.trace(self.array_board)]
        diag2_sum = [np.trace(np.flip(self.array_board, axis=1))]

        sums = [vertical_sum, horizontal_sum, diag1_sum, diag2_sum]
        for vals in sums:
            if (len(self.board) in vals) or (-len(self.board) in vals):
                self.terminated = True
                break

        if self.terminated:
            if self.turn_is_X:
                print(f'X has won! Better luck next time!')
            else:
                print(f'O has won! Congratulations!')
