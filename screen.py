import pygame
import sys
from menu_button import *
from game_function import GameFunctions
from config import *
from obstacle import *
from pygame.locals import *
from player import Player
from interactive_object import *
from door import *
import numpy as np
import pandas as pd

class Screen:
    def __init__(self):
        pass

    def update(self):
        pass

    def render(self, display_surface):
        display_surface.blit(self.background, [0, 0])
        pass

################################################


class MenuScreen():
    def __init__(self):
        self.buttons = pygame.sprite.Group()

    def update(self):
        self.buttons.update()

    def render(self, display_surface):
        display_surface.blit(self.background, [0, 0])
        self.buttons.draw(display_surface)


class HomeMenu(MenuScreen):
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load(
            "./data/menu/menu_screen.png")
        self.background = pygame.transform.scale(self.background, WINDOWS_SIZE)

        self.buttons.add(
            MenuButton(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2 + 50,
                       image_path='./data/menu/Play.png', height=MENU_BUTTON_HEIGHT, width=MENU_BUTTON_WIDTH,
                       function=lambda: GameFunctions.function['go_to_screen'](
                           'choose_level')
                       ),

            ToggleMenuButton(x=SCREEN_WIDTH / 2 + 100, y=SCREEN_HEIGHT / 2 + 100,
                             image_path='./data/menu/SoundOn.png', off_image_path='./data/menu/SoundOff.png',
                             height=MENU_BUTTON_HEIGHT, width=MENU_BUTTON_WIDTH,
                             function=GameFunctions.function['toggle_sound'],
                             check_function=GameFunctions.function['check_sound_on']
                             ),

            ToggleMenuButton(x=SCREEN_WIDTH / 2 - 100, y=SCREEN_HEIGHT / 2 + 100,
                             image_path='./data/menu/MusicOn.png', off_image_path='./data/menu/MusicOff.png', 
                             height=MENU_BUTTON_HEIGHT, width=MENU_BUTTON_WIDTH,
                             function=GameFunctions.function['toggle_music'],
                             check_function=GameFunctions.function['check_music_on']
                             )
        )


class LevelSelectMenu(MenuScreen):
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load(
            "./data/menu/level_select_screen.png")
        self.background = pygame.transform.scale(self.background, WINDOWS_SIZE)

        self.buttons.add(
            MenuButton(x=100, y=100,
                       image_path='./data/menu/Back.png', height=MENU_BUTTON_HEIGHT, width=MENU_BUTTON_WIDTH,
                       function=lambda: GameFunctions.function['go_to_screen'](
                           'home')
                       ),

            MenuButton(x=SCREEN_WIDTH / 2 - 100, y=SCREEN_HEIGHT / 2,
                       image_path='./data/menu/Level1.png', height=MENU_BUTTON_HEIGHT, width=MENU_BUTTON_WIDTH,
                       function=lambda: GameFunctions.function['go_to_screen'](
                           'level1')
                       ),

            MenuButton(x=SCREEN_WIDTH / 2 + 100, y=SCREEN_HEIGHT / 2,
                       image_path='./data/menu/Level2.png', height=MENU_BUTTON_HEIGHT, width=MENU_BUTTON_WIDTH,
                       function=lambda: GameFunctions.function['go_to_screen'](
                           'level2')
                       )

        )


