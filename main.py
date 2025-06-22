import pygame
import sys

from bots.test import Bot as TestBot

screen_w, screen_h = 1280, 720
screen = pygame.display.set_mode((screen_w, screen_h))

clock = pygame.time.Clock()

UNIT = 40

PLAYER_2 = 2
PLAYER_1 = 1

cam_x = UNIT
cam_y = UNIT

class Board:
    def __init__(self):
        self.board = [[0]*(15+1) for _ in range(15+1)]
        self.stones = set()
        self.step = 0
        self.last_x = -1
        self.last_y = -1
        self.bots = [
            TestBot()
        ]

    def draw(self):
        pygame.draw.rect(screen, "#b0813e", [cam_x-UNIT/2, cam_y-UNIT/2, UNIT+15*UNIT, UNIT+15*UNIT])
        for y in range(15+1):
            pygame.draw.line(screen, "#222222", [cam_x, cam_y+y*UNIT], [cam_x+15*UNIT, cam_y+y*UNIT], 1)
        for x in range(15+1):
            pygame.draw.line(screen, "#222222", [cam_x+x*UNIT, cam_y], [cam_x+x*UNIT, cam_y+15*UNIT], 1)
        for y in range(15+1):
            for x in range(15+1):
                if self.board[y][x] == PLAYER_1:
                    pygame.draw.circle(screen, "#d1dfe8", [cam_x+x*UNIT, cam_y+y*UNIT], UNIT//2)
                elif self.board[y][x] == PLAYER_2:
                    pygame.draw.circle(screen, "#0e1626", [cam_x+x*UNIT, cam_y+y*UNIT], UNIT//2)
        
        if self.last_x != -1 and self.last_y != -1:
            pygame.draw.circle(screen, "#ffb330", [UNIT+self.last_x*UNIT, UNIT+self.last_y*UNIT], UNIT//2, 4)

    def make_move(self, x, y, side):
        self.board[y][x] = side
        self.stones.add((x, y))
        self.last_x = x
        self.last_y = y

    def unmake_move(self, x, y):
        self.board[y][x] = 0
        self.stones.discard((x, y))

    def get_at(self, x, y):
        return self.board[y][x]

    def move(self):
        side = self.step%2
        x, y = self.bots[side].move(self)
        self.make_move(x, y, side)
        self.step += 1

board = Board()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                board.move()
    
    screen.fill("#ffffff")

    board.draw()

    pygame.display.update()
    clock.tick(60)