from generic_state_screen_template import GenericStateScreenTemplate
from typing import Callable
from pygame import Surface


class Paused(GenericStateScreenTemplate):
    
    
    def __init__(self, action: Callable, screen: Surface) -> None:
        super().__init__(action, screen, 'P A U S A D O')