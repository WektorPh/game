#
import pygame
import os
from time import sleep
import random

pygame.init()

FPS = 90


width = 1280
height = 720
colour = (0, 255, 255) 
grey = (180, 180, 180)
black = (0, 0, 0)
bg_sp = -5
ene_sp = -5
vel = 3

text = pygame.font.Font('Piedra-Regular.ttf', 24)

max_score = score = 0

window = pygame.display.set_mode((width, height ))

clock = pygame.time.Clock()

car_images = [pygame.image.load(os.path.join('Car/car0' + str(x) + '.png')) for x in range (1, 5)]

menu_image = pygame.image.load(os.path.join('menu.jpg'))

enemy_images = [ pygame.image.load(os.path.join( 'bluebat','skeleton-fly_' + str(x) + '.png')) for x in range(10)]

def display_score():
	score_text_surface = text.render("Score: " + str(score), True, black)
	score_text_rect    = score_text_surface.get_rect()
	score_text_rect.right = width - 10
	score_text_rect.top   = 10
	window.blit(score_text_surface, score_text_rect)

def display_max_score():
	score_text_surface = text.render("Max Score: " + str(max_score), True, black)
	score_text_rect    = score_text_surface.get_rect()
	score_text_rect.right = width - 10
	score_text_rect.top   = 30
	window.blit(score_text_surface, score_text_rect)

def get_size(image, width):
	image_size = image.get_rect().size 
	return (width, int(image_size[1] * width / image_size[0]))
	
def is_out_of_screen(car):
	
	if car.x < 0:
		return True
	if car.y < 0:
		return True
	if car.x + 50 > width:
		return True
	if car.y + 50 > height:
		return True

	return False


def resize_image(image, width):
	image_size = get_size(image, width)
	return pygame.transform.scale(image, image_size)


image_width = 200 
car_images = list(map(resize_image, 
					  car_images,   
					  [ image_width for i in range(len(car_images)) ] ))	 
				 
enemy_images = list(map(resize_image, enemy_images, [ 200 for x in range(len(enemy_images)) ]))

menu_image = resize_image(menu_image, width)

def check_collision(hero, enemy):
	enemy_rect = enemy.rect
	hero_rect = hero.rect
	print(enemy_rect, hero_rect)
	if hero_rect.colliderect(enemy_rect) == 1:
		print('collision')
		return True

	return False

def game_reset(hero, enemy):
	global score, max_score
	global vel
	global bg_sp
	global ene_sp
	global next_score
	if score > max_score:
		max_score = score
	score = 0
	vel = 3
	bg_sp = -5
	ene_sp = -5
	next_score = 100
	hero.crash()
	enemy.restore_position()







class Base():
	def __init__(self, x, y, images):
		self.x = x
		self.y = y
		self.images = images
		self.rect = images[0].get_rect()
		
		

	def draw(self, frame):
		window.blit(self.images[frame], (self.x, self.y))
		# pygame.draw.rect(window, (0, 255, 255), self.rect)

class Hero(Base):
	def __init__(self):
		super().__init__(int(width/4), int(height / 2), car_images) # x, y, hero_images
		self.rect.size = (self.rect.size[0] - 40, self.rect.size[1] - 20) 
		s = self.images[0].get_rect().size
		self.rect.center = (self.x + int(s[0]/2), self.y + int(s[1]/2))


	
	def move(self, x, y):
		self.x += x
		self.y += y
		s = self.images[0].get_rect().size
		self.rect.center = (self.x + int(s[0]/2), self.y + int(s[1]/2))

	def restore_pisition(self):
		self.x = 50
		self.y = int(height / 2)

	def crash(self):
		sleep(1)
		self.restore_pisition()


class Enemy(Base):
	def __init__(self):
		super().__init__(
			int(width * 0.8),    
			int(height / 2),     
			enemy_images) 
		self.rect.size = (self.rect.size[0] - 80, self.rect.size[1] - 70)
		s = self.images[0].get_rect().size 
		self.rect.center = (self.x + int(s[0]/2) - 60, self.y + int(s[1]/2) - 50)


	def move(self, x=ene_sp, y=0):
		self.x += ene_sp
		self.y += y
		s = self.images[0].get_rect().size
		self.rect.center = (self.x + int(s[0]/2) - 10 , self.y + int(s[1]/2) + 10)

	def restore_position(self):
		self.x = width
		self.y = int(height / 2) 


	def draw(self, frame):
		if self.x + image_width < 0:
			self.x = width + 150
			self.y = random.randint(0, height - self.rect.size[1])
		super().draw(frame)
	

