from guns import Weapon
import pygame
import cores
from movivel import Movivel
from time import time

fonte_30 = pygame.font.SysFont('arial', 30, True)

class Personagem(Movivel):
    
    def __init__(self, tela):
        self.velocidade = 1
        self.vel_x = 0
        self.vel_y = 0
        self.tela = tela
        self.max_hp = 100
        self.hp = 100
        self.weapon = None
        self.direcao = 'NORTE'
        self.estado = 'VIVO'
        self.tempo_que_morreu = None
        self.time_passed = 0

    def pintar(self):
        pygame.draw.rect(self.tela, cores.CIANO, (self.x, self.y, self.tamanho, self.tamanho))
        self.pintar_vida()
        self.weapon.paint(self.tamanho, True)
        
    def pintar_vida(self):
        vida = f'HP: {self.hp}'
        render_vida = fonte_30.render(vida, True, cores.BRANCO)
        largura_para_centralizar = render_vida.get_width() / 2
        self.tela.blit(render_vida, (1350 - largura_para_centralizar, 750))
        
    def reinicia_stats(self):
        self.hp = 100
        self.weapon.reinit_stats()
        self.estado = 'VIVO'
        self.direcao = 'NORTE'
    
    def processar_eventos(self, evento, teclado, mouse):
        w = pygame.K_w
        a = pygame.K_a
        s = pygame.K_s
        d = pygame.K_d
        
        w_pressionado = bool(teclado[w])
        a_pressionado = bool(teclado[a])
        s_pressionado = bool(teclado[s])
        d_pressionado = bool(teclado[d])
            
        if w_pressionado and a_pressionado:
            self.vel_y = -self.velocidade
            self.vel_x = -self.velocidade
            self.direcao = 'NOROESTE'
        elif w_pressionado and d_pressionado:
            self.vel_y = -self.velocidade
            self.vel_x = self.velocidade
            self.direcao = 'NORDESTE'
        elif s_pressionado and a_pressionado:
            self.vel_y = self.velocidade
            self.vel_x = -self.velocidade
            self.direcao = 'SUDOESTE'
        elif s_pressionado and d_pressionado:
            self.vel_y = self.velocidade
            self.vel_x = self.velocidade
            self.direcao = 'SUDESTE'
        elif s_pressionado and w_pressionado:
            self.vel_y = 0
        elif a_pressionado and d_pressionado:
            self.vel_x = 0
            
        elif w_pressionado:
            self.vel_y = -self.velocidade
            self.direcao = 'NORTE'
        elif a_pressionado:
            self.vel_x = -self.velocidade
            self.direcao = 'OESTE'
        elif s_pressionado:
            self.vel_y = self.velocidade
            self.direcao = 'SUL'
        elif d_pressionado:
            self.vel_x = self.velocidade
            self.direcao = 'LESTE'
            
        tecla_solta = evento.type == pygame.KEYUP   
        if tecla_solta:
            tecla = evento.key
            if tecla == w:
                self.vel_y = 0
            if tecla == a:
                self.vel_x = 0
            if tecla == s:
                self.vel_y = 0
            if tecla == d:
                self.vel_x = 0
        
        if any(mouse[0]):
            self.weapon.shoot(mouse[1][0], mouse[1][1], self.x, self.y)
    
    def receive_weapon(self, weapon: Weapon):
        self.weapon = weapon
        