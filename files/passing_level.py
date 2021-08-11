from generic_state_screen_template import GenericStateScreenTemplate
from typing import Callable
from pygame import Surface


class PassingLevel(GenericStateScreenTemplate):
    
    
    def __init__(self, action: Callable, screen: Surface,
                 save_pontuation: Callable, 
                 game_reseter: Callable) -> None:
        super().__init__(action, screen, 'VOCÊ PASSOU DE NÍVEL!!!',
                         save_pontuation, game_reseter)