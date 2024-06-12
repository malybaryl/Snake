import customtkinter as ctk
from constants import *
from random import choice
from sys import exit
import os

class Game(ctk.CTk):
    def __init__(self):
        try:
            # setup
            super().__init__()
            self.title('Snake')
            self.geometry(f'{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}')
            self.resizable(False,False)
            
            
            self.canvas = ctk.CTkCanvas(self, width=GRID_SIZE * FIELDS[0], height=GRID_SIZE * FIELDS[1], bg=BACKGROUND_COLOR, highlightbackground='black')
            self.canvas.pack()
            
            if os.path.exists('assets/icon/icon.ico'):
                self.iconbitmap('assets/icon/icon.ico')
            else:
                print("Icon file not found. Continuing without custom icon.")
            
            ctk.set_appearance_mode('dark')
            
            # snake
            self.snake = [START_POS, (START_POS[0] - 1, START_POS[1]), (START_POS[0] - 2, START_POS[1])]
            self.direction = DIRECTIONS['right']
            
            self.bind('<Key>', self.get_input)
            
            # apple
            self.apple_position = ()
            self.place_apple()
            
            # draw logic
            self.animate()
            
            # run
            self.mainloop()
        except Exception as e:
            print(f"Failed to initialize the game: {e}")
            exit()
    
    def animate(self):
        try:
            # create new head new head = old head + direction
            new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
            self.snake.insert(0, new_head)
            
            # apple collision
            if self.snake[0] == self.apple_position:
                self.place_apple()
            else:
                # remove last part of the snake
                self.snake.pop()
            
            self.check_game_over()
            
            # drawing
            self.draw()
            # looping game (refresh every 100 ms)
            self.after(200, self.animate)
        except Exception as e:
            print(f"Game loop error: {e}")
            exit()
    
    def place_apple(self):
        possible_positions = [(x, y) for x in range(FIELDS[0]) for y in range(FIELDS[1])]
        for part in self.snake:
            if part in possible_positions:
                possible_positions.remove(part)
        self.apple_position = choice(possible_positions)
    
    def check_game_over(self):
        snake_head = self.snake[0]
        if (snake_head[0] >= RIGHT_LIMIT or snake_head[1] >= DOWN_LIMIT or
            snake_head[0] <= LEFT_LIMIT or snake_head[1] <= UP_LIMIT or
            snake_head in self.snake[1:]):
            print("Game Over")
            exit()
    
    def get_input(self, event):
        if event.keycode == 37 and self.direction != DIRECTIONS['right']:  # left arrow
            self.direction = DIRECTIONS['left']
            return
        elif event.keycode == 65 and self.direction != DIRECTIONS['right']:  # a
            self.direction = DIRECTIONS['left']
            return
        elif event.keycode == 38 and self.direction != DIRECTIONS['down']:  # up arrow
            self.direction = DIRECTIONS['up']
            return
        elif event.keycode == 87 and self.direction != DIRECTIONS['down']:  # w
            self.direction = DIRECTIONS['up']
            return
        elif event.keycode == 39 and self.direction != DIRECTIONS['left']:  # right arrow
            self.direction = DIRECTIONS['right']
            return
        elif event.keycode == 68 and self.direction != DIRECTIONS['left']:  # d
            self.direction = DIRECTIONS['right']
            return
        elif event.keycode == 40 and self.direction != DIRECTIONS['up']:  # down arrow
            self.direction = DIRECTIONS['down']
            return
        elif event.keycode == 83 and self.direction != DIRECTIONS['up']:  # s
            self.direction = DIRECTIONS['down']
            return
           
    def draw(self):
        self.canvas.delete("all")  # Clear previous drawings
        
        # draw apple
        x1, y1 = self.apple_position[0] * GRID_SIZE, self.apple_position[1] * GRID_SIZE
        x2, y2 = x1 + GRID_SIZE, y1 + GRID_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=APPLE_COLOR, outline='')
        
        # draw snake
        for index, position in enumerate(self.snake):
            x1, y1 = position[0] * GRID_SIZE, position[1] * GRID_SIZE
            x2, y2 = x1 + GRID_SIZE, y1 + GRID_SIZE
            color = SNAKE_BODY_COLOR if index != 0 else SNAKE_HEAD_COLOR
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')

if __name__ == '__main__':
    Game()
