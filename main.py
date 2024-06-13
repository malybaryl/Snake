import customtkinter as ctk
import tkinter as tk
from constants import *
import variables
from random import choice
from sys import exit
import os

class Game(ctk.CTk):
    def __init__(self):
        try:
            super().__init__()
            self.title('Snake')
            self.geometry(f'{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}')
            self.resizable(False, False)
            
            self.canvas = ctk.CTkCanvas(self, width=GRID_SIZE * FIELDS[0], height=GRID_SIZE * FIELDS[1], bg=BACKGROUND_COLOR, highlightbackground='black')
            self.canvas.pack()
            
            if os.path.exists('assets/icon/icon.ico'):
                self.iconbitmap('assets/icon/icon.ico')
            else:
                print("Icon file not found. Continuing without custom icon.")
            
            ctk.set_appearance_mode('dark')
            
            self.menu = variables.menu
            self.animation_id = None
            
            self.bind('<Key>', self.get_input)
            
            if self.menu:
                self.show_menu()
            else:
                self.start_game()
            
            self.mainloop()
        except Exception as e:
            print(f"Failed to initialize the game: {e}")
            exit()
    
    def show_menu(self):
        self.GameLogo = ctk.CTkLabel(self.canvas, text='SNAKE', font=ctk.CTkFont(family='Modern', size=106, weight='bold'))
        self.GameLogo.place(relx=0.5, rely=0.25, anchor='center')
        
        self.option_canvas = ctk.CTkCanvas(self.canvas, bg=BACKGROUND_COLOR)
        
        self.selected_option = tk.StringVar()  # Tworzenie zmiennej dla radiobuttonów
        
        self.radio_button_easy_mode = ctk.CTkRadioButton(self.option_canvas, command=self.radio_button_game_mode, text='easy', variable=self.selected_option, value='easy')
        self.radio_button_normal_mode = ctk.CTkRadioButton(self.option_canvas, command=self.radio_button_game_mode, text='normal', variable=self.selected_option, value='normal')
        self.radio_button_hard_mode = ctk.CTkRadioButton(self.option_canvas, command=self.radio_button_game_mode, text='hard', variable=self.selected_option, value='hard')
        
        # Ustawienie domyślnej opcji wyboru na normal
        self.selected_option.set('normal')
        variables.refresh_rate = variables.refresh_rates['normal']
        
        self.radio_button_easy_mode.pack(side='left')
        self.radio_button_normal_mode.pack(side='left')
        self.radio_button_hard_mode.pack(side='left')
        
        self.option_canvas.place(relx=0.53, rely=0.5, anchor='center') 

        self.press_space_to_continue = ctk.CTkLabel(self.canvas, text='PRESS "SPACE" TO START THE GAME', font=ctk.CTkFont(family='Modern', size=26, weight='bold'))
        self.press_space_to_continue.place(relx=0.5, rely=0.85, anchor='center')

    def radio_button_game_mode(self):
        selected_mode = self.selected_option.get()
        if selected_mode in variables.refresh_rates:
            variables.refresh_rate = variables.refresh_rates[selected_mode]
        else:
            print(f"Unsupported game mode: {selected_mode}")

    def start_game(self):
        if self.animation_id:
            self.after_cancel(self.animation_id)
        
        # clear canvas
        self.canvas.delete("all")
        
        # clear menu labels if they exist
        try:
            self.GameLogo.place_forget()
            self.press_space_to_continue.place_forget()
            self.option_canvas.place_forget()
        except AttributeError:
            pass
        
        # snake
        self.snake = [START_POS, (START_POS[0] - 1, START_POS[1]), (START_POS[0] - 2, START_POS[1])]
        self.direction = DIRECTIONS['right']
        
        # apple
        self.apple_position = ()
        self.place_apple()
        
        # draw logic
        self.animate()
    
    def animate(self):
        try:
            if self.snake:
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
                # looping game (refresh every 200 ms)
                self.animation_id = self.after(variables.refresh_rate, self.animate)
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
        if self.snake:
            snake_head = self.snake[0]
            if (snake_head[0] >= FIELDS[0] or snake_head[1] >= FIELDS[1] or
                snake_head[0] < 0 or snake_head[1] < 0 or
                snake_head in self.snake[1:]):
                print("Game Over")
                self.menu = True
                variables.menu = True
                self.snake = []  # Clear the snake
                self.apple_position = ()  # Clear the apple position
                self.canvas.delete("all")  # Clear canvas
                self.show_menu()
                self.after_cancel(self.animation_id)  # Stop the game loop
    
    def get_input(self, event):
        if self.menu:
            if event.keycode == 32:  # space
                print("Pressed Space")
                variables.menu = False
                self.menu = False
                self.start_game()
        else:
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
        
        # draw apple if it exists
        if self.apple_position:
            x1, y1 = self.apple_position[0] * GRID_SIZE, self.apple_position[1] * GRID_SIZE
            x2, y2 = x1 + GRID_SIZE, y1 + GRID_SIZE
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=APPLE_COLOR, outline='')
        
        # draw snake if it exists
        if self.snake:
            for index, position in enumerate(self.snake):
                x1, y1 = position[0] * GRID_SIZE, position[1] * GRID_SIZE
                x2, y2 = x1 + GRID_SIZE, y1 + GRID_SIZE
                color = SNAKE_BODY_COLOR if index != 0 else SNAKE_HEAD_COLOR
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')

if __name__ == '__main__':
    Game()
