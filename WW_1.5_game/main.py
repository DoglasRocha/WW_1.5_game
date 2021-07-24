import pygame
from cenario import Cenario
from cores import PRETO

pygame.init()

def main():
    
    screen = pygame.display.set_mode((1500, 1000))
    environment = Cenario(screen)
    
    while True:
        
        pygame.display.update()
        
        # captura eventos
        events = pygame.event.get()
        keyboard = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed(), pygame.mouse.get_pos()
            
        # calcula as regras
        environment.calculate_rules(mouse)
            
        # pinta
        screen.fill(PRETO)
        environment.paint()
            
        # processa eventos
        environment.process_events(events, keyboard, mouse)

if __name__ == '__main__': main()