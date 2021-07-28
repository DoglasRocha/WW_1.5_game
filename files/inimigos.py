from abc import ABCMeta
from movivel import Movivel
from abc import ABCMeta, abstractmethod
from random import choice
from time import time
from guns import Pistol, SMG, AK47, Shotgun
import cores
import pygame

direcoes = ['NORTH', 'SOUTH', 'EAST', 'WEST', 'NORTH EAST', 'NORTH WEST', 'SOUTH EAST', 'SOUTH WEST']

class Inimigo(Movivel, metaclass=ABCMeta):
    
    @abstractmethod
    def pintar(self):
        pass
    
    def processar_eventos(self):
        if time() - self.tempo_que_andou >= self.tempo_andar:
            if len(self.direcoes) <= 0:
                direcao = choice(direcoes)
            else:
                direcao = choice(self.direcoes)
            self.andar(direcao)
            self.tempo_que_andou = time()
        if time() - self.tempo_que_atirou >= self.tempo_atirar:
            atira = choice(self.chance_tiro)
            if atira:
                self.atirar()
                self.tempo_que_atirou = time()
        
    def andar(self, direcao):
        directions_and_speeds = {'NORTH': (-self.SPEED, 0),
                                 'SOUTH': (self.SPEED, 0),
                                 'EAST': (0, self.SPEED),
                                 'WEST': (0, -self.SPEED),
                                 'NORTH EAST': (-self.SPEED, self.SPEED),
                                 'NORTH WEST': (-self.SPEED, -self.SPEED),
                                 'SOUTH EAST': (self.SPEED, self.SPEED),
                                 'SOUTH WEST': (self.SPEED, -self.SPEED)}
        
        ''' direction_to_move = directions_and_speeds[direction]
        self.y_speed, self.x_speed = direction_to_move '''
        
        if direcao == 'NORTH':
            self.y_speed = -self.SPEED
            self.x_speed = 0
        if direcao == 'SOUTH':
            self.y_speed = self.SPEED
            self.x_speed = 0
        if direcao == 'EAST':
            self.y_speed = 0
            self.x_speed = self.SPEED
        if direcao == 'WEST':
            self.y_speed = 0
            self.x_speed = -self.SPEED
        if direcao == 'NORTH EAST':
            self.y_speed = -self.SPEED
            self.x_speed = self.SPEED
        if direcao == 'NORTH WEST':
            self.y_speed = -self.SPEED
            self.x_speed = -self.SPEED
        if direcao == 'SOUTH EAST':
            self.y_speed = self.SPEED
            self.x_speed = self.SPEED
        if direcao == 'SOUTH WEST':
            self.y_speed = self.SPEED
            self.x_speed = -self.SPEED
    
    def atirar(self):
        self.weapon.shoot(self.personagem.x, self.personagem.y, self.x, self.y)
        
    def recusar_movimento(self, direcoes):
        self.direcoes = direcoes
        
class Recruta(Inimigo, Movivel):
    
    def __init__(self, tela, personagem):
        self.SPEED = 1
        self.x_speed = 0
        self.y_speed = 0
        self.tela = tela
        self.max_hp = 100
        self.hp = 100
        self.weapon = Pistol(tela)
        self.direcao = 'NORTH'
        self.balas_atiradas = []
        self.state = 'ALIVE'
        self.personagem = personagem
        self.tempo_andar = 6
        self.tempo_que_andou = self.tempo_andar
        self.tempo_atirar = 7.5
        self.tempo_que_atirou = self.tempo_atirar
        self.chance_tiro = [False for i in range(4)]
        self.chance_tiro.append(True)
        self.recompensa = 10
        self.time_passed = 0
    
    def pintar(self):
        if self.state == 'ALIVE':
            self.pintar_ALIVE()
        
    def pintar_ALIVE(self):
        pygame.draw.rect(self.tela, cores.AMARELO_ESVERDEADO, (self.x, self.y, self.size, self.size))
        self.weapon.paint(self.size)


class Soldado(Inimigo, Movivel):
    
    def __init__(self, tela, personagem):
        self.SPEED = 2
        self.x_speed = 0
        self.y_speed = 0
        self.tela = tela
        self.max_hp = 150
        self.hp = 150
        self.weapon = SMG(tela)
        self.direcao = 'NORTH'
        self.balas_atiradas = []
        self.state = 'ALIVE'
        self.personagem = personagem
        self.tempo_andar = 4
        self.tempo_que_andou = self.tempo_andar
        self.tempo_atirar = 4
        self.tempo_que_atirou = self.tempo_atirar
        self.chance_tiro = [False for i in range(3)]
        self.chance_tiro.append(True)
        self.recompensa = 25
        self.time_passed = 0
    
    def pintar(self):
        if self.state == 'ALIVE':
            self.pintar_ALIVE()
        
    def pintar_ALIVE(self):
        pygame.draw.rect(self.tela, cores.VERDE_LIMAO, (self.x, self.y, self.size, self.size))
        self.weapon.paint(self.size)
        
        
class Capitao(Inimigo, Movivel):
    
    def __init__(self, tela, personagem):
        self.SPEED = 1
        self.x_speed = 0
        self.y_speed = 0
        self.tela = tela
        self.max_hp = 125
        self.hp = 125
        self.weapon = AK47(tela)
        self.direcao = 'NORTH'
        self.balas_atiradas = []
        self.state = 'ALIVE'
        self.personagem = personagem
        self.tempo_andar = 3
        self.tempo_que_andou = self.tempo_andar
        self.tempo_atirar = 3
        self.tempo_que_atirou = self.tempo_atirar
        self.chance_tiro = [False for i in range(3)]
        self.chance_tiro.append(True)
        self.recompensa = 50
        self.time_passed = 0
    
    def pintar(self):
        if self.state == 'ALIVE':
            self.pintar_ALIVE()
        
    def pintar_ALIVE(self):
        pygame.draw.rect(self.tela, cores.VERDE_ESCURO, (self.x, self.y, self.size, self.size))
        self.weapon.paint(self.size)
        
        
class General(Inimigo, Movivel):
    
    def __init__(self, tela, personagem):
        self.SPEED = 2
        self.x_speed = 0
        self.y_speed = 0
        self.tela = tela
        self.max_hp = 300
        self.hp = 300
        self.weapon = Shotgun(tela)
        self.direcao = 'NORTH'
        self.balas_atiradas = []
        self.state = 'ALIVE'
        self.personagem = personagem
        self.tempo_andar = 6
        self.tempo_que_andou = self.tempo_andar
        self.tempo_atirar = 5
        self.tempo_que_atirou = self.tempo_atirar
        self.chance_tiro = [False for i in range(2)]
        self.chance_tiro.append(True)
        self.recompensa = 200
        self.time_passed = 0
    
    def pintar(self):
        if self.state == 'ALIVE':
            self.pintar_ALIVE()
        
    def pintar_ALIVE(self):
        pygame.draw.rect(self.tela, cores.DOURADO, (self.x, self.y, self.size, self.size))
        self.weapon.paint(self.size)
        