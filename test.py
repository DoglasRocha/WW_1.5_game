from gun_button import GunButton
import pygame
from guns import Shotgun

def foo(aaa):
    print('deu boa')

pygame.init()

screen = pygame.display.set_mode((800,600))

button = GunButton(400, 300, foo, foo, screen, (255,255,255),
                   (255,255,255), (255,255,255), (0,0,0), Shotgun)

while True:
    
	pygame.display.update()
	screen.fill((0,0,0))
	
	mouse = pygame.mouse.get_pressed(), pygame.mouse.get_pos()
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			exit()
   
	button.calculate_rules(mouse[1])
	button.paint()
	button.process_events(None, mouse)
