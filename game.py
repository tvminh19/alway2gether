from config import *
from controller import Controller
from screen import *
import pygame
from game_function import GameFunctions

# control main game loop, settingg and bla bla


class Game:
    sound_dictionary = {}

    def start():
        pygame.init()

        pygame.mixer.init()
        pygame.mixer.music.load('./data/sound/background.mp3')
        pygame.mixer.music.play(loops = -1)
        Game.sound_effect = {}

        Game.music_on = True
        Game.sound_on = True
        Game.clock = pygame.time.Clock()

        # assign functions for lower classes
        GameFunctions.function['play_sound_effect'] = Game.play_sound_effect
        GameFunctions.function['toggle_sound'] = Game.toggle_sound
        GameFunctions.function['toggle_music'] = Game.toggle_music
        GameFunctions.function['go_to_screen'] = Game.go_to_screen
        GameFunctions.function['check_sound_on'] = lambda: Game.sound_on
        GameFunctions.function['check_music_on'] = lambda: Game.music_on

        Game.display_surface = pygame.display.set_mode(WINDOWS_SIZE)

        Game.current_screen = IntroSCreen()

        # game loop
        while True:
            # update controller to get input
            Controller.update()

            # update

            Game.current_screen.update()
            Game.current_screen.render(Game.display_surface)

            # render the screen
            #Game.display_surface = pygame.transform.scale(Game.display_surface, )
            pygame.display.update()

            # tick the clock
            Game.clock.tick(FPS)

    def toggle_sound():
        print('toggle_sound')
        Game.sound_on = not Game.sound_on

    def toggle_music():
        print('toggle_music')
        Game.music_on = not Game.music_on
        if Game.music_on:
            pygame.mixer.music.play(loops = -1)
        else:
            pygame.mixer.music.stop()

    def go_to_screen(screen_name):
        print('go_to_screen: ', screen_name)
        Game.current_screen.render(Game.display_surface)
        if screen_name == 'home':
            Game.current_screen = HomeMenu()
        elif screen_name == 'choose_level':
            Game.current_screen = LevelSelectMenu()
        elif screen_name == 'lose_screen':
            Game.current_screen = LoseScreen()
        elif screen_name == 'win_screen':
            Game.current_screen = WinScreen()
        elif screen_name == 'reset_level':
            Game.current_screen = LevelScreen(Game.current_level)
        else:
            Game.current_level = screen_name
            Game.current_screen = LevelScreen(screen_name)

    def play_sound_effect(sound_path):
        if Game.sound_on:
            if not sound_path in Game.sound_effect:
                Game.sound_effect[sound_path] = pygame.mixer.Sound(sound_path)

            Game.sound_effect[sound_path].play()
