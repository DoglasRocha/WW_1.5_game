from back_button import BackButton
import pygame
from pygame.event import Event
import cores
from score_manager import ScoreManager
from game_element import GameElement
from enemies import Enemy, Recruit, Soldier, Captain, General
from character import Character
from matrix import Matrix
from time import time
from main_menu import MainMenu

fonte_20 = pygame.font.SysFont('arial', 20, True)
fonte_10 = pygame.font.SysFont('arial', 15, True)
fonte_50 = pygame.font.SysFont('times new roman', 50, True)

class Cenario(GameElement):
    
    
    def __init__(self, tela):
        self.state = 'MENU PRINCIPAL'
        self.nivel = 1
        self.objeto_matriz = Matrix(self.nivel, tela)
        self.matriz = self.objeto_matriz.get_matrix()
        self.tamanho = self.objeto_matriz.get_size()
        self.blocos_na_matriz = self.objeto_matriz.get_number_of_blocks()
        self.paredes = self.objeto_matriz.get_walls()
        self.tela = tela
        self.menu = MainMenu(self.tela)
        self.personagem = Character(self.tela)
        self.instanciamento_moviveis()
        self.clock = pygame.time.Clock()
        self.tempo_para_passar = 2.5
        self.tempo_que_passou = self.tempo_para_passar
        self.passou_tempo = time() - self.tempo_que_passou >= self.tempo_para_passar
        self.score_manager = ScoreManager()
        self.define_fps()
        back_button = BackButton(10, 10, 150, 25, self.state_changer,
                                 'MENU PRINCIPAL', self.score_manager.save_score,
                                 self.tela, 'VOLTAR', cores.BRANCO, cores.BRANCO,
                                 cores.BRANCO, cores.PRETO, fonte_10)
        self.buttons = [back_button]
        
    '''passagem tempo'''
    @property
    def ja_passou_o_tempo(self):
        return time() - self.tempo_que_passou >= self.tempo_para_passar
    
    '''calculo das regras'''
    
    def calculate_rules(self, mouse: tuple):
        for button in self.buttons:
            button.calculate_rules(mouse[1])
        if self.state == 'JOGANDO':
            if len(self.moviveis) <= 1:
                self.state = 'PASSANDO NIVEL'
                self.tempo_que_passou = time()
            else:
                for movivel in self.moviveis:
                    movivel.calculate_rules()
                    self.calcula_regras_jogando(movivel)
        elif self.state == 'PASSANDO NIVEL' and self.ja_passou_o_tempo:
            for button in self.buttons:
                button.calculate_rules(mouse[1])
            self.passa_o_nivel()
        elif self.state == 'DEAD' and self.ja_passou_o_tempo:
            for button in self.buttons:
                button.calculate_rules(mouse[1])
            self.reinicia_o_nivel()
        elif self.state == 'MENU PRINCIPAL':
            self.menu.calculate_rules(mouse)
            
    def calcula_regras_jogando(self, movivel):
        if movivel.state == 'ALIVE':
            
            for bala in movivel.weapon.fired_bullets:
                for _movivel in self.moviveis:
                    if _movivel != movivel:
                        _movivel.analyse_shot(bala, movivel)
                        
                if self.colide_com_parede(bala):
                    bala.collided()
                    movivel.weapon.fired_bullets.remove(bala)
                    del bala
                    
            column_where_the_movable_is = self.matriz[movivel.line][movivel.column]
            if column_where_the_movable_is in (6,7,8,12):
                damages_and_times = {6: (5, 5),
                                     7: (10, 5),
                                     8: (4, 2),
                                    12: (3, 2)}
                        
                damage_and_time = damages_and_times[column_where_the_movable_is]
                movivel.take_damage_from_environment(damage_and_time)
                    
            elif column_where_the_movable_is == 10:
                movivel.receive_ammo(50)
                self.objeto_matriz.clear_ammo(movivel.line, movivel.column)
                        
            elif column_where_the_movable_is == 11:
                movivel.gain_hp(50)
                self.objeto_matriz.clear_health_kit(movivel.line, movivel.column)
                            
            if self.colide_com_parede(movivel) or self.colide_com_movivel(movivel):
                if isinstance(movivel, Enemy):
                    direcoes_possiveis = self.get_direcoes(movivel.line, movivel.column)
                    movivel.refuse_movement(direcoes_possiveis)
                else:
                    movivel.refuse_movement()
            else:
                movivel.accept_movement()
        elif movivel.state == 'DEAD':
            if isinstance(movivel, Enemy):
                self.moviveis.remove(movivel)
                self.score_manager.add_points(movivel.reward)
                del movivel
            elif isinstance(movivel, Character):
                self.state = 'DEAD'
                self.tempo_que_passou = time()
        
    def colide_com_parede(self, movivel):
        pode_mover = []
        for lin_intencao, col_intencao in movivel.hitbox: 
            colide_com_parede = self.matriz[lin_intencao][col_intencao] in self.paredes
            pode_mover.append(colide_com_parede)

        return any(pode_mover)
    
    def colide_com_movivel(self, movivel):
        colide_com_movivel = []
        for lin_intencao, col_intencao in movivel.hitbox:
            for _movivel in self.moviveis:
                if id(movivel) != id(_movivel) and not isinstance(movivel, Enemy):
                    colide = _movivel.line == lin_intencao and _movivel.column == col_intencao
                    colide_com_movivel.append(colide)
                
        return any(colide_com_movivel)
    
    def get_direcoes(self, linha, coluna):
        direcoes = []
        
        if self.matriz[int(linha - 1)][int(coluna)] not in self.paredes:
            direcoes.append('NORTH')
            
        if self.matriz[int(linha + 1)][int(coluna)] not in self.paredes:
            direcoes.append('SOUTH')
            
        if self.matriz[int(linha)][int(coluna - 1)] not in self.paredes:
            direcoes.append('WEST')
            
        if self.matriz[int(linha)][int(coluna + 1)] not in self.paredes:
            direcoes.append('EAST')
            
        if self.matriz[int(linha - 1)][int(coluna + 1)] not in self.paredes:
            direcoes.append('NORTH EAST')
            
        if self.matriz[int(linha - 1)][int(coluna - 1)] not in self.paredes:
            direcoes.append('NORTH WEST')
            
        if self.matriz[int(linha + 1)][int(coluna + 1)] not in self.paredes:
            direcoes.append('SOUTH EAST')
            
        if self.matriz[int(linha + 1)][int(coluna - 1)] not in self.paredes:
            direcoes.append('SOUTH WEST')
            
        return direcoes
    
    def state_changer(self, new_state: str):
        self.state = new_state
    
    '''processamento de eventos'''
    
    def process_events(self, eventos, teclado, mouse):
        for e in eventos:
            if e.type == pygame.QUIT:
                self.score_manager.save_score()
                exit()
            elif self.state == 'MENU PRINCIPAL' and e.type == pygame.MOUSEBUTTONDOWN:
                self.menu.process_events(e, mouse)
                if self.menu.allowed_to_play():
                    weapon = self.menu.get_gun()(self.tela)
                    self.personagem.receive_weapon(weapon)
                    self.menu.reset()
                    self.inicia_o_nivel()
            elif self.state == 'JOGANDO':
                for button in self.buttons:
                    button.process_events(e, mouse)
                self.processar_eventos_jogando(e, teclado, mouse)
            elif self.state == 'PAUSADO':
                for button in self.buttons:
                    button.process_events(e, mouse)
                self.processar_eventos_pausado(e)
                
    def processar_eventos_jogando(self, evento, teclado, mouse):
        tecla_pressionada = evento.type == pygame.KEYDOWN
        if tecla_pressionada:
            tecla = evento.key
            esc = pygame.K_ESCAPE
            
            if tecla == esc:
                self.state = 'PAUSADO'
                
        for movivel in self.moviveis:
            if isinstance(movivel, Character):
                movivel.process_events(evento, teclado, mouse)
            else:
                movivel.process_events()
        
    def processar_eventos_pausado(self, evento):
        esc_pressionado = evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE
        
        if esc_pressionado:
            self.state = 'JOGANDO'
                    
    '''pintura'''
                               
    def paint(self):
        if self.state == 'MENU PRINCIPAL':
            self.menu.paint()
        elif self.state == 'JOGANDO':
            self.pintar_jogando()
        elif self.state == 'PAUSADO':
            self.pintar_pausado()
        elif self.state == 'PASSANDO NIVEL':
            self.pintar_passagem_nivel()
        elif self.state == 'DEAD':
            self.pintar_DEAD()
        elif self.state == 'VITORIA':
            self.pintar_vitoria()
        
            
    def pintar_linha(self, numero_linha, linha):
        for numero_coluna, coluna in enumerate(linha):
            x = numero_coluna * self.tamanho + 300
            y = numero_linha * self.tamanho
            
            all_colors = {0: cores.VERDE, 1: cores.BRANCO, 2: cores.AMARELO,
                          3: cores.CINZA, 4: cores.CINZA_ESCURO, 5: cores.LARANJA,
                          6: cores.MARROM_ESCURO, 7: cores.MARROM_CLARO, 8: cores.PRATA,
                          9: cores.LARANJA_FEIO, 10: cores.AZUL_ACO, 11: cores.VERMELHO,
                          12: cores.MARROM_FEIO}
            
            color = all_colors[coluna]
            
            pygame.draw.rect(self.tela, color, (x, y, self.tamanho, self.tamanho))

    def pintar_texto(self, texto, x, y, fonte, cor):
        render = fonte.render(texto, True, cor)
        cent_x = render.get_width() / 2
        cent_y = render.get_height() / 2
        self.tela.blit(render, (x - cent_x, y - cent_y))
        
    def pintar_jogando(self):
        for numero_linha, linha in enumerate(self.matriz):
            self.pintar_linha(numero_linha, linha)
        for movivel in self.moviveis:
            movivel.paint()
        self.paint_side_bar()
        for button in self.buttons:
            button.paint()
                
    def pintar_pausado(self):
        self.pintar_jogando()
        pausado = 'P A U S A D O'
        self.pintar_texto(pausado, 750, 450, fonte_50, cores.BRANCO)
    
    def pintar_passagem_nivel(self):
        mensagem = 'PARABÉNS, VOCÊ PASSOU DE NÍVEL!'
        self.pintar_texto(mensagem, 750, 450, fonte_50, cores.BRANCO)
    
    def pintar_vitoria(self):
        mensagem = 'PARABÉNS, VOCÊ VENCEU!!!'
        pontuacao = f'SUA PONTUAÇÃO FOI DE {self.score_manager.get_general_score()} PONTOS'
        self.pintar_texto(mensagem, 750, 425, fonte_50, cores.BRANCO)
        self.pintar_texto(pontuacao, 750, 475, fonte_50, cores.BRANCO)
        
        pygame.draw.rect(self.tela, cores.AMARELO, (650, 425, 200, 50))
        self.pintar_texto('VOLTAR AO MENU PRINCIPAL', 750, 450, fonte_50, cores.BRANCO)
    
    def pintar_DEAD(self):
        mensagem = 'VOCÊ MORREU... :('
        mensagem_2 = 'VAI TER QUE COMEÇAR O NÍVEL NOVAMENTE... :/'
        self.pintar_texto(mensagem, 750, 425, fonte_50, cores.BRANCO)
        self.pintar_texto(mensagem_2, 750, 475, fonte_50, cores.BRANCO)
    
    def paint_side_bar(self):
        self.pintar_score()
        self.paint_records()
    
    def pintar_score(self):
        pontuacao_total = f'Pontuação Geral: {round(self.score_manager.get_general_score(), 2)}'
        nivel = f'Nível: {self.nivel}'
        pontuacao_nivel = f'Pontuação no Nível: {round(self.score_manager.get_level_score(), 2)}'
        tentativa = f'Tentativa nº: {self.score_manager.get_attempt()}'
        
        self.pintar_texto(pontuacao_total, 1350, 25, fonte_20, cores.BRANCO)
        self.pintar_texto(nivel, 1350, 75, fonte_20, cores.BRANCO)
        self.pintar_texto(pontuacao_nivel, 1350, 125, fonte_20, cores.BRANCO)
        self.pintar_texto(tentativa, 1350, 175, fonte_20, cores.BRANCO)
        
    def paint_records(self):
        title = 'RECORDES DE PONTUAÇÃO'
        self.pintar_texto(title, 1350, 410, fonte_20, cores.BRANCO)
        
        five_biggest_scores = self.score_manager.get_five_biggest_scores()
        
        position_y = 440
        for key, value in five_biggest_scores.items():
            date = key
            text = f'{date} ... {value:5.2f} pontos'
            
            self.pintar_texto(text, 1350, position_y, fonte_10, cores.BRANCO)
            position_y += 20
            
    '''logica de niveis'''
    
    def inicia_o_nivel(self):
        self.personagem.reinit_stats()
        self.objeto_matriz = Matrix(self.nivel, self.tela)
        self.matriz = self.objeto_matriz.get_matrix()
        self.tamanho = self.objeto_matriz.get_size()
        self.blocos_na_matriz = self.objeto_matriz.get_number_of_blocks()
        self.instanciamento_moviveis()
        self.define_fps()
        self.state = 'JOGANDO'
        
    def passa_o_nivel(self):
        self.nivel += 1
        self.score_manager.to_next_level()
        self.inicia_o_nivel()
        
    def reinicia_o_nivel(self):
        self.score_manager.re_init_level()
        self.inicia_o_nivel()
        
    '''nascimento dos moviveis'''
    def instanciamento_moviveis(self):
        self.moviveis = []
        self.moviveis.append(self.personagem)
        for i in range(int(self.nivel)):
            self.moviveis.append(Recruit(self.tela, self.personagem))
        for i in range(int(self.nivel * 0.5)):
            self.moviveis.append(Soldier(self.tela, self.personagem))
        for i in range(int(self.nivel * 0.2)):
            self.moviveis.append(Captain(self.tela, self.personagem))
        for i in range(int(self.nivel * 0.1)):
            self.moviveis.append(General(self.tela, self.personagem))
        for movivel in self.moviveis:
            if isinstance(movivel, Character):
                movivel.define_geometric_stats(len(self.matriz[0]) - 2, len(self.matriz[0]) - 2, self.tamanho)
            else:
                movivel.define_geometric_stats(1, 1, self.tamanho)
    
    '''calculo dos fps'''
    def define_fps(self):
        fps = 2420 // self.blocos_na_matriz
        self.clock.tick(fps)
        