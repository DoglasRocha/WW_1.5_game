from abc import ABCMeta, abstractmethod
from bullet import Bullet
from time import time
from random import choice
import cores
import pygame

pygame.font.init()

font_30 = pygame.font.SysFont('arial', 30, True)
font_20 = pygame.font.SysFont('arial', 20, True)

class Weapon(metaclass=ABCMeta):
    
    
    def shoot(self, x_position_click: int, y_position_click: int, 
            current_x: int, current_y: int) -> None:
        
        if self.can_shoot() and self.will_shoot():
            relative_x_position = x_position_click - current_x
            relative_y_position = y_position_click - current_y
                
            distance = (relative_x_position**2 + relative_y_position**2)**(1/2)
            divider = distance / self.bullet_speed
            try:
                bullet_x_speed = round(relative_x_position / divider)
                bullet_y_speed = round(relative_y_position / divider)
                
            except ZeroDivisionError:
                bullet_x_speed, bullet_y_speed = 3, 4
                
            self.fired_bullets.append(Bullet(current_x, current_y, 
                                            bullet_x_speed, bullet_y_speed, 
                                            self.screen, self.damage,
                                            self.time_since_bullet_flying,
                                            self.imprecision))
            
            self.time_passed_since_shoot = time()
            self.bullets_in_the_gun -= 1
            
        if self.bullets_in_the_gun <= 0:
            self.state = 'RELOADING'
            self.reload()
            
    def reload(self) -> None:
        amount_to_reload = self.ammo_capacity - self.bullets_in_the_gun
        
        if self.ammo_bag > amount_to_reload:
            self.ammo_bag -= amount_to_reload
            
        else: 
            amount_to_reload = self.ammo_bag * 1
            self.ammo_bag = 0
            
        self.bullets_in_the_gun += amount_to_reload
        self.time_passed_since_reload = time()
        
    def can_shoot(self) -> bool:
        return (self.has_the_cooldown_time_passed()
                    and self.has_the_reload_time_passed()
                    and self.bullets_in_the_gun > 0)
    
    def has_the_cooldown_time_passed(self) -> bool:
        return time() - self.time_passed_since_shoot >= self.shoot_time
    
    def has_the_reload_time_passed(self) -> bool:
        return time() - self.time_passed_since_reload >= self.reload_time
    
    def will_shoot(self) -> bool:
        return choice(self.fire_chance)
    
    def process_events(self, event: pygame.event.EventType) -> None:
        pass
    
    def paint_bullets(self, size: int) -> None:
        for bullet in self.fired_bullets:
            bullet.paint(size)
            
    def calculate_rules(self, size: int) -> None:
        for bullet in self.fired_bullets:
            bullet.calculate_rules(size)
        
        if self.can_shoot():
            self.state = 'LOADED'
            
    def paint_ammo(self) -> None:
        ammo_bag = self.ammo_bag
        in_the_gun = self.bullets_in_the_gun
        
        ammo_text = f'{in_the_gun}  /  {ammo_bag}'
        ammo_render = font_30.render(ammo_text, True, cores.BRANCO)
        width_to_center = ammo_render.get_width() / 2
        
        self.screen.blit(ammo_render, (1350 - width_to_center, 800))
        
    def paint_reloading(self) -> None:
        reloading = 'RECARREGANDO...'
        reloading_render = font_20.render(reloading, True, cores.BRANCO)
        width_to_center = reloading_render.get_width() / 2
        self.screen.blit(reloading_render, (1350 - width_to_center, 850))
        
    def paint(self, size: int, paint_ammo: bool=False) -> None:
        self.paint_gun(size)
        self.paint_bullets(size)
        
        if paint_ammo:
            self.paint_ammo()
            
        if self.state == 'RELOADING':
            self.paint_reloading()
            
    
    @abstractmethod
    def paint_gun(self, size: int) -> None:
        pass
    
    @abstractmethod
    def reinit_stats(self) -> None:
        pass
    
    
