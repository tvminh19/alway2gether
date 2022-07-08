from config import *
import pygame
class Obstacle(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()

class Wall(Obstacle):
	def __init__(self, coor_x = 0, coor_y = 0, name = None):
		super().__init__()
		self.image = pygame.image.load('./data/environment/castleCenter.png')
		self.rect = pygame.Rect(coor_x * TILE_WIDTH, coor_y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
		self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_HEIGHT))

class HalfWall(Obstacle):
	def __init__(self, coor_x = 0, coor_y = 0, name = None):
		super().__init__()
		self.image = pygame.image.load('./data/environment/castleCenter.png')
		self.rect = pygame.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT / 2)
		self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_HEIGHT / 2))
		self.rect.bottom = TILE_HEIGHT * (coor_y + 1)
		self.rect.centerx = TILE_WIDTH * (coor_x + 0.5)

class Gate(Obstacle):
	def __init__(self, coor_x = 0, coor_y = 0, move_x = 0, move_y = -5, size_x = 1, size_y = 3, code = 0):
		super().__init__()
		self.code = code
		self.switches = []
		self.rect = pygame.Rect(0, 0, size_x * TILE_WIDTH, size_y * TILE_HEIGHT)
		self.image = pygame.image.load('./data/environment/boxEmpty.png')
		self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

		self.rect.bottom = TILE_HEIGHT * (coor_y + 1)
		self.rect.centerx = TILE_WIDTH * (coor_x + 0.5)

		self.x, self.y = 0, 0
		self.move_x, self.move_y = move_x * TILE_WIDTH, move_y * TILE_HEIGHT

	def add_switch(self,switch):
		self.switches.append(switch)

	def update(self):
		activate = False
		for switch in self.switches:
			if switch.state == ACTIVATE:
				activate = True
		if activate:
			if not (self.move_x == self.x and self.move_y == self.y):
				self.x = self.x + self.move_x * GATE_SPEED
				self.y = self.y + self.move_y * GATE_SPEED
				self.rect.centerx = self.rect.centerx + self.move_x * GATE_SPEED
				self.rect.centery = self.rect.centery + self.move_y * GATE_SPEED

		elif self.x != 0 or self.y != 0:
			self.x = self.x - self.move_x * GATE_SPEED
			self.y = self.y - self.move_y * GATE_SPEED
			self.rect.centerx = self.rect.centerx - self.move_x * GATE_SPEED
			self.rect.centery = self.rect.centery - self.move_y * GATE_SPEED
