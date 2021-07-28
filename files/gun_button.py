from guns import Weapon
from typing import Callable
from pygame.event import Event
from pygame import Surface
from game_element import GameElement
import pygame

font_20 = pygame.font.SysFont('arial', 20, True)
font_50 = pygame.font.SysFont('arial', 50, True)

class GunButton(GameElement):


    def __init__(self, x: int, y: int, gun_receiver: Callable,
                 state_changer: Callable, screen: Surface,
                 unfocused_border_color: tuple,
                 unfocused_text_color: tuple,
                 focused_button_color: tuple,
                 focused_text_color: tuple,
                 gun: Weapon) -> None:
        self.x = x
        self.gun_receiver = gun_receiver
        self.state_changer = state_changer
        self.screen = screen
        self.unfocused_border_color = unfocused_border_color
        self.unfocused_text_color = unfocused_text_color
        self.focused_button_color = focused_button_color
        self.focused_text_color = focused_text_color
        self.gun = gun
        self.gun_instance = self.gun(self.screen)
        self.state = 'NOT FOCUSED'
        self.renders = []
        self.render_weapon(self.unfocused_text_color)
        self.width = self.get_max_width() + 60
        self.height = self.get_height() + 60
        self.line_height = self.get_one_line_height()
        self.weapon_name_height = self.get_weapon_name_height()
        self.x_rect = x - self.width // 2
        self.centered_y = y - self.height // 2

    def process_events(self, event: Event, mouse: tuple) -> None:
        mouse_buttons_pressed, mouse_position = mouse
        x, y = mouse_position

        if self.has_click_inside_the_button(x, y,
                                            mouse_buttons_pressed):
            self.gun_receiver(self.gun)
            self.state_changer('PLAYING')

    def calculate_rules(self, mouse_position: tuple) -> None:
        if self.is_mouse_inside_the_button(mouse_position[0], mouse_position[1]):
            self.state = 'FOCUSED'
        else:
            self.state = 'NOT FOCUSED'

    def is_mouse_inside_the_button(self, x: int, y: int) -> bool:
        return (self.x_rect <= x <= self.x_rect + self.width) and \
               (self.centered_y <= y <= self.centered_y + self.height)

    def has_click_inside_the_button(self, x: int, y: int,
                                    mouse_buttons: tuple) -> bool:
        return self.is_mouse_inside_the_button(x, y) and \
            any(mouse_buttons)

    def paint(self) -> None:
        states_and_paintings = {'NOT FOCUSED': self.paint_not_focused,
                              'FOCUSED': self.paint_focused}

        painting = states_and_paintings[self.state]
        painting()

    def paint_focused(self) -> None:
        pygame.draw.rect(self.screen, self.focused_button_color,
                         (self.x_rect,
                          self.centered_y,
                          self.width,
                          self.height),
                         border_radius=self.width // 25)

        self.render_weapon(self.focused_text_color)
        self.render_painter()

    def paint_not_focused(self) -> None:
        pygame.draw.rect(self.screen, self.unfocused_border_color,
                         (self.x_rect,
                          self.centered_y,
                          self.width,
                          self.height), self.width // 25,
                         self.width // 25)

        self.render_weapon(self.unfocused_text_color)
        self.render_painter()
                
    def render_painter(self) -> None:
        y = self.centered_y
        y += 20 + self.weapon_name_height // 2
        
        for i in range(len(self.renders)):
            render = self.renders[i]
            self.paint_centered_render(render, y)
            
            if i == 0:
                y += self.weapon_name_height
                
            else:
                y += self.line_height
                
    def paint_centered_render(self, render: Surface, y_coordinate: str) -> None:
        cent_x = render.get_width() / 2
        cent_y = render.get_height() / 2
        self.screen.blit(render, (self.x - cent_x, y_coordinate - cent_y))
        
    def render_weapon(self, text_color: tuple) -> None:
        self.renders = []
        
        nome = self.gun.__name__
        capacidade_municao = self.gun_instance.ammo_capacity
        bolsa = self.gun_instance.ammo_bag
        precisao = f'{round((self.gun_instance.imprecision.count(0) / len(self.gun_instance.imprecision)) * 100, 2)}%'
        chance_tiro = f'{round((self.gun_instance.fire_chance.count(True) / len(self.gun_instance.fire_chance)) * 100, 2)}%'
        fire_rate = f'{self.gun_instance.time_passed_since_shoot} s'
        tempo_recarga = f'{self.gun_instance.time_passed_since_reload} s'
        dano = f'{self.gun_instance.damage}'
        
        info_arma = f'''Capacidade da arma: {capacidade_municao} balas
        Bolsa de Munição: {bolsa} balas
        Precisão da Arma: {precisao}
        Chance da Arma atirar: {chance_tiro}
        Frequência de Tiro: {fire_rate}
        Tempo de Recarga: {tempo_recarga}
        Dano: {dano} pontos'''
        
        lines = info_arma.splitlines()
        for i in range(len(lines)): 
            lines[i] = lines[i].strip()
        
        render_nome_arma = font_50.render(nome, True, text_color)
        self.renders.append(render_nome_arma)
        for line in lines: 
            self.renders.append(font_20.render(line, True, text_color))
    
    def get_max_width(self) -> int:
        render_widths = [render.get_width() for render in self.renders]
        
        return max(render_widths)
    
    def get_height(self) -> int:
        render_heights = [render.get_height() for render in self.renders]
        
        return sum(render_heights)
    
    def get_one_line_height(self) -> int:
        height = self.renders[1].get_height()
        
        return height
        
    def get_weapon_name_height(self) -> int:
        height = self.renders[0].get_height()
        
        return height