import random
from copy import deepcopy


class Game:
    won: bool = False
    turn: int = 0
    grid: list = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

    def __init__(self):
        self.won = False
        self.turn = 0
        self.grid = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        again: str = "Y"

        while again.upper() == "Y":
            self.game_loop()
            print("PLAY AGAIN? Y/N")
            again = input()

    def game_loop(self) -> None:
        self.grid = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.won = False
        self.turn = 0
        player_turn = lambda x: (x % 2)

        while not self.won and self.turn <= 9:
            if player_turn(self.turn) == 0:
                self.human_place("X")
                self.won = self.detect_win("X", self.grid)
            else:
                self.ai_place("O")
                self.won = self.detect_win("O", self.grid)
                self.display_grid()
            self.turn += 1

        self.won = self.detect_win("X", self.grid)
        self.won = self.detect_win("O", self.grid)
        self.display_grid()
        if player_turn(self.turn - 1) == 1:
            print("YOU LOST")
        else:
            print("YOU WON")

        if self.turn > 9 and not self.won:
            print("DRAW")

    def human_place(self, player_piece: str) -> None:
        valid_placement = False
        while not valid_placement:
            print("PLEASE ENTER A ROW")
            row = self.take_input()
            print("PLEASE ENTER A COLUMN")
            column = self.take_input()
            if self.grid[row][column] == " ":
                valid_placement = True
                self.grid[row][column] = player_piece
            else:
                print("INVALID SPACE")

    def take_input(self) -> int:
        """
        takes input from user and verifies the value as an integer and within the range of 1 and 3
        converts this value to an index
        :return:
        """
        valid = False
        while not valid:
            value: int = int(input())
            if 1 <= value <= 3:
                valid = True
            else:
                print("INVALID INPUT")
        return value - 1

    def ai_place(self, computer_piece: str) -> None:
        optimal_moves: list = self.find_optimal_move(computer_piece)
        move_found: bool = False
        for move in optimal_moves:
            if self.grid[move[0]][move[1]] == " ":
                self.grid[move[0]][move[1]] = computer_piece
                move_found = True
                break
        if not move_found:
            valid_placement = False
            while not valid_placement:
                row = random.randint(0, 2)
                column = random.randint(0, 2)
                if self.grid[row][column] == " ":
                    valid_placement = True
                    self.grid[row][column] = computer_piece

    def display_grid(self) -> None:
        """
        iterate through values in grid and print a traditional noughts and crosses grid
        value at centre of row should be surrounded by | characters, can be adapted to any size grid
        :return:
        """
        for row in self.grid:
            row_to_print = ""
            for i in range(len(row)):
                row_to_print += row[i]
                if i != len(row) - 1:
                    row_to_print += "|"
            print(row_to_print)
            self.construct_horizontal()

    def construct_horizontal(self) -> None:
        print("-----")

    def find_optimal_move(self, computer_piece: str, opponent_piece: str = "X") -> list:
        """
        to find optimal move, find any possible opponent wins, then look for possible AI wins
        opponent wins should be prioritised so prepended to the output list, opponent wins can be appended
        :param opponent_piece:
        :param computer_piece:
        :return:
        """
        moves: list = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                list_copy:list = deepcopy(self.grid)
                list_copy[i][j] = opponent_piece
                if self.detect_win(opponent_piece, list_copy):
                    moves = [(i,j)] + moves

                list_copy = deepcopy(self.grid)
                list_copy[i][j] = computer_piece
                if self.detect_win(computer_piece, list_copy):
                    moves.append((i,j))

        return moves

    def detect_win(self, player_symbol: str, grid: list) -> bool:
        """
        check all possible horizontal wins, followed by vertical wins, followed by diagonal wins
        :param grid:
        :param player_symbol:
        :return:
        """
        #horizontal
        for i in range(0, len(grid) - 1):
            found: bool = True
            for symbol in grid[i]:
                if symbol != player_symbol:
                    found = False
            if found:
                return True

        #vertical
        for i in range(0, len(grid[0]) -1):
            found: bool = True
            for row in grid:
                if row[i] != player_symbol:
                    found = False
            if found:
                return True

        #standard diagonal
        found: bool = True
        for i in range(0, len(grid)):
            if grid[i][i] != player_symbol:
                found = False
        if found:
            return True

        #reverse diagonal
        found: bool = True
        for i in range(0, len(grid)):
            if grid[i][(len(grid)-1)-i] != player_symbol:
                found = False
        if found:
            return True

        return False

new_game: Game = Game()
