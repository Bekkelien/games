import sys
import random
import pygame
import numpy as np

# PYGAME
from pygame.locals import QUIT

pygame.init()
pygame.display.set_caption('Snake')

### User configuration ###
FPS = 10
BOARD_SIZE = 20 # Minimum 10 is recommended
BOX_SIZE = 30
OBSTACLE = True

COLOR_HEAD = (0, 0, 139)
COLOR_BODY = (110,110,110)
COLOR_FOOD = (255,120,203)
COLOR_OBSTACLE = (255,120,4)
COLOR_TEXT = (0, 0, 0)

COLOR_BACKGROUND = (220,220,220)

WINDOW_WIDTH = BOX_SIZE * BOARD_SIZE
WINDOW_HEIGHT = BOX_SIZE * BOARD_SIZE

CLOCK = pygame.time.Clock()
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
WINDOW.fill(COLOR_BACKGROUND) # Fill the background ASAP

class SnakeGame():
    def __init__(self):
        self.map = np.zeros([BOARD_SIZE,BOARD_SIZE],dtype=np.int16)
        self.direction = "RIGHT"
        self.score = 0
    
    def _starting_position(self):
        self.map[int(BOARD_SIZE/2)][1] = 1
        self.map[int(BOARD_SIZE/2)][0] = 2
        self.map[int(BOARD_SIZE/2)+1][random.randint(0, BOARD_SIZE-1)] = -1 # FOOD

    def _add_obstacle(self): # TODO: Improve placement solution 
        self.map[random.randint(1, int(BOARD_SIZE/2)-1)][random.randint(2, BOARD_SIZE-3)] = -2 # Obstacle in upper half

    def _render_graphics(self, color, index, box_size=BOX_SIZE):
        pygame.draw.rect(WINDOW, color, pygame.Rect(index[1][0]*box_size, index[0][0]*box_size, box_size, box_size))
    
    def _render_text(self,index,text,size=30,text_color=COLOR_TEXT, box_size=BOX_SIZE):
        Font=pygame.font.SysFont('Aerial', size)
        WINDOW.blit(Font.render(text, False, text_color),(index[1][0]*box_size,index[0][0]*box_size))

    def _render_score(self,size=30, text_color=COLOR_TEXT):
        Font=pygame.font.SysFont('Aerial', size)
        WINDOW.blit(Font.render(f"Score: {self.score}", False, text_color),(10,10))

    # Logic for one move
    def _move_snake(self):
        self.snake_length = np.max(self.map)
        food_position = np.where(self.map == -1)
        index_head = []
        index_body = []

        # Iterate over the snake head and body
        for index in range(1,self.snake_length+1):
            # Head
            if index == 1: 
                # Remove the tail and store the index, if food is eaten this index will be the new body part else it will be discarded
                index_tail = np.where(self.map == self.snake_length)
                self.map[index_tail[0][0]][index_tail[1][0]] = 0

                # Find current position of the head
                search_index = np.where(self.map == index)
                index_head.append(search_index[0][0])
                index_head.append(search_index[1][0])

                # Set new index for snake head
                if self.direction == "UP": index_head[0] -= 1
                if self.direction == "DOWN": index_head[0] += 1
                if self.direction == "RIGHT": index_head[1] += 1
                if self.direction == "LEFT": index_head[1] -= 1
                
                # Check for valid move (Walls)
                if index_head[0] < 0 or index_head[0] >= BOARD_SIZE or index_head[1] < 0 or index_head[1] >= BOARD_SIZE:
                    print("Wall collision detected")
                    return False # GAME OVER

            # Body (TODO: Implementation is not very clean)
            elif index <= self.snake_length:
                search_index = np.where(self.map == index-1)
                index_body.append(search_index)

        # Move the snake head
        self.map[index_head[0]][index_head[1]] = 1
                
        # Check if we have eaten some food
        if  food_position[0][0] == index_head[0] and food_position[1][0] == index_head[1]:
            # Add food (-1) to valid food positions in the matrix/array
            index_valid_food_position = np.where(self.map == 0) 
            index_food = random.choice(list(zip(index_valid_food_position[0][:],index_valid_food_position[1][:])))
            self.map[index_food[0]][index_food[1]] = -1
            
            # New tail + increment score
            index_body.append(index_tail) 
            self.score += 1
            print("Food eaten")

        # Move the body and extend if food is eaten
        for index, body_n in enumerate(index_body):
            self.map[body_n[0][0]][body_n[1][0]] = index + 2
        
        if 1 not in self.map:
            print("Body collision detected")
            return False # GAME OVER
        
        if OBSTACLE and -2 not in self.map:
            print("Obstacle collision detected")
            return False # GAME OVER

        return True

    def game(self):
        self._starting_position()
        if OBSTACLE: self._add_obstacle()
        gaming = True
        while gaming:
            for event in pygame.event.get():
                if event.type == QUIT:
                    print(f"Game over - Final score: {self.score}")   
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if not direction_previous == "DOWN":
                        if event.key == pygame.K_UP: self.direction = "UP"
                    if not direction_previous == "UP":
                        if event.key == pygame.K_DOWN: self.direction = "DOWN"
                    if not direction_previous == "LEFT":
                        if event.key == pygame.K_RIGHT: self.direction = "RIGHT"
                    if not direction_previous == "RIGHT":
                        if event.key == pygame.K_LEFT: self.direction = "LEFT"

                direction_previous = self.direction

            if self._move_snake():
                # Head
                index = np.where(self.map == 1)
                self._render_graphics(COLOR_HEAD,index)

                # Body
                for index in range(1,self.snake_length):
                    self._render_graphics(COLOR_BODY,np.where(self.map == index+1))
                
                # Food
                index = np.where(self.map == -1)
                self._render_graphics(COLOR_FOOD,index)
                #self._render_text(index,"F",size=int(BOX_SIZE*1.5))

                # Obstacle
                if OBSTACLE:
                    index = np.where(self.map == -2)
                    self._render_graphics(COLOR_OBSTACLE,index)
                    #self._render_text(index,"O",size=int(BOX_SIZE*1.5))

                # Update score
                self._render_score()

                # Refresh game
                pygame.display.flip()
                CLOCK.tick(FPS)

                WINDOW.fill(COLOR_BACKGROUND)
            
            else:
                print(f"Game over | Score: {self.score}")
                gaming = False
        
if __name__ == '__main__':
    game = SnakeGame()
    game.game()
    #import time
    #time.sleep(20)
