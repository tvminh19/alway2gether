from interactive_object import InteractiveObject
import pygame
from config import *

class Door(InteractiveObject):
	def __init__(self, coor_x, coor_y):
		super().__init__()

		self.rect = pygame.Rect(0, 0, DOOR_WIDTH, DOOR_HEIGHT)
		self.rect.bottom = (coor_y + 1) * (TILE_HEIGHT)
		self.rect.centerx = coor_x * TILE_WIDTH + TILE_WIDTH / 2

		
		self.open_image = pygame.image.load('./data/environment/door_open.png')
		self.open_image = pygame.transform.scale(self.open_image, (self.rect.width, self.rect.height))
		self.close_image = self.open_image
		self.is_opened = False
		

	def update(self, players, all_diamond_collected):
		for player in players:
			if player.character != self.immune_player:
				if self.check_collide(player) and all_diamond_collected:
					self.is_opened = True
					self.image = self.open_image
				else:
					self.is_opened = False
					self.image = self.close_image

class FireDoor(Door):
	def __init__(self, *args, **kargs):
		super().__init__(*args, **kargs)
		self.close_image = pygame.image.load('./data/environment/door_fire_close.png')
		self.close_image = pygame.transform.scale(self.close_image, (self.rect.width, self.rect.height))
		self.immune_player = WATER
		self.image = self.close_image

class WaterDoor(Door):
	def __init__(self, *args, **kargs):
		super().__init__(*args, **kargs)
		self.close_image = pygame.image.load('./data/environment/door_water_close.png')
		self.close_image = pygame.transform.scale(self.close_image, (self.rect.width, self.rect.height))
		self.immune_player = FIRE
		self.image = self.close_image
