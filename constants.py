from random import randint

# game variables
GRID_SIZE = 32
FIELDS = (20, 15)

# window info
WINDOW_SIZE = (((GRID_SIZE - 6)*FIELDS[0]), ((GRID_SIZE - 6)*FIELDS[1]))

# movement
START_POS = (randint(3, FIELDS[0] - 3), randint(3, FIELDS[1 ] - 3))
DIRECTIONS = {'left': [-1,0],
              'right': [1,0],
              'up': [0,-1],
              'down': [0,1],}
RIGHT_LIMIT = FIELDS[0]
LEFT_LIMIT = -1
UP_LIMIT = -1
DOWN_LIMIT = FIELDS[1]

# colors
BACKGROUND_COLOR = '#242424'
SNAKE_BODY_COLOR = '#13d12c'
SNAKE_HEAD_COLOR = '#068f18'
APPLE_COLOR = '#b00c0c'