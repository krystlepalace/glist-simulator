import pygame
from random import randrange

resolution = 800
size = 50

x, y = randrange(0, resolution, size), randrange(0, resolution, size)
apple = randrange(0, resolution, size), randrange(0, resolution, size)
length = 1
snake = [(x, y)]
dx, dy = 0, 0
fps = 5
directions = {'W': True, 'S': True, 'D': True, 'A': True}
score = 0

pygame.init()
screen = pygame.display.set_mode([resolution, resolution])
clock = pygame.time.Clock()
font = pygame.font.SysFont('Comic-Sans', 26, bold = True)
font2 = pygame.font.SysFont('Castellar', 66, bold = True)
img = pygame.image.load('data/images/background.jpg').convert()
pygame.mixer.music.load('data/music/phonk.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

while True:
	# создаем окно и заполняем его
	screen.blit(img, (0, 0))
	[pygame.draw.rect(screen, pygame.Color(76, 187, 23), 
		(i, j, size-2, size-2)) for i, j in snake]
	pygame.draw.rect(screen, pygame.Color(76, 137, 10), 
		(*snake[-1], size-2, size-2))
	pygame.draw.rect(screen, pygame.Color(199, 0, 57), (*apple, size, size))

	# счёт
	render_score = font.render(f'SCORE: {score}', 1, 
		pygame.Color(191, 64, 191))
	screen.blit(render_score, (0, 0))

	# перемещаем змейку
	x += dx*size
	y += dy*size
	snake.append((x, y))
	# срез рендера в зависимости от длины змейки
	snake = snake[-length:]

	# поедание яблока
	if snake[-1] == apple:
		apple = randrange(0, resolution, size), randrange(0, resolution, size)
		s = pygame.mixer.Sound('data/sfx/50700.ogg')
		s.play()
		length += 1
		score += 1
		fps+=1

	# game over
	x_out = x < 0 or x > resolution-size
	y_out = y < 0 or y > resolution-size
	if x_out or y_out or len(snake) != len(set(snake)):
		pygame.mixer.music.stop()
		s = pygame.mixer.Sound('data/sfx/death.ogg')
		s.play()
		while True:
			render_end = font2.render('GAME OVER', 1, 
				pygame.Color(191, 64, 191))
			screen.blit(render_end, (resolution//2 - 250, resolution//3))
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()

	# обновляем экран
	pygame.display.flip()
	clock.tick(fps)

	# обработка закрытия
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()

	# управление
	key = pygame.key.get_pressed()
	if key[pygame.K_w] and directions['W']:
		dx, dy = 0, -1
		directions = {'W': True, 'S': False, 'D': True, 'A': True}
	elif key[pygame.K_s] and directions['S']:
		dx, dy = 0, 1
		directions = {'W': False, 'S': True, 'D': True, 'A': True}
	elif key[pygame.K_a] and directions['A']:
		dx, dy = -1, 0
		directions = {'W': True, 'S': True, 'D': False, 'A': True}
	elif key[pygame.K_d] and directions['D']:
		dx, dy = 1, 0
		directions = {'W': True, 'S': True, 'D': True, 'A': False}

print('GAME OVER')
