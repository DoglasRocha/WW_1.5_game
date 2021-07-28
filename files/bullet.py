import pygame
import cores
from time import time
from random import choice

class Bullet:
    
    
    def __init__(self, initial_x: int, initial_y: int, 
                 x_speed: int, y_speed: int, screen: int,
                 damage: int, time_to_explode: int, imprecision: list):
        self.initial_x, self.initial_y = initial_x, initial_y
        self.x, self.y = self.initial_x, self.initial_y
        self.x_speed, self.y_speed = x_speed, y_speed
        self.screen = screen
        self.state = 'FLYING'
        self.damage = damage
        self.time_to_explode = time_to_explode
        self.creation_time = time()
        self.x_imprecision, self.y_imprecision = (choice(imprecision), 
                                                  choice(imprecision))
        
    def paint(self, size: int) -> None:
        states_and_actions = {'FLYING': self.paint_flying,
                              'STOPPED': self.paint_stopped}
        
        action = states_and_actions[self.state]
        action(size)
        
    def paint_flying(self, size: int) -> None:
        pygame.draw.circle(self.screen, cores.BRANCO, (self.x, self.y), size // 5)
        
    def paint_stopped(self, size: int) -> None:
        pass
    
    def calculate_rules(self, size: int) -> None:
        states_and_actions = {'FLYING': self.calculate_flying_rules,
                              'STOPPED': self.calculate_stopped_rules}
        
        action = states_and_actions[self.state]
        action(size)
        
    def calculate_flying_rules(self, size: int) -> None:
        self.x += self.x_speed + self.x_imprecision
        self.y += self.y_speed + self.y_imprecision
        
        line = (self.y) // size
        column = (self.x - 300) // size
        
        self.hitbox = [(line, column)]
        
        if self.time_to_explode > 0 and self.has_to_explode():
            self.exploded()
        
    def calculate_stopped_rules(self, size: int) -> None:
        pass
        
    def collided(self) -> None:
        self.state = 'STOPPED'
        
    def exploded(self) -> None:
        self.state = 'STOPPED'
        
    def has_to_explode(self) -> bool:
        return time() - self.creation_time >= self.time_to_explode
