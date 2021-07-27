from typing import Callable
from button import Button
import pygame
from pygame import Surface
import cores
from screen_template import ScreenTemplate

font_15 = pygame.font.SysFont('arial', 15, True)

class CreditsScreen(ScreenTemplate):
    
    def __init__(self, action: Callable, screen: Surface):
        buttons_width = 150
        buttons_height = 25
        buttons_x = 10
        buttons_initial_y = 10
        back_button = Button(buttons_x, buttons_initial_y, 
                             buttons_width, buttons_height, action,
                             'MENU',
                             screen, 'VOLTAR', cores.BRANCO, 
                             cores.BRANCO, cores.BRANCO, cores.PRETO,
                             font_15)
        self.buttons = [back_button]
        