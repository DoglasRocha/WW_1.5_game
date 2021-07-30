from abc import ABCMeta
from character import Character
from movivel import Movivel
from abc import ABCMeta, abstractmethod
from random import choice
from time import time
from guns import Pistol, SMG, AK47, Shotgun
from pygame import Surface
import cores
import pygame

directions = ['NORTH', 'SOUTH', 'EAST', 'WEST', 'NORTH EAST', 'NORTH WEST', 'SOUTH EAST', 'SOUTH WEST']

class Enemy(Movivel, metaclass=ABCMeta):
    
    
    @abstractmethod
    def paint(self) -> None:
        pass
    
    def process_events(self) -> None:
        if self.has_the_time_to_walk_passed():
            direction = choice(directions) if len(self.directions) <= 0 \
            else choice(self.directions)
                
            self.walk(direction)
            self.time_passed_since_walk = time()
            
        if self.has_the_time_to_shoot_passed():
            will_it_shoot = choice(self.probability_to_shoot)
            if will_it_shoot:
                self.shoot()
                self.time_passed_shot = time()
        
    def walk(self, direction: str) -> None:
        directions_and_speeds = {'NORTH': (-self.SPEED, 0),
                                 'SOUTH': (self.SPEED, 0),
                                 'EAST': (0, self.SPEED),
                                 'WEST': (0, -self.SPEED),
                                 'NORTH EAST': (-self.SPEED, self.SPEED),
                                 'NORTH WEST': (-self.SPEED, -self.SPEED),
                                 'SOUTH EAST': (self.SPEED, self.SPEED),
                                 'SOUTH WEST': (self.SPEED, -self.SPEED)}
        
        speeds = directions_and_speeds[direction]
        self.y_speed, self.x_speed = speeds
            
    def has_the_time_to_walk_passed(self) -> bool:
        return time() - self.time_passed_since_walk >= self.time_to_walk
    
    def has_the_time_to_shoot_passed(self) -> bool:
        return time() - self.time_passed_shot >= self.tempo_shoot
    
    def shoot(self) -> None:
        self.weapon.shoot(self.character.x, self.character.y, self.x, self.y)
        
    def refuse_movement(self, directions: str) -> None:
        self.directions = directions
        
class Recruit(Enemy, Movivel):
    
    def __init__(self, screen: Surface, character: Character):
        self.SPEED = 1
        self.x_speed = 0
        self.y_speed = 0
        self.screen = screen
        self.max_hp = 100
        self.hp = 100
        self.weapon = Pistol(screen)
        self.direction = 'NORTH'
        self.state = 'ALIVE'
        self.character = character
        self.time_to_walk = 6
        self.time_passed_since_walk = self.time_to_walk
        self.tempo_shoot = 7.5
        self.time_passed_shot = self.tempo_shoot
        self.probability_to_shoot = [False for i in range(4)]
        self.probability_to_shoot.append(True)
        self.reward = 10
        self.time_passed = 0
        self.directions = []
    
    def paint(self) -> None:
        if self.state == 'ALIVE':
            self.alive_painting()
        
    def alive_painting(self) -> None:
        pygame.draw.rect(self.screen, cores.AMARELO_ESVERDEADO, (self.x, self.y, self.size, self.size))
        self.weapon.paint(self.size)


class Soldier(Enemy, Movivel):
    
    def __init__(self, screen: Surface, character: Character):
        self.SPEED = 2
        self.x_speed = 0
        self.y_speed = 0
        self.screen = screen
        self.max_hp = 150
        self.hp = 150
        self.weapon = SMG(screen)
        self.direction = 'NORTH'
        self.state = 'ALIVE'
        self.character = character
        self.time_to_walk = 4
        self.time_passed_since_walk = self.time_to_walk
        self.tempo_shoot = 4
        self.time_passed_shot = self.tempo_shoot
        self.probability_to_shoot = [False for i in range(3)]
        self.probability_to_shoot.append(True)
        self.reward = 25
        self.time_passed = 0
        self.directions = []
    
    def paint(self) -> None:
        if self.state == 'ALIVE':
            self.alive_painting()
        
    def alive_painting(self) -> None:
        pygame.draw.rect(self.screen, cores.VERDE_LIMAO, (self.x, self.y, self.size, self.size))
        self.weapon.paint(self.size)
        
        
class Capitain(Enemy, Movivel):
    
    def __init__(self, screen: Surface, character: Character):
        self.SPEED = 1
        self.x_speed = 0
        self.y_speed = 0
        self.screen = screen
        self.max_hp = 125
        self.hp = 125
        self.weapon = AK47(screen)
        self.direction = 'NORTH'
        self.state = 'ALIVE'
        self.character = character
        self.time_to_walk = 3
        self.time_passed_since_walk = self.time_to_walk
        self.tempo_shoot = 3
        self.time_passed_shot = self.tempo_shoot
        self.probability_to_shoot = [False for i in range(3)]
        self.probability_to_shoot.append(True)
        self.reward = 50
        self.time_passed = 0
        self.directions = []
    
    def paint(self) -> None:
        if self.state == 'ALIVE':
            self.alive_painting()
        
    def alive_painting(self) -> None:
        pygame.draw.rect(self.screen, cores.VERDE_ESCURO, (self.x, self.y, self.size, self.size))
        self.weapon.paint(self.size)
        
        
class General(Enemy, Movivel):
    
    def __init__(self, screen: Surface, character: Character):
        self.SPEED = 2
        self.x_speed = 0
        self.y_speed = 0
        self.screen = screen
        self.max_hp = 300
        self.hp = 300
        self.weapon = Shotgun(screen)
        self.direction = 'NORTH'
        self.state = 'ALIVE'
        self.character = character
        self.time_to_walk = 6
        self.time_passed_since_walk = self.time_to_walk
        self.tempo_shoot = 5
        self.time_passed_shot = self.tempo_shoot
        self.probability_to_shoot = [False for i in range(2)]
        self.probability_to_shoot.append(True)
        self.reward = 200
        self.time_passed = 0
        self.directions = []
    
    def paint(self) -> None:
        if self.state == 'ALIVE':
            self.alive_painting()
        
    def alive_painting(self) -> None:
        pygame.draw.rect(self.screen, cores.DOURADO, (self.x, self.y, self.size, self.size))
        self.weapon.paint(self.size)