###############################################
class LevelScreen(Screen):
    def __init__(self, screen_name):
        self.menu_buttons = pygame.sprite.Group()
        self.background = pygame.image.load(
            "./data/environment/wall.png")
        self.background = pygame.transform.scale(self.background, WINDOWS_SIZE)

        self.menu_buttons.add(
            MenuButton(x=50, y=50,
                       image_path='./data/menu/Back.png', height=MENU_BUTTON_HEIGHT, width=MENU_BUTTON_WIDTH,
                       function=lambda: GameFunctions.function['go_to_screen'](
                           'choose_level')
                       ),

            ToggleMenuButton(x=SCREEN_WIDTH - 100, y=50,
                             image_path='./data/menu/SoundOn.png', off_image_path='./data/menu/SoundOff.png',
                             height=MENU_BUTTON_HEIGHT, width=MENU_BUTTON_WIDTH,
                             function=GameFunctions.function['toggle_sound'],
                             check_function=GameFunctions.function['check_sound_on']
                             ),

            ToggleMenuButton(x=SCREEN_WIDTH - 50, y=50,
                             image_path='./data/menu/MusicOn.png', off_image_path='./data/menu/MusicOff.png',
                              height=MENU_BUTTON_HEIGHT, width=MENU_BUTTON_WIDTH,
                             function=GameFunctions.function['toggle_music'],
                             check_function=GameFunctions.function['check_music_on']
                             )
        )
        self.lose_animation_counter = None

        #TODO: update the load file mechanic
        self.load_level(screen_name)

    def load_level(self, level):
        self.obstacles = pygame.sprite.Group()
        self.interactive_objects = pygame.sprite.Group()
        self.liquid = pygame.sprite.Group()
        self.diamonds = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        self.players = pygame.sprite.Group()

        #load gates first
        gates = []
        df = pd.read_csv('./data/level/' + level + '/gate.csv')
        for index, row in df.iterrows():
            tmp = Gate(coor_x = row['coor_x'], coor_y = row['coor_y'],
                    move_x  = row['move_x'], move_y = row['move_y'],
                    size_x = row['size_x'], size_y = row['size_y'],
                    code = row['code'])
            gates.append(tmp)
            self.obstacles.add(tmp)
        #load normal components
        # 1: wall
        # 2: water
        # 3: lava
        # 4: acid

        # 11: water player
        # 12: fire player

        # 21: water diamond
        # 22: fire diamond

        # 31: water door
        # 32: fire door

        # 1XX: button with code XX
        # 2XX: switch with code XX

        board_arr = np.genfromtxt('./data/level/' + level + '/board.txt', delimiter = ',')

        for y in range(COOR_HEIGHT):
            for x in range(COOR_WIDTH):
                if board_arr[y, x] == 1:
                    self.obstacles.add(Wall(coor_x = x, coor_y = y))
                elif board_arr[y, x] == 2:
                    self.obstacles.add(HalfWall(coor_x = x, coor_y = y))
                    tmp = Water(coor_x = x, coor_y = y)
                    self.liquid.add(tmp)
                    self.interactive_objects.add(tmp)
                elif board_arr[y, x] == 3:
                    self.obstacles.add(HalfWall(coor_x = x, coor_y = y))
                    tmp = Lava(coor_x = x, coor_y = y)
                    self.liquid.add(tmp)
                    self.interactive_objects.add(tmp)
                elif board_arr[y, x] == 4:
                    self.obstacles.add(HalfWall(coor_x = x, coor_y = y))
                    tmp = Acid(coor_x = x, coor_y = y)
                    self.liquid.add(tmp)
                    self.interactive_objects.add(tmp)
                elif board_arr[y, x] == 11:
                    self.players.add(Player(WATER, coor_x = x, coor_y = y))
                elif board_arr[y, x] == 12:
                    self.players.add(Player(FIRE, coor_x = x, coor_y = y))
                elif board_arr[y, x] == 31:
                    self.doors.add(WaterDoor(coor_x = x, coor_y = y))
                elif board_arr[y, x] == 32:
                    self.doors.add(FireDoor(coor_x = x, coor_y = y))
                elif board_arr[y, x] == 21:
                    tmp = Diamond(coor_x = x, coor_y = y, type_diamond = WATER)
                    self.diamonds.add(tmp)
                    self.interactive_objects.add(tmp)
                elif board_arr[y, x] == 22:
                    tmp = Diamond(coor_x = x, coor_y = y, type_diamond = FIRE)
                    self.diamonds.add(tmp)
                    self.interactive_objects.add(tmp)
                elif board_arr[y, x] >= 100 and board_arr[y, x] < 200:
                    tmp = GateButton(coor_x = x, coor_y = y)
                    self.interactive_objects.add(tmp)
                    code = board_arr[y, x] - 100
                    for gate in gates:
                        if gate.code == code:
                            gate.add_switch(tmp)
                elif board_arr[y, x] >= 200 and board_arr[y, x] < 300:
                    tmp = Switch(coor_x = x, coor_y = y)
                    self.interactive_objects.add(tmp)
                    code = board_arr[y, x] - 200
                    for gate in gates:
                        if gate.code == code:
                            gate.add_switch(tmp)

    def update(self):
        if self.lose_animation_counter != None:
            
            if self.lose_animation_counter == 0:
                self.menu_buttons.empty()
                GameFunctions.function['go_to_screen']('lose_screen')
            else:
                self.lose_animation_counter = self.lose_animation_counter - 1
                
         #check if all diamonds is collected
        if self.diamonds.sprites():
            all_diamond_collected = False
        else:
            all_diamond_collected = True
        #update obstacles
        self.obstacles.update()

        # update players
        self.players.update(self.obstacles.sprites())

        # update interactive objects
        players = self.players.sprites()
        self.interactive_objects.update(players)
        self.doors.update(players, all_diamond_collected)
        # update menu buttons
        self.menu_buttons.update()

        #check lose condition
        
        for i in self.liquid.sprites():
            if i.killed_character != None:
                if self.lose_animation_counter == None:
                    self.lose_animation_counter = LOSE_COUNTER

                for player in self.players.sprites():
                    if player.character == i.killed_character:
                        player.die()
        
        #check win condition
        win = True

        for door in self.doors.sprites():
            if not door.is_opened:
                win = False
        if win:
            self.menu_buttons.empty()
            GameFunctions.function['go_to_screen']('win_screen')


    def render(self, display_surface):
        # render the background first
        display_surface.blit(self.background, [0, 0])

        #render door
        self.doors.draw(display_surface)

        #render the obstacles
        self.obstacles.draw(display_surface)

        # render player
        self.players.draw(display_surface)

        # render interactive objects, danger objects
        self.interactive_objects.draw(display_surface)

        # render menu buttons
        self.menu_buttons.draw(display_surface)


