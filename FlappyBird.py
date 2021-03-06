import pygame
import random
import math
import os
import time
pygame.font.init()

longeur = 500
largeur= 800

BACKGROUND = pygame.transform.scale2x(pygame.image.load("bg.png"))

BIRDS = [pygame.transform.scale2x(pygame.image.load("bird1.png")),pygame.transform.scale2x(pygame.image.load("bird2.png")),pygame.transform.scale2x(pygame.image.load("bird3.png"))]

BASE = pygame.transform.scale2x(pygame.image.load("base.png"))

PIPE = pygame.transform.scale2x(pygame.image.load("pipe.png"))

class Base:
	VEL = 5
	WIDTH = BASE.get_width()
	IMG = BASE

	def __init__(self,y):
		self.y = y
		self.x1 = 0
		self.x2 = self.WIDTH


	def move(self):
		self.x1 = self.x1 - self.VEL
		self.x2 = self.x2 - self.VEL

		if ((self.x1 + self.WIDTH)<0):
			self.x1 = self.x2 + self.WIDTH

		if ((self.x2 + self.WIDTH)):
			self.x2 = self.x1 + self.WIDTH

	def draw(self,screen):
		screen.blit(self.IMG, (self.x1, self.y))
		screen.blit(self.IMG, (self.x2, self.y))


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
		self.velocity = -8.5
		self.tick_count = 0
		self.height = self.y


	def move(self):
		self.tick_count = self.tick_count + 1
		d = self.velocity * self.tick_count + 0.5*3*self.tick_count**2

		if (d >= 16):
			d = ((d / abs(d))*16)

		if (d<= 0):
			d = d - 2
		#self.tilt = self.tilt+d

		self.y = self.y + d
		if (d < 0 or self.y < self.height + 50):
			if (self.tilt < self.MAX_ROTATION):
				self.tilt = self.MAX_ROTATION
		else:
			if (self.tilt >= 0):
				self.tilt = self.tilt - self.ROT_VEL


	def draw(self,screen):
		self.img_count += 1

		if (self.img_count < self.ANIMATION_TIME):
			self.img = self.IMGS[0]
		elif (self.img_count < self.ANIMATION_TIME*2):
			self.img = self.IMGS[1]
		elif (self.img_count < self.ANIMATION_TIME*3):
			self.img = self.IMGS[2]
		elif (self.img_count < self.ANIMATION_TIME*4):
			self.img = self.IMGS[1]
		elif (self.img_count == self.ANIMATION_TIME*4 + 1):
			self.img = self.IMGS[0]
			self.img_count = 0

		if (self.tilt <= -80):
			self.img = self.IMGS[1]
			self.img_count = self.ANIMATION_TIME * 2

		rotated_image = pygame.transform.rotate(self.img,self.tilt)

		new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
		screen.blit(rotated_image, new_rect.topleft)

	def get_mask(self):
		return pygame.mask.from_surface(self.img)





class Pipe:
	GAP = 200
	VEL = 5


	def __init__(self, x):
		self.x = x
		self.height = 0
		self.bottom = 0
		self.top = 0
		self.PIPE_TOP = pygame.transform.flip(PIPE,False,True)
		self.PIPE_BOTTOM = PIPE
		self.passed = False
		self.set_height()


	def set_height(self):
		self.largeur = random.randrange(50,450)
		self.top = self.largeur - self.PIPE_TOP.get_height()
		self.bottom = self.largeur + self.GAP


	def move(self):
		self.x = self.x - self.VEL


	def draw(self, screen):
		screen.blit(self.PIPE_TOP, (self.x, self.top))
		screen.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

	def collide(self,bird):
		bird_mask = bird.get_mask()
		top_mask = pygame.mask.from_surface(self.PIPE_TOP)
		bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

		top_offset = (self.x - bird.x, self.top - round(bird.y))
		bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

		b_point = bird_mask.overlap(bottom_mask, bottom_offset)
		t_point = bird_mask.overlap(top_mask, top_offset)

		if (t_point or b_point):
			return True

			return False
							
def draw_window(screen, bird,pipes,base):
	screen.blit(BACKGROUND, (0,0))
	bird.draw(screen)
	for pipe in pipes:
		pipe.draw(screen)
	base.draw(screen)

	pygame.display.update()

def main():
	run = True
	screen = pygame.display.set_mode((longeur,largeur))
	clock = pygame.time.Clock()
	bird = Bird(230, 350)
	base = Base(730)
	pipes = [Pipe(600)]
	score = 0

	while (run):
		clock.tick(30)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					bird.jump()






		pipe_ind = 0
		bird.move()
		add_pipe = False
		rem = []


		for pipe in pipes:
			if (pipe.collide(bird)):
				main()
			if (not (pipe.passed) and (pipe.x < bird.x)):
				pipe.passed = True
				add_pipe = True


			if (pipe.x + pipe.PIPE_TOP.get_width() < 0):
				rem.append(pipe)
			pipe.move()

		if (add_pipe):
			pipes.append(Pipe(600))
			score = score + 1

		for r in rem:
			pipes.remove(r)

		base.move()
		draw_window(screen,bird,pipes,base)


if __name__ == "__main__":
	main()




