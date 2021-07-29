from weapon_selector_screen import WeaponSelectorScreen
from credits_screen import CreditsScreen
from main_menu_screen import MainMenuScreen
from pygame import QUIT, Surface
from pygame.event import Event
from guns import Weapon


class MainMenu:
    
    def __init__(self, screen: Surface):
        self.state = 'MENU'
        self.main_menu_screen = MainMenuScreen(self.change_state, screen)
        self.credits_screen = CreditsScreen(self.change_state, screen)
        self.weapon_selector_screen = WeaponSelectorScreen(self.change_state, 
                                                           screen, 
                                                           self.gun_receiver)
        self.gun = None
        self.screen_selector_by_state = {'MENU': self.main_menu_screen,
                                         'WEAPON SELECTOR': self.weapon_selector_screen,
                                         'CREDITS': self.credits_screen,
                                         'EXITING': exit}
        
    '''PAINTING'''
    def paint(self) -> None:
        painting = self.screen_selector_by_state[self.state]
        if painting != exit: 
            painting.paint()
        
    '''EVENT PROCESSOR'''    
    def process_events(self, evento: Event, mouse: tuple) -> None:
        event_processor = self.screen_selector_by_state[self.state]
        
        if evento.type == QUIT or event_processor == exit:
            exit()
        else:
            event_processor.process_events(evento, mouse)
            
    '''RULES CALCULATOR'''
    def calculate_rules(self, mouse: tuple):
        _, mouse_position = mouse
        
        ruler = self.screen_selector_by_state[self.state]
        
        if ruler != exit:
            ruler.calculate_rules(mouse_position)
        else:
            ruler()
        
    '''AUXILIARY METHODS'''
    def allowed_to_play(self) -> None:
        return self.state == 'PLAYING'
            
    def gun_receiver(self, gun: Weapon) -> None:
        self.gun = gun
            
    def reset(self) -> None:
        self.state = 'MENU'
        
    def change_state(self, new_state: str) -> None:
        self.state = new_state

    def get_gun(self) -> None:
        return self.gun
    