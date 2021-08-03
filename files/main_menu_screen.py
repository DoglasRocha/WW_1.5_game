from typing import Callable
from button import Button
import pygame
from pygame import Surface
import cores
from screen_template import ScreenTemplate

font_50 = pygame.font.SysFont('arial', 50, True)

class MainMenuScreen(ScreenTemplate):
    
    def __init__(self, action: Callable, screen: Surface):
        buttons_width = 500
        buttons_height = 125
        buttons_x = 750 - buttons_width // 2
        buttons_initial_y = 300
        
        play_button = Button(buttons_x, buttons_initial_y, 
                             buttons_width, buttons_height, action,
                             'WEAPON SELECTOR',
                             screen, 'JOGAR', cores.BRANCO, 
                             cores.BRANCO, cores.BRANCO, cores.PRETO,
                             font_50)
        
        buttons_y = buttons_initial_y + buttons_height + 25
        credits_button = Button(buttons_x, buttons_y, 
                          buttons_width, buttons_height, action,
                          'CREDITS',
                          screen, 'CRÉDITOS', cores.BRANCO, 
                          cores.BRANCO, cores.BRANCO, cores.PRETO,
                          font_50)
        
        buttons_y += buttons_height + 25
        exit_button = Button(buttons_x, buttons_y, 
                             buttons_width, buttons_height, action,
                             'EXITING',
                             screen, 'SAIR', cores.BRANCO, 
                             cores.BRANCO, cores.BRANCO, cores.PRETO,
                             font_50)
        
        self.buttons = [play_button, credits_button, exit_button]
        