class Background():
	def __init__(self):
		self.line_interval = 150
		self.line_width = 300
		self.line_height = 50
		self.lines =[ pygame.Rect(x, int(height/2 - self.line_height/2), self.line_width, self.line_height) for x in [0, 400, 800]] 
	
	def draw_back(self):
		window.fill(grey)

	def draw_lines(self):
		for rectangle in self.lines:
			pygame.draw.rect(window, (255, 255, 255) , rectangle)

	def draw(self):
		self.move_lines()
		self.draw_back()
		self.draw_lines()

	def append_line(self):
		if self.lines[-1].x < width:
			self.lines.append(
				pygame.Rect(self.lines[-1].x + self.line_width + self.line_interval,
				int(height / 2) - int(self.line_height / 2),
				self.line_width, self.line_height))
	def pop_lines(self):
		if self.lines[0].x + self.line_width < 0:
			self.lines.pop(0)



	def move_lines(self):
		self.append_line()
		self.pop_lines()

		for i in range(len(self.lines)):
			self.lines[i] = self.lines[i].move(bg_sp, 0)


def game_menu():

	text_size = 100
	text_resize_speed = 1

	intro = True
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				intro = False


		textMenu        = pygame.font.Font('Piedra-Regular.ttf', 140)
		textMenuSurface = textMenu.render("Main Menu", True, black)
		textMenuRect    = textMenuSurface.get_rect()
		textMenuRect.center = (int(width/2), int(height/6))



		textEnter        = pygame.font.Font('Piedra-Regular.ttf', text_size) 
		textEnterSurface = textEnter.render("Press Enter", True, black)
		textEnterRect    = textEnterSurface.get_rect()
		textEnterRect.center = (int(width/2), int(height/1.5)) 


		window.blit(menu_image, (0,0))
		window.blit(textMenuSurface, textMenuRect)
		window.blit(textEnterSurface, textEnterRect)

		text_size += text_resize_speed

		if text_size > 110:
			text_resize_speed *= -1
		elif text_size < 100:
			text_resize_speed *= -1

		pygame.display.update()

		clock.tick(60)

def game_pause():
	pause = True
	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pause = False

		textMenu        = pygame.font.Font('Piedra-Regular.ttf', 140)
		textMenuSurface = textMenu.render("Pause", True, black)
		textMenuRect    = textMenuSurface.get_rect()
		textMenuRect.center = (int(width/2), int(height/4))

		window.blit(textMenuSurface, textMenuRect)
		pygame.display.update()

next_score = 100
	
def game_loop():	

	car = Hero()
	enemy = Enemy()
	bg = Background()

	x = width / 2
	y = height / 2

	
	car_x = 0
	car_y = 0
	car_next_tick = 100
	enemy_next_tick = 50
	car_frame = 0
	enemy_frame = 0
	ene_x = 0
	ene_y = 0
	next_enemy_addition_score = 0
	

	global score, max_score
	global FPS

	game_menu()

	global vel

	while True:

		clock.tick(FPS)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()



			elif event.type == pygame.KEYDOWN:
				# if event.key == pygame.K_d:
				# 	ene_x += vel
				# elif event.key == pygame.K_a:
				# 	ene_x -= vel
				# elif event.key == pygame.K_w:
				# 	ene_y -= vel
				# elif event.key == pygame.K_s:
				# 	ene_y += vel
				if event.key == pygame.K_RIGHT:
					car_x += vel
				elif event.key == pygame.K_LEFT:
					car_x -= vel
				elif event.key == pygame.K_UP:
					car_y -= vel
				elif event.key == pygame.K_DOWN:
					car_y += vel


				print(event)
				if event.key == pygame.K_ESCAPE:
					game_pause()
					vel_y = vel_x = 0
					enemy_next_tick = car_next_tick = pygame.time.get_ticks()	

			elif event.type == pygame.KEYUP:
				# if event.key == pygame.K_d:
				# 	ene_x += -vel
				# elif event.key == pygame.K_a:
				# 	ene_x -= -vel
				# elif event.key == pygame.K_w:
				# 	ene_y -= -vel
				# elif event.key == pygame.K_s:
				# 	ene_y += -vel
				if event.key == pygame.K_RIGHT:
					car_x += -vel
				elif event.key == pygame.K_LEFT:
					car_x -= -vel
				elif event.key == pygame.K_UP:
					car_y -= -vel
				elif event.key == pygame.K_DOWN:
					car_y += -vel



			


		if is_out_of_screen(car):
			print('out of screen')
			car.crash()

		
		if pygame.time.get_ticks() > car_next_tick:
			if car_x > 0:
				car_next_tick += 80
			elif car_x < 0:
				car_next_tick += 120
			else:
				car_next_tick += 100

			car_frame = (car_frame + 1) % 4

		
		if pygame.time.get_ticks() > enemy_next_tick:
			enemy_next_tick += 25
			enemy_frame = (enemy_frame + 1) % 10

		if check_collision(car, enemy):
			game_reset(car, enemy)

		score += 1
		if score > max_score:
			max_score = score

		global next_score
		global bg_sp 
		global ene_sp
		

		if score > next_score:
			bg_sp -= 1
			ene_sp -= 1
			vel += 1
			next_score += 100


		window.fill(colour)
		bg.draw()
		display_score()
		display_max_score()
		car.move(car_x, car_y)
		enemy.move()
		car.draw(car_frame)
		enemy.draw(enemy_frame)
		pygame.display.update()

game_loop()