class AK47(Weapon):
    
    
    def __init__(self, screen: pygame.Surface):
        self.ammo_capacity = 30
        self.bullets_in_the_gun = 40
        self.ammo_bag = 300
        self.fire_chance = [True for i in range(9)]
        self.fire_chance.append(False)
        self.bullet_speed = 7
        self.fired_bullets = []
        self.shoot_time = 0.25
        self.reload_time = 4
        self.time_passed_since_shoot = self.shoot_time
        self.time_passed_since_reload = self.reload_time
        self.screen = screen
        self.damage = 35
        self.time_since_bullet_flying = 0
        self.imprecision = [0 for i in range(4)]
        self.imprecision.append(1)
        self.imprecision.append(-1)
        self.state = 'LOADED'
        
    def paint_gun(self, size):
        pass
        
    def reinit_stats(self):
        self.ammo_capacity = 50
        self.bullets_in_the_gun = 50
        self.ammo_bag = 400
        self.fired_bullets = []
        

class Pistol(Weapon):
    
    
    def __init__(self, screen: pygame.Surface):
        self.ammo_capacity = 10
        self.bullets_in_the_gun = 10
        self.ammo_bag = 200
        self.fire_chance = [True for i in range(3)]
        self.fire_chance.append(False)
        self.bullet_speed = 4
        self.fired_bullets = []
        self.shoot_time = 0.5
        self.reload_time = 4
        self.time_passed_since_shoot = self.shoot_time
        self.time_passed_since_reload = self.reload_time
        self.screen = screen
        self.damage = 25
        self.time_since_bullet_flying = 0
        self.imprecision = [0 for i in range(18)]
        self.imprecision.append(1)
        self.imprecision.append(-1)
        self.state = 'LOADED'
        
    def paint_gun(self, size: int):
        pass
        
    def reinit_stats(self):
        self.ammo_capacity = 10
        self.bullets_in_the_gun = 10
        self.ammo_bag = 200
        self.fired_bullets = []
        

class Shotgun(Weapon):
    
    
    def __init__(self, screen: pygame.Surface):
        self.ammo_capacity = 5
        self.bullets_in_the_gun = 5
        self.ammo_bag = 100
        self.fire_chance = [True for i in range(2)]
        self.fire_chance.append(False)
        self.bullet_speed = 8
        self.fired_bullets = []
        self.shoot_time = 1
        self.reload_time = 6
        self.time_passed_since_shoot = self.shoot_time
        self.time_passed_since_reload = self.reload_time
        self.screen = screen
        self.damage = 100
        self.time_since_bullet_flying = 0.5
        self.imprecision = [0 for i in range(4)]
        self.imprecision.append(1)
        self.imprecision.append(-1)
        self.state = 'LOADED'
        
    def paint_gun(self, size: int):
        pass
        
    def reinit_stats(self):
        self.ammo_capacity = 5
        self.bullets_in_the_gun = 5
        self.ammo_bag = 100
        self.fired_bullets = []
        
        
class SMG(Weapon):
    
    
    def __init__(self, screen: pygame.Surface):
        self.ammo_capacity = 50
        self.bullets_in_the_gun = 50
        self.ammo_bag = 400
        self.fire_chance = [True for i in range(9)]
        self.fire_chance.append(False)
        self.bullet_speed = 6
        self.fired_bullets = []
        self.shoot_time = 0.1
        self.reload_time = 4
        self.time_passed_since_shoot = self.shoot_time
        self.time_passed_since_reload = self.reload_time
        self.screen = screen
        self.damage = 25
        self.time_since_bullet_flying = 0
        self.imprecision = [0 for i in range(2)]
        self.imprecision.append(1)
        self.imprecision.append(-1)
        self.state = 'LOADED'
        
    def paint_gun(self, size):
        pass
        
    def reinit_stats(self):
        self.ammo_capacity = 50
        self.bullets_in_the_gun = 50
        self.ammo_bag = 400
        self.fired_bullets = []


class Sniper(Weapon):
    
    
    def __init__(self, screen: pygame.Surface):
        self.ammo_capacity = 8
        self.bullets_in_the_gun = 8
        self.ammo_bag = 150
        self.fire_chance = [True]
        self.bullet_speed = 13
        self.fired_bullets = []
        self.shoot_time = 5
        self.reload_time = 5
        self.time_passed_since_shoot = self.shoot_time
        self.time_passed_since_reload = self.reload_time
        self.screen = screen
        self.damage = 200
        self.time_since_bullet_flying = 0
        self.imprecision = [0]
        self.state = 'LOADED'
        
    def paint_gun(self, size: int):
        pass
        
    def reinit_stats(self):
        self.ammo_capacity = 8
        self.bullets_in_the_gun = 8
        self.ammo_bag = 150
        self.fired_bullets = []