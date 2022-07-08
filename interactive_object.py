import pygame
from config import *
from game_function import *

class InteractiveObject(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()

		pass
	def update(self, players):
		pass
	def check_collide(self, player):
		if self.rect.colliderect(player.rect) and player.character != self.immune_player:
			return True
		else:
			return False

class Diamond(InteractiveObject):
	def __init__(self, coor_x = 15, coor_y = 22, type_diamond = WATER):
		super().__init__()

		self.rect = pygame.Rect(0, 0, DIAMOND_WIDTH, DIAMOND_HEIGHT)
		self.rect.center = (coor_x * TILE_WIDTH + TILE_WIDTH / 2, coor_y * TILE_HEIGHT + TILE_HEIGHT / 2)

		if type_diamond == FIRE:
			self.immune_player = WATER
			self.image = pygame.image.load('./data/environment/gemRed.png')
		else:
			self.immune_player = FIRE
			self.image = pygame.image.load('./data/environment/gemBlue.png')
		self.image = pygame.transform.scale(self.image, (DIAMOND_WIDTH, DIAMOND_HEIGHT))
	def update(self, players):
		for player in players:
			if self.check_collide(player):
				GameFunctions.function['play_sound_effect']('./data/sound/diamond.mp3')
				self.kill()

class Switch(InteractiveObject):
	def __init__(self, coor_x = 10, coor_y = 22):
		super().__init__()
		self.immune_player = None
		self.state = INACTIVATE
		self.player_holding = False
		self.left_image = pygame.image.load('./data/environment/switchLeft.png')
		self.left_image = pygame.transform.scale(self.left_image, (SWITCH_WIDTH, SWITCH_HEIGHT))
		self.image = self.left_image
		self.rect = pygame.Rect(0, 0, SWITCH_WIDTH, SWITCH_HEIGHT)
		self.rect.bottom = (coor_y + 1) * (TILE_HEIGHT)
		self.rect.centerx = coor_x * TILE_WIDTH + TILE_WIDTH / 2

	def update(self, players):
		for player in players:
			if self.check_collide(player) and not self.player_holding:
				if self.rect.centerx < player.rect.centerx:
					self.state = ACTIVATE
				else:
					self.state = INACTIVATE
			else:
				self.player_holding = False
			#update image
			if self.state == INACTIVATE:
				self.image = self.left_image
			else:
				self.image = pygame.transform.flip(self.left_image, True, False)

class GateButton(InteractiveObject):
	def __init__(self, coor_x = 10, coor_y = 22):
		super().__init__()
		self.immune_player = None
		self.state = INACTIVATE

		self.rect = pygame.Rect(0, 0, GATE_BUTTON_WIDTH, GATE_BUTTON_HEIGHT)
		self.rect.bottom = (coor_y + 1) * (TILE_HEIGHT)
		self.rect.centerx = coor_x * TILE_WIDTH + TILE_WIDTH / 2

		self.inactivate_image = pygame.image.load('./data/environment/buttonYellow.png')
		self.inactivate_image = pygame.transform.scale(self.inactivate_image, (self.rect.width, self.rect.height))

		self.activate_image = pygame.image.load('./data/environment/buttonYellow_pressed.png')
		self.activate_image = pygame.transform.scale(self.activate_image, (self.rect.width, self.rect.height))
		self.image = self.inactivate_image

	def update(self, players):
		self.state = INACTIVATE
		for player in players:
		
			if self.check_collide(player):
				self.state = ACTIVATE
				self.image = self.activate_image
		
		if self.state == INACTIVATE:
			self.image = self.inactivate_image

class Liquid(InteractiveObject):
	def __init__(self, coor_x = 10, coor_y = 22):
		super().__init__()
		self.state_counter = 0
		self.killed_character = None
		self.rect = pygame.Rect(coor_x * TILE_WIDTH, coor_y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT / 2)
	def update(self, players):
		for player in players:
			self.state_counter = self.state_counter + 1
			if self.state_counter > LIQUID_ANIMATION_FREQUENCY:
				self.state_counter = 0
				self.image = pygame.transform.flip(self.image, True, False)
			if self.check_collide(player):
				self.killed_character = player.character

class Acid(Liquid):
	def __init__(self, *args, **kargs):
		super().__init__(*args, **kargs)
		self.image = pygame.image.load('./data/environment/acid.png')
		self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
		self.immune_player = None

class Water(Liquid):
	def __init__(self, *args, **kargs):
		super().__init__(*args, **kargs)
		self.image = pygame.image.load('./data/environment/water.png')
		self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
		self.immune_player = WATER

class Lava(Liquid):
	def __init__(self, *args, **kargs):
		super().__init__(*args, **kargs)
		self.image = pygame.image.load('./data/environment/fire.png')
		self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
		self.immune_player = FIRE