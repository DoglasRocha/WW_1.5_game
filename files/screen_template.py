from abc import ABCMeta, abstractmethod
from typing import Callable
from pygame import Surface
from pygame.event import Event
from game_element import GameElement


class ScreenTemplate(GameElement, metaclass=ABCMeta):


    @abstractmethod
    def __init__(self, action: Callable, screen: Surface) -> None:
        pass
        
    def calculate_rules(self, mouse_positon: tuple):
        for button in self.buttons:
            button.calculate_rules(mouse_positon)
            
    def process_events(self, events: Event, mouse: tuple):
        for button in self.buttons:
            button.process_events(events, mouse)
            
    def paint(self):
        for button in self.buttons:
            button.paint()