from typing import Callable
from pygame.event import Event
from pygame import Surface
from game_element import GameElement
from pygame.font import Font
import pygame


class Button(GameElement):


    def __init__(self, x: int, y: int, width: int, height: int,
                 state_changer: Callable, new_state: str,
                 screen: Surface, text: str,
                 unfocused_border_color: tuple,
                 unfocused_text_color: tuple,
                 focused_button_color: tuple,
                 focused_text_color: tuple,
                 font: Font) -> None:
        self.x = x
        self.width = width
        self.y = y
        self.height = height
        self.new_state = new_state
        self.state_changer = state_changer
        self.screen = screen
        self.text = text
        self.unfocused_border_color = unfocused_border_color
        self.unfocused_text_color = unfocused_text_color
        self.focused_button_color = focused_button_color
        self.focused_text_color = focused_text_color
        self.font = font
        self.state = 'NOT FOCUSED'

    '''processing events'''
    def process_events(self, event: Event, mouse: tuple) -> None:
        mouse_buttons_pressed = mouse[0]
        mouse_position = mouse[1]

        if self.has_click_inside_the_button(mouse_position[0],
                                            mouse_position[1],
                                            mouse_buttons_pressed):
            self.state_changer(self.new_state)

    '''calculating rules'''
    def calculate_rules(self, mouse_position: tuple) -> None:
        if self.is_mouse_inside_the_button(mouse_position[0], mouse_position[1]):
            self.state = 'FOCUSED'
        else:
            self.state = 'NOT FOCUSED'

    def is_mouse_inside_the_button(self, x: int, y: int) -> bool:
        return (self.x <= x <= self.x + self.width) and \
               (self.y <= y <= self.y + self.height)

    def has_click_inside_the_button(self, x: int, y: int,
                                    mouse_buttons: tuple) -> bool:
        return self.is_mouse_inside_the_button(x, y) and \
            any(mouse_buttons)

    '''painting'''
    def paint(self):
        states_and_paintings = {'NOT FOCUSED': self.paint_not_focused,
                              'FOCUSED': self.paint_focused}

        painting = states_and_paintings[self.state]
        painting()

    def paint_focused(self):
        pygame.draw.rect(self.screen, self.focused_button_color,
                         (self.x,
                          self.y,
                          self.width,
                          self.height),
                         border_radius=self.height // 10)

        self.paint_text(self.focused_text_color)

    def paint_not_focused(self):
        pygame.draw.rect(self.screen, self.unfocused_border_color,
                         (self.x,
                          self.y,
                          self.width,
                          self.height), self.height // 10,
                         self.height // 10)

        self.paint_text(self.unfocused_text_color)

    def paint_text(self, color: tuple) -> None:
        render = self.font.render(self.text, True, color)
        cent_x = render.get_width() / 2
        cent_y = render.get_height() / 2
        self.screen.blit(render, (self.x - cent_x + self.width / 2,
                                  self.y - cent_y + self.height / 2))
