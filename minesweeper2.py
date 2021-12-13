'''
create a minesweeper game
#create a board
#create mines
#create flags
#create a gui

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
        self.nodes = dict()
        self.clicked = set()
        self.setup(mines)

    def setup(self, mines):
        for x in range(self.width):
            for y in range(self.height):
                self.nodes[(x, y)] = Node(x, y)

        while len(self.mines) != mines:
            x = random.randint(0, self.width-1)
            y = random.randint(0, self.height-1)
            if (x, y) not in self.mines:
                self.mines.add((x, y))
                self.nodes[(x, y)].is_mine = True

        for x in range(self.width):
            for y in range(self.height):
                self.nodes[(x, y)].add_neighbors(self.nodes, self.width, self.height)

    def click(self, x, y):
        self.clicked.add((x, y))
        node = self.nodes[(x, y)]
        if node.is_mine:
            return True
        else:
            node.click(self.nodes)
            return False

    def flag(self, x, y):
        self.flags.add((x, y))

    def unflag(self, x, y):
        self.flags.remove((x, y))

    def is_solved(self):
        if self.width * self.height - len(self.flags) == len(self.mines):
            return True
        else:
            return False

    def draw(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                self.nodes[(x, y)].draw(screen)

class Node:

    def __init__(self, x, y, is_mine=False):
        self.x = x
        self.y = y
        self.is_mine = is_mine
        self.is_clicked = False
        self.is_flagged = False
        self.neighbors = set()

    def add_neighbors(self, nodes, width, height):
        for x in range(self.x-1, self.x+2):
            for y in range(self.y-1, self.y+2):
                if x >= 0 and x < width and y >= 0 and y < height and (x, y) != (self.x, self.y):
                    self.neighbors.add(nodes[(x, y)])

    def click(self, nodes):
        self.is_clicked = True
        if self.is_mine:
            return True
        else:
            if len(self.neighbors) == 0:
                for neighbor in self.neighbors:
                    if not neighbor.is_clicked:
                        neighbor.click(nodes)

    def draw(self, screen):
        x = self.x * 20 + 1
        y = self.y * 20 + 1
        if self.is_clicked:
            pygame.draw.rect(screen, (255, 255, 255), (x, y, 19, 19))
            if self.is_mine:
                pygame.draw.circle(screen, (255, 0, 0), (x+10, y+10), 5)
            else:
                pygame.draw.rect(screen, (0, 0, 0), (x+1, y+1, 18, 18))
                if len(self.neighbors) != 0:
                    pygame.draw.rect(screen, (255, 255, 255), (x+1, y+1, 18, 18), 1)
                    font = pygame.font.SysFont("comicsansms", 15)
                    text = font.render(str(len(self.neighbors)), True, (0, 0, 0))
                    screen.blit(text, (x+9-text.get_width()/2, y+9-text.get_height()/2))
        elif self.is_flagged:
            pygame.draw.rect(screen, (0, 0, 0), (x, y, 19, 19))
            pygame.draw.polygon(screen, (255, 0, 0), ((x+10, y), (x+10, y+10), (x+20, y+10)))
        else:
            pygame.draw.rect(screen, (0, 0, 0), (x, y, 19, 19), 1)

def main():
    width = 10
    height = 10
    mines = 20
    if len(sys.argv) > 1:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        mines = int(sys.argv[3])
    game = Minesweeper(width, height, mines)
    pygame.init()
    screen = pygame.display.set_mode((width*20+1, height*20+1))
    pygame.display.set_caption("Minesweeper")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x = x // 20
                y = y // 20
                if event.button == 1:
                    if game.click(x, y):
                        running = False
                elif event.button == 3:
                    game.flag(x, y)
        screen.fill((255, 255, 255))
        game.draw(screen)
        if game.is_solved():
            font = pygame.font.SysFont("comicsansms", 50)
            text = font.render("You Win!", True, (0, 255, 0))
            screen.blit(text, (screen.get_width()/2-text.get_width()/2, screen.get_height()/2-text.get_height()/2))
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()