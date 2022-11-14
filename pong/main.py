import sys
import time
import pygame
import numpy as np

from dataclasses import dataclass

# PYGAME
from pygame.locals import QUIT

pygame.init()
pygame.display.set_caption('Pong')

DEBUG = False

### User configuration ###
FPS = 40
BALL_SPEED = 10

if DEBUG: 
    FPS = 2
    BALL_SPEED = 0.5
    BOARD_SIZE = 15

PLAYER_1 = 1
PLAYER_2 = 2
BALL = 5
WALL = 10
WALL_SIDES = 20

BOARD_SIZE = 30 # For evert 10 add a bar to players?
BOX_SIZE = 30
MID = int(BOARD_SIZE/2)


@dataclass
class Direction():
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4

@dataclass
class Player1Direction():
    STATIC = 0
    UP = 1
    DOWN = 2

@dataclass
class Player2Direction():
    STATIC = 0
    UP = 1
    DOWN = 2

# Init Pygame
CLOCK = pygame.time.Clock()
WINDOW = pygame.display.set_mode((BOX_SIZE*BOARD_SIZE, BOX_SIZE*BOARD_SIZE))
WINDOW.fill((0,0,0))

class Pong():
    def __init__(self):
        # self.map
        self.map = np.zeros((BOARD_SIZE,BOARD_SIZE),dtype=np.int8)
        self.map[[0,-1],2:-2] = WALL
        self.map[:,[0,-1]] = WALL_SIDES
        self.map[MID+1,MID+1] = BALL
        self.map[MID-2:MID+3,1] = PLAYER_1
        self.map[MID-2:MID+3,-2] = PLAYER_2

        self.index_ball = np.where(self.map == BALL)

        self.player1_direction = Player1Direction.STATIC
        self.player2_direction = Player2Direction.STATIC
        self.direction = [Direction.DOWN, Direction.RIGHT]

        self.score_player1 = 0
        self.score_player2 = 0
    
    def move_player(self):
        " Move player x up or down"
        if len(np.where(self.map[0,1] == 1)[0]) > 0 and self.player1_direction == 1: self.player1_direction = 0
        elif len(np.where(self.map[-1,1] == 1)[0]) > 0 and self.player1_direction == 2: self.player1_direction = 0
        #print(f"{self.player1_direction}")

        if len(np.where(self.map[0,-2] == 2)[0]) > 0 and self.player2_direction == 1: self.player2_direction = 0
        elif len(np.where(self.map[-1,-2] == 2)[0]) > 0 and self.player2_direction == 2: self.player2_direction = 0 

        # Move player 1
        if self.player1_direction > 0 :
            player_position = np.where(self.map == 1)
            self.map[player_position[0],player_position[1][0]] = 0 # Clear old position
            if self.player1_direction == 1: self.map[player_position[0]-1,player_position[1][0]] = 1
            if self.player1_direction == 2: self.map[player_position[0]+1,player_position[1][0]] = 1

         # Move player 2
        if self.player2_direction > 0 :
            player_position = np.where(self.map == 2)
            self.map[player_position[0],player_position[1][0]] = 0 # Clear old position
            if self.player2_direction == 1: self.map[player_position[0]-1,player_position[1][0]] = 2
            if self.player2_direction == 2: self.map[player_position[0]+1,player_position[1][0]] = 2        

    def render_graphics(self, color, index, box_size=BOX_SIZE):
        for i in range(len(index[0])):
            pygame.draw.rect(WINDOW, color, pygame.Rect(index[1][i]*box_size, index[0][i]*box_size, box_size, box_size))


    def _render_score(self,size=BOX_SIZE, text_color=(255,255,255)):
        Font=pygame.font.SysFont('Aerial', size)
        WINDOW.blit(Font.render(f"Score: {self.score_player1}", False, text_color),(10,10))
        # BUG: Hardcoded left player score (player2)
        WINDOW.blit(Font.render(f"Score: {self.score_player2}", False, text_color),(BOX_SIZE*BOARD_SIZE - 100/1.1,10))
    
    #def render_graphics_ball(self, color, index, box_size=BOX_SIZE):
    #    for i in range(len(index[0])):
    #        pygame.draw.circle(WINDOW, color, (index[1][i]*box_size, index[0][i]*box_size), box_size/2)
    
    def get_ball_position(self):
        for i in [5,6,7,15]:#,101,102]:
            if i in self.map: 
                self.index_ball = np.where(self.map == i)

    # Remove hardcoded when tested
    def game_logic(self):
        # Check wall hits
        if 15 in self.map:
            if Direction.DOWN == self.direction[0]: self.direction[0] = Direction.UP
            else: self.direction[0] = Direction.DOWN      

        if 6 == self.map[0,1] or 6 == self.map[-1,1] or 7 == self.map[0,-2] or 7 == self.map[-1,-2]: # Edge case
            print("Edge case!")
            if Direction.DOWN == self.direction[0]: self.direction[0] = Direction.UP
            else: self.direction[0] = Direction.DOWN
            if Direction.RIGHT == self.direction[1]: self.direction[1] = Direction.LEFT
            else: self.direction[1] = Direction.RIGHT

        elif 6 in self.map or 7 in self.map:
            if Direction.RIGHT == self.direction[1]: self.direction[1] = Direction.LEFT
            else: self.direction[1] = Direction.RIGHT
        
    
    #def move_ball(self):  
    #    if Direction.RIGHT == self.direction[1] and Direction.DOWN == self.direction[0]: self.map[self.index_ball[0]+1,self.index_ball[1]+1] += 5
    #    if Direction.LEFT == self.direction[1] and Direction.DOWN == self.direction[0]: self.map[self.index_ball[0]+1,self.index_ball[1]-1] += 5
    #    if Direction.RIGHT == self.direction[1] and Direction.UP == self.direction[0]: self.map[self.index_ball[0]-1,self.index_ball[1]+1] += 5
    #    if Direction.LEFT == self.direction[1] and Direction.UP == self.direction[0]: self.map[self.index_ball[0]-1,self.index_ball[1]-1] += 5
    #    
    #    # Recovering old positions when hitting something
    #    if self.map[self.index_ball[0],self.index_ball[1]][0] == 5:   
    #        self.map[self.index_ball[0],self.index_ball[1]] = 0
