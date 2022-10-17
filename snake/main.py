import sys
import time
import random 
import pygame
from pygame.locals import QUIT

pygame.init()

# Game Setup
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
BACKGROUND = (0,0,0)

    
# Game window
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

class SnakeGame():
    def __init__(self):
        self.box_size = 50
        self.food = True
        self.x = 0 
        self.y = 0 

    def start(self):
        print("Starting Game...")
        while True:
            # Do events first
            for event in pygame.event.get():
                if event.type == QUIT:
                    print("Goodbye!")
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP: self.y -= self.box_size
                    if event.key == pygame.K_DOWN: self.y += self.box_size
                    if event.key == pygame.K_RIGHT: self.x += self.box_size
                    if event.key == pygame.K_LEFT: self.x -= self.box_size
                

            # Starting position
            if self.food:
                food_x, food_y = random.randrange(0, 500, 50), random.randrange(0, 500, 50)
                self.food = False

            food = pygame.draw.rect(WINDOW, (42, 169, 169), pygame.Rect(food_x, food_y, self.box_size, self.box_size)) # Can be same as starting position
            snake = pygame.draw.rect(WINDOW, (0, 100, 25), pygame.Rect(self.x, self.y, self.box_size, self.box_size)) 

            if food == snake:
                self.food = True

            # Update display     
            pygame.display.flip()  

            # Render elements of the game (Last)
            WINDOW.fill(BACKGROUND)

if __name__ == '__main__':
    SnakeGame().start()
