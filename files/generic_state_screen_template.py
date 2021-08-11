from back_button import BackButton
from button import Button
from screen_template import ScreenTemplate
from pygame.font import SysFont
from pygame import Surface
from typing import Callable
import cores


font_25 = SysFont('arial', 25, True)
font_50 = SysFont('arial', 50, True)

class GenericStateScreenTemplate(ScreenTemplate):
    
    
    def __init__(self, action: Callable, screen: Surface,
                 text: str, save_pontuation: Callable,
                 game_reseter: Callable) -> None:
        '''Special python method that constructs the class.
        
        Receives the state changer and the screen Surface'''
        
        # calculating the x and y position
        buttons_width = 350
        buttons_height = 100
        x = screen.get_width() // 2 - buttons_width // 2
        initial_y = screen.get_height() // 2
        second_y = initial_y + buttons_height + 20
        
        # instantiating the continue button
        continue_button = Button(x, initial_y, buttons_width, buttons_height,
                             action, 'PLAYING', screen, 'CONTINUAR',
                             cores.BRANCO, cores.BRANCO, cores.BRANCO,
                             cores.PRETO, font_25)
        
        # instantiating the back button
        back_button = BackButton(x, second_y, buttons_width,
                                 buttons_height, action, 'MAIN MENU',
                                 save_pontuation, game_reseter, screen, 'MENU', cores.BRANCO,
                                 cores.BRANCO, cores.BRANCO, cores.PRETO,
                                 font_25)
        
        self.buttons = [back_button, continue_button]
        
        # instantiating the render of the text
        self.text = font_50.render(text, True, cores.BRANCO)
        text_x = screen.get_width() // 2 - self.text.get_width() // 2
        text_y = screen.get_height() // 4 - self.text.get_height() // 2
        self.text_position = (text_x, text_y)
        self.screen = screen
        
    def paint(self):
        '''Method that paints the text and the buttons'''
        
        # painting the text
        self.screen.blit(self.text, self.text_position)
        super().paint()
        