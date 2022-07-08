import pygame
from controller import Controller
from config import *
from game_function import *


class Player(pygame.sprite.Sprite):
    def __init__(self, character, coor_x, coor_y):
        super().__init__()
        self.character = character
        if character == WATER:
            folder = './data/character/Water/'
            self.up = 'up'
            self.left = 'left'
            self.right = 'right'
        else:
            folder = './data/character/Fire/'
            self.up = 'w'
            self.right = 'd'
            self.left = 'a'


        self.rect = pygame.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.rect.bottom = (coor_y + 1) * (TILE_HEIGHT)
        self.rect.centerx = coor_x * TILE_WIDTH + TILE_WIDTH / 2
        print('bottom: ', self.rect.bottom)
        self.previous_rect = self.rect.copy()
        # moving left or right
        self.moving = False

        # jumping or not
        self.jumping = False

        # facing left or right
        self.facing_left = False

        # this is for walking animation
        self.state_counter = 0

        self.is_dead = False

        self.y_velocity = 0

        self.walk_images = []
        for i in range(1, 12):
            self.walk_images.append(
                pygame.transform.scale(
                    pygame.image.load(folder + 'Walk/walk' + str(i) + '.png'),
                    (self.rect.width, self.rect. height)
                )
            )

        self.jump_image = pygame.image.load(folder + 'jump.png')
        self.jump_image = pygame.transform.scale(
            self.jump_image, (self.rect.width, self.rect. height))

        self.die_image = pygame.image.load(folder + 'hurt.png')
        self.die_image = pygame.transform.scale(
            self.die_image, (self.rect.width, self.rect. height))

        self.stand_image = pygame.image.load(folder + 'stand.png')
        self.stand_image = pygame.transform.scale(
            self.stand_image, (self.rect.width, self.rect. height))

        self.image = self.stand_image

    def update(self, obstacles):
        # check input
        if not self.is_dead:
            # jump
            if not self.jumping:
                if Controller.pressed[self.up]:
                    self.jumping = True
                    self.y_velocity -= PLAYER_JUMP_SPEED
                    if self.character == WATER:
                        GameFunctions.function['play_sound_effect']('./data/sound/jump_girl.mp3')
                    else:
                        GameFunctions.function['play_sound_effect']('./data/sound/jump_boy.mp3')
            if Controller.pressed[self.right]:
                self.facing_left = False
                self.rect.x += PLAYER_MOVING_SPEED
                self.moving = True
            elif Controller.pressed[self.left]:
                self.facing_left = True
                self.rect.x -= PLAYER_MOVING_SPEED
                self.moving = True
            else:
                self.moving = False

        self.y_velocity += GRAVITY
        self.rect.y += self.y_velocity

        # check collide and adjust the position
        for ob in obstacles:
            if self.rect.colliderect(ob.rect):
                # collide bottom
                if self.rect.bottom > ob.rect.top and self.previous_rect.bottom <= ob.rect.top:
                    self.rect.bottom = ob.rect.top
                    self.jumping = False
                    self.y_velocity = 0
                # collide top
                elif self.rect.top < ob.rect.bottom and self.previous_rect.top >= ob.rect.bottom:
                    self.rect.top = ob.rect.bottom
                    self.y_velocity = 0
                # collide right
                elif self.rect.right > ob.rect.left and self.rect.centerx <= ob.rect.centerx:
                    self.rect.right = ob.rect.left
                # collide left
                elif self.rect.left < ob.rect.right and self.rect.centerx >= ob.rect.centerx:
                    self.rect.left = ob.rect.right

        self.previous_rect = self.rect.copy()

        # choose image
        if self.is_dead:
            self.image = self.die_image
        else:
            if self.jumping:
                self.image = self.jump_image
                self.state_counter = 0
            elif self.moving:
                self.image = self.walk_images[self.state_counter]

                self.state_counter += 1
                if self.state_counter > 10:
                    self.state_counter = 0
            else:
                self.state_counter = 0
                self.image = self.stand_image

        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

    def die(self):
        if not self.is_dead:
            GameFunctions.function['play_sound_effect']('./data/sound/die.mp3')
            self.is_dead = True
            self.image = self.die_image
            self.y_velocity = - PLAYER_DIE_SPEED