class IntroSCreen(Screen):
    def __init__(self):
        self.background = pygame.image.load("./data/menu/intro_screen.png")
        self.background = pygame.transform.scale(self.background, WINDOWS_SIZE)

    def update(self):
        if Controller.pressed['left_mouse']:
            GameFunctions.function['go_to_screen']('home')


class LoseScreen(MenuScreen):
    def __init__ (self):
        super().__init__()
        self.background = pygame.image.load('./data/menu/death_screen.png')
        self.background = pygame.transform.scale(self.background, WINDOWS_SIZE)

        self.buttons.add(
            MenuButton(x=SCREEN_WIDTH / 2 - 100, y=SCREEN_HEIGHT / 2,
                       image_path='./data/menu/Back.png', height=MENU_BUTTON_HEIGHT, width=MENU_BUTTON_WIDTH,
                       function=lambda: GameFunctions.function['go_to_screen'](
                           'choose_level')
                       ),

            MenuButton(x=SCREEN_WIDTH / 2 + 100, y=SCREEN_HEIGHT / 2,
                       image_path='./data/menu/ResetLevel.png', height=MENU_BUTTON_HEIGHT, width=MENU_BUTTON_WIDTH,
                       function=lambda: GameFunctions.function['go_to_screen'](
                           'reset_level')
                       )
            )

class WinScreen(MenuScreen):
    def __init__ (self):
        super().__init__()
        self.background = pygame.image.load('./data/menu/win_screen.png')
        self.background = pygame.transform.scale(self.background, WINDOWS_SIZE)

        self.buttons.add(
            MenuButton(x=SCREEN_WIDTH / 2 - 100, y=SCREEN_HEIGHT / 2,
                       image_path='./data/menu/Back.png', height=MENU_BUTTON_HEIGHT, width=MENU_BUTTON_WIDTH,
                       function=lambda: GameFunctions.function['go_to_screen'](
                           'choose_level')
                       ),

            MenuButton(x=SCREEN_WIDTH / 2 + 100, y=SCREEN_HEIGHT / 2,
                       image_path='./data/menu/ResetLevel.png', height=MENU_BUTTON_HEIGHT, width=MENU_BUTTON_WIDTH,
                       function=lambda: GameFunctions.function['go_to_screen'](
                           'reset_level')
                       )
            )