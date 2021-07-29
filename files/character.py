from guns import Weapon
from pygame import Surface
import cores
from movivel import Movivel
from pygame.event import Event
import pygame

fonte_30 = pygame.font.SysFont('arial', 30, True)

class Character(Movivel):
    
    
    def __init__(self, screen: Surface) -> None:
        self.SPEED = 1
        self.x_speed = 0
        self.y_speed = 0
        self.screen = screen
        self.max_hp = 100
        self.hp = 100
        self.weapon = None
        self.direction = 'NORTH'
        self.state = 'ALIVE'
        self.time_passed_since_death = None
        self.time_passed = 0
        self.size = None

    def paint(self) -> None:
        pygame.draw.rect(self.screen, cores.CIANO, (self.x, self.y, self.size, self.size))
        self.paint_hp()
        self.weapon.paint(self.size, True)
        
    def paint_hp(self) -> None:
        hp = f'HP: {self.hp}'
        hp_render = fonte_30.render(hp, True, cores.BRANCO)
        width_to_center = hp_render.get_width() / 2
        self.screen.blit(hp_render, (1350 - width_to_center, 750))
        
    def reinit_stats(self) -> None:
        self.hp = 100
        self.weapon.reinit_stats()
        self.state = 'ALIVE'
        self.direction = 'NORTH'
    
    def processar_eventos(self, event: Event, keyboard: tuple, mouse: tuple) -> None:
        key_up = event.type == pygame.KEYUP
        
        w = pygame.K_w
        a = pygame.K_a
        s = pygame.K_s
        d = pygame.K_d
        
        w_pressed = bool(keyboard[w])
        a_pressed = bool(keyboard[a])
        s_pressed = bool(keyboard[s])
        d_pressed = bool(keyboard[d])
            
        if w_pressed and a_pressed:
            self.y_speed = -self.SPEED
            self.x_speed = -self.SPEED
            self.direction = 'NORTH WEST'
            
        elif w_pressed and d_pressed:
            self.y_speed = -self.SPEED
            self.x_speed = self.SPEED
            self.direction = 'NORTH EAST'
            
        elif s_pressed and a_pressed:
            self.y_speed = self.SPEED
            self.x_speed = -self.SPEED
            self.direction = 'SOUTH WEST'
            
        elif s_pressed and d_pressed:
            self.y_speed = self.SPEED
            self.x_speed = self.SPEED
            self.direction = 'SOUTH EAST'
            
        elif s_pressed and w_pressed:
            self.y_speed = 0
            
        elif a_pressed and d_pressed:
            self.x_speed = 0
            
        elif w_pressed:
            self.y_speed = -self.SPEED
            self.direction = 'NORTH'
            
        elif a_pressed:
            self.x_speed = -self.SPEED
            self.direction = 'WEST'
            
        elif s_pressed:
            self.y_speed = self.SPEED
            self.direction = 'SOUTH'
            
        elif d_pressed:
            self.x_speed = self.SPEED
            self.direction = 'EAST'
               
        if key_up:
            key = event.key            
            if key == w:
                self.y_speed = 0
                
            if key == a:
                self.x_speed = 0
                
            if key == s:
                self.y_speed = 0
                
            if key == d:
                self.x_speed = 0
        
        if any(mouse[0]):
            self.weapon.shoot(mouse[1][0], mouse[1][1], self.x, self.y)
    
    def receive_weapon(self, weapon: Weapon):
        self.weapon = weapon
        