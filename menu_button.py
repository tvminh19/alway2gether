import pygame
import sys
from pygame.locals import *
from controller import Controller


class MenuButton(pygame.sprite.Sprite):
    def __init__(self, image_path=None, x=None, y=None, width=100, height=100, function=None):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.function = function

    def update(self):
        if Controller.pressed['left_mouse']:
            if self.rect.collidepoint(Controller.mouse_position):
                self.function()


class ToggleMenuButton(MenuButton):
    def __init__(self, off_image_path=None, check_function=None, *args, **kargs):
        super(ToggleMenuButton, self).__init__(*args, **kargs)
        off_image = pygame.image.load(off_image_path)
        self.on_image = self.image
        self.off_image = pygame.transform.scale(
            off_image, (self.rect.width, self.rect.height))
        self.check_function = check_function

    def update(self):
        super().update()

        if self.check_function():
            self.image = self.on_image
        else:
            self.image = self.off_image

# add more classes here if u like
