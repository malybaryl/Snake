from random import randint

# window info
WINDOW_SIZE = (800, 600)
FIELDS = (20, 15)

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
SNAKE_BODY_COLOR = '#13d12c'
SNAKE_HEAD_COLOR = '#068f18'
APPLE_COLOR = '#b00c0c'