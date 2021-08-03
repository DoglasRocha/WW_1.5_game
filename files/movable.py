from abc import ABCMeta, abstractmethod
from time import time
from bullet import Bullet

class Movable(metaclass=ABCMeta):
    
    def define_geometric_stats(self, line: list, column: int, size: int) -> None:
        self.directions = []
        self.line = line
        self.column = column
        self.size = size
        self.hitbox = [(self.line, self.column)]
        self.x = self.column * self.size + 300
        self.y = self.line * self.size
        self.intention_x = self.x
        self.intention_y = self.y
            
    def calculate_rules(self) -> None:
        self.intention_x = self.x + self.x_speed
        self.intention_y = self.y + self.y_speed
        self.line = self.y // self.size
        self.column = (self.x - 300) // self.size
            
        self.hitbox = []
        
        # 0 = canto superior esquerdo, 1 = canto superior direito
        # 2 = canto inferior esquerdo, 2 = canto inferior esquerdo
            
        line_intention_0 = int((self.intention_y) / self.size)
        col_intention_0 = int((self.intention_x - 300) / self.size)
        self.hitbox.append((line_intention_0, col_intention_0))
            
        line_intention_1 = int((self.intention_y) / self.size)
        col_intention_1 = int((self.intention_x + self.size - 1 - 300) / self.size)
        self.hitbox.append((line_intention_1, col_intention_1))
            
        line_intention_3 = int((self.intention_y + self.size - 1) / self.size)
        col_intention_2 = int((self.intention_x - 300) / self.size)
        self.hitbox.append((line_intention_3, col_intention_2))
            
        lin_intencao_3 = int((self.intention_y + self.size - 1) / self.size)
        col_intention_3 = int((self.intention_x + self.size - 1 - 300) / self.size)
        self.hitbox.append((lin_intencao_3, col_intention_3))
                
        self.weapon.calculate_rules(self.size)
        
        if self.hp <= 0:
            self.state = 'DEAD'
    
    def accept_movement(self) -> None:
        self.x = self.intention_x
        self.y = self.intention_y
        
    def refuse_movement(self) -> None:
        pass
    
    def analyse_shot(self, bullet: Bullet, movable) -> None:
        if (self.x < bullet.x < (self.x + self.size)) \
        and (self.y < bullet.y < (self.y + self.size)) \
        and bullet in movable.weapon.fired_bullets:
            self.take_damage_from_bullet(bullet.damage)
            bullet.collided()
            movable.weapon.fired_bullets.remove(bullet)
            del bullet
            
    def has_the_time_passed(self, stipulated_time: int) -> bool:
        if time() - self.time_passed > stipulated_time:
            self.time_passed = time()
            return True
        return False
    
    def take_damage_from_environment(self, damage_and_time: tuple) -> None:
        damage, time = damage_and_time
        if self.has_the_time_passed(time):
            self.hp -= damage
            
    def take_damage_from_bullet(self, damage: int) -> None:
        self.hp -= damage
        
    def receive_ammo(self, ammo: int) -> None:
        self.weapon.ammo_bag += ammo
        
    def gain_hp(self, hp: int) -> None:
        possible_hp_to_gain = self.max_hp - self.hp
        if possible_hp_to_gain < hp:
            self.hp += possible_hp_to_gain
        else:
            self.hp += hp
        
    @abstractmethod
    def paint(self):
        pass
    
    @abstractmethod
    def process_events(self):
        pass