#
    #    elif self.map[self.index_ball[0],self.index_ball[1]][0] == 6:   
    #        self.map[self.index_ball[0],self.index_ball[1]] = 1
    #    
    #    elif self.map[self.index_ball[0],self.index_ball[1]][0] == 7:   
    #        self.map[self.index_ball[0],self.index_ball[1]] = 2
    #        
    #    elif self.map[self.index_ball[0],self.index_ball[1]][0] == 15:   
    #        self.map[self.index_ball[0],self.index_ball[1]] = 10
    #    
    #    else:
    #        print("BUG: Unknown")

    def move_ball(self):  
        if Direction.RIGHT == self.direction[1] and Direction.DOWN == self.direction[0]: self.map[self.index_ball[0]+1,self.index_ball[1]+1] += 5
        if Direction.LEFT == self.direction[1] and Direction.DOWN == self.direction[0]: self.map[self.index_ball[0]+1,self.index_ball[1]-1] += 5
        if Direction.RIGHT == self.direction[1] and Direction.UP == self.direction[0]: self.map[self.index_ball[0]-1,self.index_ball[1]+1] += 5
        if Direction.LEFT == self.direction[1] and Direction.UP == self.direction[0]: self.map[self.index_ball[0]-1,self.index_ball[1]-1] += 5
        
        # Recovering old positions when hitting something
        if self.map[self.index_ball[0],self.index_ball[1]][0] == 5:   
            self.map[self.index_ball[0],self.index_ball[1]] = 0

        
    def hax2(self):
        if self.map[self.index_ball[0],self.index_ball[1]][0] == 6:   
            self.map[self.index_ball[0],self.index_ball[1]] = 1
        
        elif self.map[self.index_ball[0],self.index_ball[1]][0] == 7:   
            self.map[self.index_ball[0],self.index_ball[1]] = 2
            
        elif self.map[self.index_ball[0],self.index_ball[1]][0] == 15:   
            self.map[self.index_ball[0],self.index_ball[1]] = 10
        
        #else: # Due to fps diff with ball to player this prints to often noe, ignore for now
          #  print("BUG: Unknown")

    def game(self):
        gaming = True
        hax = 0
        while gaming:
            hax += 1
            for event in pygame.event.get():
                if event.type == QUIT:
                    print(f"Game over - Final score: {99}")   
                    pygame.quit()
                    sys.exit()
 
                
            if not 6 in self.map or 7 in self.map:
                keys = pygame.key.get_pressed()
                #print(keys[pygame.K_DOWN])
                if keys[pygame.K_w]: self.player1_direction = Player1Direction.UP
                elif keys[pygame.K_s]: self.player1_direction = Player1Direction.DOWN
                else: self.player1_direction = Player1Direction.STATIC
                if keys[pygame.K_UP]: self.player2_direction = Player2Direction.UP
                elif keys[pygame.K_DOWN]: self.player2_direction = Player2Direction.DOWN
                else: self.player2_direction = Player2Direction.STATIC

            else:
                self.player1_direction = Player1Direction.STATIC
                self.player2_direction = Player2Direction.STATIC
            
            self.move_player()

            #print(self.map)
            self.get_ball_position() # Getting on to many frames
            self.game_logic()

            
            if DEBUG: 
                self.move_ball()

            else:
                if hax%(FPS/BALL_SPEED) == 0:
                    self.move_ball()

            self.hax2()

            # HAX SCORE 
            if 6 in self.map:
                self.score_player1 += 1
            if 7 in self.map:
                self.score_player2 += 1

            self._render_score()
            self.render_graphics((50,50,50),np.where(self.map == 1))
            self.render_graphics((50,50,50),np.where(self.map == 2))

            self.render_graphics((50,100,50),np.where(self.map == 5))
            self.render_graphics((50,100,50),np.where(self.map == 6))
            self.render_graphics((50,100,50),np.where(self.map == 7))
            self.render_graphics((50,100,50),np.where(self.map == 15))

            #self.render_graphics((255,255,255),np.where(self.map == 10))
            #self.render_graphics((128,200,200),np.where(self.map == 20))
            self.render_graphics((255,0,0),np.where(self.map == 25))

            self._render_score()
            # Refresh game
            pygame.display.flip()
            CLOCK.tick(FPS)
            WINDOW.fill((0,0,0))

            if 25 in self.map:
                print("Game over")
                gaming = False


if __name__ == '__main__':
    game = Pong()
    game.game()
    time.sleep(20)
