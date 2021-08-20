from typing import Callable
from button import Button
from pygame import Surface
from pygame.font import SysFont
from screen_template import ScreenTemplate
import cores

font_15 = SysFont('arial', 15, True)
font_45 = SysFont('arial', 45, True, True)

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
        self.screen = screen
        
    def paint(self) -> None:
        '''Method that paints the button and the credits.'''
        self.paint_text()
        return super().paint()
    
    def paint_text(self) -> None:
        '''Method that paints the credits'''
        
        text = 'Game Developer, Programmer and Designer: Doglas Rocha'
        render = font_45.render(text, True, cores.BRANCO)
        # centering in the x axis
        center_x = self.screen.get_width() / 2 - render.get_width() / 2
        # centering in the y axis
        center_y = self.screen.get_height() /2 - render.get_height() / 2
        
        # blitting in the screen
        self.screen.blit(render, (center_x, center_y))