from abc import ABCMeta
from movivel import Movivel
from abc import ABCMeta, abstractmethod
from random import choice
from time import time
from guns import Pistol, SMG, AK47, Shotgun
import cores
import pygame

direcoes = ['NORTE', 'SUL', 'LESTE', 'OESTE', 'NORDESTE', 'NOROESTE', 'SUDESTE', 'SUDOESTE']

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
        if direcao == 'NORTE':
            self.vel_y = -self.velocidade
            self.vel_x = 0
        if direcao == 'SUL':
            self.vel_y = self.velocidade
            self.vel_x = 0
        if direcao == 'LESTE':
            self.vel_y = 0
            self.vel_x = self.velocidade
        if direcao == 'OESTE':
            self.vel_y = 0
            self.vel_x = -self.velocidade
        if direcao == 'NORDESTE':
            self.vel_y = -self.velocidade
            self.vel_x = self.velocidade
        if direcao == 'NOROESTE':
            self.vel_y = -self.velocidade
            self.vel_x = -self.velocidade
        if direcao == 'SUDESTE':
            self.vel_y = self.velocidade
            self.vel_x = self.velocidade
        if direcao == 'SUDOESTE':
            self.vel_y = self.velocidade
            self.vel_x = -self.velocidade
    
    def atirar(self):
        self.weapon.shoot(self.personagem.x, self.personagem.y, self.x, self.y)
        
    def recusar_movimento(self, direcoes):
        self.direcoes = direcoes
        
class Recruta(Inimigo, Movivel):
    
    def __init__(self, tela, personagem):
        self.velocidade = 1
        self.vel_x = 0
        self.vel_y = 0
        self.tela = tela
        self.max_hp = 100
        self.hp = 100
        self.weapon = Pistol(tela)
        self.direcao = 'NORTE'
        self.balas_atiradas = []
        self.estado = 'VIVO'
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
        if self.estado == 'VIVO':
            self.pintar_vivo()
        
    def pintar_vivo(self):
        pygame.draw.rect(self.tela, cores.AMARELO_ESVERDEADO, (self.x, self.y, self.tamanho, self.tamanho))
        self.weapon.paint(self.tamanho)


class Soldado(Inimigo, Movivel):
    
    def __init__(self, tela, personagem):
        self.velocidade = 2
        self.vel_x = 0
        self.vel_y = 0
        self.tela = tela
        self.max_hp = 150
        self.hp = 150
        self.weapon = SMG(tela)
        self.direcao = 'NORTE'
        self.balas_atiradas = []
        self.estado = 'VIVO'
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
        if self.estado == 'VIVO':
            self.pintar_vivo()
        
    def pintar_vivo(self):
        pygame.draw.rect(self.tela, cores.VERDE_LIMAO, (self.x, self.y, self.tamanho, self.tamanho))
        self.weapon.paint(self.tamanho)
        
        
class Capitao(Inimigo, Movivel):
    
    def __init__(self, tela, personagem):
        self.velocidade = 1
        self.vel_x = 0
        self.vel_y = 0
        self.tela = tela
        self.max_hp = 125
        self.hp = 125
        self.weapon = AK47(tela)
        self.direcao = 'NORTE'
        self.balas_atiradas = []
        self.estado = 'VIVO'
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
        if self.estado == 'VIVO':
            self.pintar_vivo()
        
    def pintar_vivo(self):
        pygame.draw.rect(self.tela, cores.VERDE_ESCURO, (self.x, self.y, self.tamanho, self.tamanho))
        self.weapon.paint(self.tamanho)
        
        
class General(Inimigo, Movivel):
    
    def __init__(self, tela, personagem):
        self.velocidade = 2
        self.vel_x = 0
        self.vel_y = 0
        self.tela = tela
        self.max_hp = 300
        self.hp = 300
        self.weapon = Shotgun(tela)
        self.direcao = 'NORTE'
        self.balas_atiradas = []
        self.estado = 'VIVO'
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
        if self.estado == 'VIVO':
            self.pintar_vivo()
        
    def pintar_vivo(self):
        pygame.draw.rect(self.tela, cores.DOURADO, (self.x, self.y, self.tamanho, self.tamanho))
        self.weapon.paint(self.tamanho)
        