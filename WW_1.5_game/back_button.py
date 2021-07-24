from button import Button
from typing import Callable
from pygame import Surface
from pygame.font import Font
from pygame.event import Event

class BackButton(Button):
    
    
    def __init__(self, x: int, y: int, width: int, height: int,
                 state_changer: Callable, new_state: str,
                 save_pontuation_method: Callable,
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
        self.save_pontuation_method = save_pontuation_method
        self.screen = screen
        self.text = text
        self.unfocused_border_color = unfocused_border_color
        self.unfocused_text_color = unfocused_text_color
        self.focused_button_color = focused_button_color
        self.focused_text_color = focused_text_color
        self.font = font
        self.state = 'NOT FOCUSED'
        
    def process_events(self, event: Event, mouse: tuple) -> None:
        mouse_buttons_pressed = mouse[0]
        mouse_position = mouse[1]

        if self.has_click_inside_the_button(mouse_position[0],
                                            mouse_position[1],
                                            mouse_buttons_pressed):
            self.save_pontuation_method()
            self.state_changer(self.new_state)