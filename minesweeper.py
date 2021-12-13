'''
create a minesweeper game
#create a board
#create mines
#create flags

'''


import random
import sys
import time
import pygame

class Minesweeper:
    def __init__(self, width=10, height=10, mines=10):
        self.width = width
        self.height = height
        self.mines = set()
        self.flags = set()
        self.nodes = set()
        self.exposed_nodes = set()
        self.game_over = False
        self.start_time = None
        self.end_time = None
        self.mines_hit = False
        self.setup_game(mines)

    def setup_game(self, mines):
        #initialize the game
        for x in range(self.width):
            for y in range(self.height):
                self.nodes.add((x, y))
        while len(self.mines) != mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) not in self.mines:
                self.mines.add((x, y))
        for node in self.nodes:
            if node in self.mines:
                continue
            count = 0
            for x in range(node[0] - 1, node[0] + 2):
                for y in range(node[1] - 1, node[1] + 2):
                    if (x, y) in self.mines:
                        count += 1
            self.nodes.remove(node)
            self.nodes.add((node[0], node[1], count))

    def print_board(self):
        #print the board
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.mines:
                    print("*", end=" ")
                elif (x, y) in self.flags:
                    print("F", end=" ")
                elif (x, y) in self.exposed_nodes:
                    print(self.nodes.get((x, y))[2], end=" ")
                else:
                    print("-", end=" ")
            print()

    def expose_node(self, x, y):
        #expose a node
        if (x, y) in self.exposed_nodes:
            return
        self.exposed_nodes.add((x, y))
        node = self.nodes.get((x, y))
        if node[2] == 0:
            for x in range(x - 1, x + 2):
                for y in range(y - 1, y + 2):
                    if (x, y) in self.nodes:
                        self.expose_node(x, y)

    def check_for_loss(self):
        #check if the game is over
        for x in range(self.width):
            for y in range(self.height):
                if (x, y) in self.mines and (x, y) in self.exposed_nodes:
                    self.game_over = True
                    self.mines_hit = True
                    return
        if len(self.exposed_nodes) == (self.width * self.height) - len(self.mines):
            self.game_over = True
            return

    def flag_node(self, x, y):
        #flag a node
        if (x, y) in self.flags:
            self.flags.remove((x, y))
        else:
            self.flags.add((x, y))

    def play_game(self):
        #play the game
        self.start_time = time.time()
        while not self.game_over:
            self.print_board()
            print("\nEnter the coordinates of the node you want to expose (x, y):")
            x = int(input("x: "))
            y = int(input("y: "))
            self.expose_node(x, y)
            self.check_for_loss()
        self.end_time = time.time()
        self.print_board()
        if self.mines_hit:
            print("You lose!")
        else:
            print("You win!")
        print("It took you", round(self.end_time - self.start_time, 2), "seconds to complete the game.")

def main():
    #main function
    print("Welcome to Minesweeper!")
    print("Enter the size of the board (width, height):")
    width = int(input("width: "))
    height = int(input("height: "))
    print("Enter the number of mines:")
    mines = int(input("mines: "))
    game = Minesweeper(width, height, mines)
    game.play_game()

if __name__ == "__main__":
    main()