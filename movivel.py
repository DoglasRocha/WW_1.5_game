from abc import ABCMeta, abstractmethod
from time import time

class Movivel(metaclass=ABCMeta):
    
    def define_caracteristicas_geometricas(self, linha, coluna, size):
        self.direcoes = []
        self.linha = linha
        self.coluna = coluna
        self.size = size
        self.hitbox = [(self.linha, self.coluna)]
        self.x = self.coluna * self.size + 300
        self.y = self.linha * self.size
        self.x_intencao = self.x
        self.y_intencao = self.y
            
    def calcular_regras(self):
        if self.estado == 'ALIVE':
            self.calcular_regras_ALIVE()
            if self.hp <= 0:
                self.estado = 'DEAD'
            
    def calcular_regras_ALIVE(self):
        self.x_intencao = self.x + self.vel_x
        self.y_intencao = self.y + self.vel_y
        self.linha = self.y // self.size
        self.coluna = (self.x - 300) // self.size
            
        self.hitbox = []
        
        # 0 = canto superior esquerdo, 1 = canto superior direito
        # 2 = canto inferior esquerdo, 2 = canto inferior esquerdo
            
        lin_intencao_0 = int((self.y_intencao) / self.size)
        col_intencao_0 = int((self.x_intencao - 300) / self.size)
        self.hitbox.append((lin_intencao_0, col_intencao_0))
            
        lin_intencao_1 = int((self.y_intencao) / self.size)
        col_intencao_1 = int((self.x_intencao + self.size - 1 - 300) / self.size)
        self.hitbox.append((lin_intencao_1, col_intencao_1))
            
        lin_intencao_2 = int((self.y_intencao + self.size - 1) / self.size)
        col_intencao_2 = int((self.x_intencao - 300) / self.size)
        self.hitbox.append((lin_intencao_2, col_intencao_2))
            
        lin_intencao_3 = int((self.y_intencao + self.size - 1) / self.size)
        col_intencao_3 = int((self.x_intencao + self.size - 1 - 300) / self.size)
        self.hitbox.append((lin_intencao_3, col_intencao_3))
                
        self.weapon.calculate_rules(self.size)
    
    def aceitar_movimento(self):
        self.x = self.x_intencao
        self.y = self.y_intencao
        
    def recusar_movimento(self):
        pass
    
    def analisar_tiro(self, bala, movivel):
        if (self.x < bala.x < (self.x + self.size)) and (self.y < bala.y < (self.y + self.size)) and \
        bala in movivel.weapon.fired_bullets:
            self.take_damage_from_bullet(bala.damage)
            bala.collided()
            movivel.weapon.fired_bullets.remove(bala)
            del bala
            
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
    def pintar(self):
        pass