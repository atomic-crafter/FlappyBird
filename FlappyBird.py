import pygame
import random
import math
import os
import time
pygame.font.init()

longeur = 500
largeur= 800

BACKGROUND = pygame.transform.scale2x(pygame.image.load("bg.png"))

def draw_window(screen):
	screen.blit(BACKGROUND, (0,0))
	pygame.display.update()

def principal():
	run = True
	screen = pygame.display.set_mode((longeur,largeur))
	clock = pygame.time.Clock()

	while (run):
		clock.tick(30)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit()
		draw_window(screen)


if __name__ == "__main__":
	main()


BIRDS = [pygame.transform.scale2x(pygame.image.load("bird1.png")),pygame.transform.scale2x(pygame.image.load(bird2.png)),pygame.transform.scale2x(pygame.image.load(bird3.png))]


class Bird:
	IMGS = BIRDS
	MAX_ROTATION = 25
	ROT_VEL = 20
	ANIMATION_TIME = 5

	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.tilt = 0
		self.tick_count = 0
		self.velocity = 0
		self.height = self.y
		self.img_count = 0
		self.img = self.IMGS[0]


	def jump(self):
		
