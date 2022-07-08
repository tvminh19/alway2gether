CHUNK_SIZE = 30


MENU_BUTTON_WIDTH = 50
MENU_BUTTON_HEIGHT = 50
FPS = 24

#therefore the screen will have 34x25 tiles
TILE_WIDTH = CHUNK_SIZE
TILE_HEIGHT = CHUNK_SIZE


COOR_WIDTH = 34 
COOR_HEIGHT = 25 

SCREEN_WIDTH = COOR_WIDTH * TILE_WIDTH
SCREEN_HEIGHT = COOR_HEIGHT * TILE_HEIGHT

WINDOWS_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

#just a character code for objects to know which is which
FIRE = 1
WATER = 2

WHITE = (255, 255, 255)


GRAVITY = 0.8

PLAYER_SIZE = (14, 20)
PLAYER_WIDTH = 28
PLAYER_HEIGHT = 40
PLAYER_MOVING_SPEED = 5
PLAYER_JUMP_SPEED = 14
PLAYER_DIE_SPEED = 6

#
DIAMOND_WIDTH = 20
DIAMOND_HEIGHT = 20

#switch
SWITCH_WIDTH = 40
SWITCH_HEIGHT = 40

#button
GATE_BUTTON_WIDTH = 30
GATE_BUTTON_HEIGHT = 30


#gate
GATE_SPEED = 0.1
ACTIVATE = 1
INACTIVATE = 0

#liquid
LIQUID_ANIMATION_FREQUENCY = 10

#doors
DOOR_WIDTH = 40
DOOR_HEIGHT = 60

#level
LOSE_COUNTER = 15