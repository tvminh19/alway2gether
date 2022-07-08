import pygame
import sys
from pygame.locals import *

# act as a interface for input device


class Controller:
    pressed = {'left_mouse': False,
               'w': False,
               'a': False,
               'd': False,
               'up': False,
               'left': False,
               'right': False}

    mouse_cooling_down = False

    def update():

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        # update value for the keys
        pressed = pygame.key.get_pressed()
        Controller.pressed['up'] = pressed[pygame.K_UP]
        Controller.pressed['left'] = pressed[pygame.K_LEFT]
        Controller.pressed['right'] = pressed[pygame.K_RIGHT]

        Controller.pressed['w'] = pressed[pygame.K_w]
        Controller.pressed['a'] = pressed[pygame.K_a]
        Controller.pressed['d'] = pressed[pygame.K_d]
        # the mouse is a little bit special so we treat it differently
        Controller.mouse_position = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0]:
            if not Controller.mouse_cooling_down:
                Controller.mouse_cooling_down = True
                Controller.pressed['left_mouse'] = True
                print(Controller.mouse_position)
            else:
                Controller.pressed['left_mouse'] = False

        else:
            Controller.mouse_cooling_down = False
            Controller.pressed['left_mouse'] = False
