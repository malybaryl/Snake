import customtkinter as ctk
import tkinter as tk
import variables
import os
import constants 
from random import randint
from random import choice
from sys import exit


class Game(ctk.CTk):
    def __init__(self):
        try:
            super().__init__()
            self.title('Snake')
            self.geometry(f'{constants.WINDOW_SIZE[0]}x{constants.WINDOW_SIZE[1]}')
            self.resizable(False, False)
            
            self.canvas = ctk.CTkCanvas(self, width=constants.GRID_SIZE * constants.FIELDS[0], height=constants.GRID_SIZE * constants.FIELDS[1], bg=constants.BACKGROUND_COLOR, highlightbackground='black')
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
        
        self.option_canvas = ctk.CTkCanvas(self.canvas, bg=constants.BACKGROUND_COLOR)
        
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
        
        self.version_text = ctk.CTkLabel(self.canvas, text=constants.VERSION, font=ctk.CTkFont(family='Modern', size=12, weight='bold'))
        self.version_text.place(relx=0.70, rely=0.41, anchor='se')

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
            self.version_text.place_forget()
        except AttributeError:
            pass
        
        # snake
        self.snake = [constants.START_POS, (constants.START_POS[0] - 1, constants.START_POS[1]), (constants.START_POS[0] - 2, constants.START_POS[1])]
        self.direction = constants.DIRECTIONS['right']
        
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
        possible_positions = [(x, y) for x in range(constants.FIELDS[0]) for y in range(constants.FIELDS[1])]
        for part in self.snake:
            if part in possible_positions:
                possible_positions.remove(part)
        self.apple_position = choice(possible_positions)
    
    def check_game_over(self):
        if self.snake:
            snake_head = self.snake[0]
            if (snake_head[0] >= constants.FIELDS[0] or snake_head[1] >= constants.FIELDS[1] or
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
                constants.START_POS = (randint(3, constants.FIELDS[0] - 3), randint(3, constants.FIELDS[1] - 3))
                self.start_game()
        else:
            if event.keycode == 37 and self.direction != constants.DIRECTIONS['right']:  # left arrow
                self.direction = constants.DIRECTIONS['left']
                return
            elif event.keycode == 65 and self.direction != constants.DIRECTIONS['right']:  # a
                self.direction = constants.DIRECTIONS['left']
                return
            elif event.keycode == 38 and self.direction != constants.DIRECTIONS['down']:  # up arrow
                self.direction = constants.DIRECTIONS['up']
                return
            elif event.keycode == 87 and self.direction != constants.DIRECTIONS['down']:  # w
                self.direction = constants.DIRECTIONS['up']
                return
            elif event.keycode == 39 and self.direction != constants.DIRECTIONS['left']:  # right arrow
                self.direction = constants.DIRECTIONS['right']
                return
            elif event.keycode == 68 and self.direction != constants.DIRECTIONS['left']:  # d
                self.direction = constants.DIRECTIONS['right']
                return
            elif event.keycode == 40 and self.direction != constants.DIRECTIONS['up']:  # down arrow
                self.direction = constants.DIRECTIONS['down']
                return
            elif event.keycode == 83 and self.direction != constants.DIRECTIONS['up']:  # s
                self.direction = constants.DIRECTIONS['down']
                return
    
    def draw(self):
        self.canvas.delete("all")  # Clear previous drawings
        
        # draw apple if it exists
        if self.apple_position:
            x1, y1 = self.apple_position[0] * constants.GRID_SIZE, self.apple_position[1] * constants.GRID_SIZE
            x2, y2 = x1 + constants.GRID_SIZE, y1 + constants.GRID_SIZE
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=constants.APPLE_COLOR, outline='')
        
        # draw snake if it exists
        if self.snake:
            for index, position in enumerate(self.snake):
                x1, y1 = position[0] * constants.GRID_SIZE, position[1] * constants.GRID_SIZE
                x2, y2 = x1 + constants.GRID_SIZE, y1 + constants.GRID_SIZE
                color = constants.SNAKE_BODY_COLOR if index != 0 else constants.SNAKE_HEAD_COLOR
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')

if __name__ == '__main__':
    Game()
