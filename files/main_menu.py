from character import Character
from typing import Callable
from weapon_selector_screen import WeaponSelectorScreen
from credits_screen import CreditsScreen
from main_menu_screen import MainMenuScreen
from pygame import QUIT, Surface
from pygame.event import Event
from guns import Weapon


class MainMenu:
    
    def __init__(self, screen: Surface, game_state_changer: Callable,
                 character: Character):
        self.state = 'MENU'
        self.main_menu_screen = MainMenuScreen(self.change_state, screen)
        self.credits_screen = CreditsScreen(self.change_state, screen)
        self.weapon_selector_screen = WeaponSelectorScreen(self.change_state, 
                                                           screen, 
                                                           self.gun_receiver,
                                                           self.trigger)
        self.gun = None
        self.game_state_changer = game_state_changer
        self.character = character
        self.screen_selector_by_state = {'MENU': self.main_menu_screen,
                                         'WEAPON SELECTOR': self.weapon_selector_screen,
                                         'CREDITS': self.credits_screen,
                                         'EXITING': exit}
        
    '''PAINTING'''
    def paint(self) -> None:
        if self.state != 'PLAYING':
            painting = self.screen_selector_by_state[self.state]
            if painting != exit: 
                painting.paint()
        
    '''EVENT PROCESSOR'''    
    def process_events(self, evento: Event, mouse: tuple) -> None:
        
        if self.state != 'PLAYING':
            event_processor = self.screen_selector_by_state[self.state]
            if evento.type == QUIT or event_processor == exit:
                exit()
            else:
                event_processor.process_events(evento, mouse)
            
    '''RULES CALCULATOR'''
    def calculate_rules(self, mouse_position: tuple):
        if self.state != 'PLAYING' and self.state != 'PLAYING':
            ruler = self.screen_selector_by_state[self.state]
            
            if ruler != exit:
                ruler.calculate_rules(mouse_position)
                    
            elif ruler == exit:
                ruler()
        
    '''AUXILIARY METHODS'''
            
    def gun_receiver(self, gun: Weapon) -> None:
        self.gun = gun
            
    def reset(self) -> None:
        self.state = 'MENU'
        
    def change_state(self, new_state: str) -> None:
        self.state = new_state

    def trigger(self) -> None:
        '''Method that triggers the game to init'''
        self.character.receive_weapon(self.gun)
        self.reset()
        self.game_state_changer('PLAYING')