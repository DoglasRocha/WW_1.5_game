from gun_button import GunButton
from guns import AK47, Pistol, SMG, Shotgun, Sniper
from typing import Callable
from button import Button
from pygame import Surface
from screen_template import ScreenTemplate
from pygame.font import SysFont
import cores

font_15 = SysFont('arial', 15, True)

class WeaponSelectorScreen(ScreenTemplate):

    
    def __init__(self, state_changer: Callable, screen: Surface, 
                 gun_receiver: Callable, trigger: Callable):
        buttons_width = 150
        buttons_height = 25
        buttons_x = 10
        buttons_initial_y = 10
        back_button = Button(buttons_x, buttons_initial_y, 
                             buttons_width, buttons_height, state_changer,
                             'MENU',
                             screen, 'VOLTAR', cores.BRANCO, 
                             cores.BRANCO, cores.BRANCO, cores.PRETO,
                             font_15)
        self.buttons = [back_button]
        
        self.gun_button_instanciation(screen, gun_receiver, 
                                      state_changer, trigger)
            
    def gun_button_instanciation(self, screen: Surface,
                                 gun_receiver: Callable,
                                 state_changer: Callable,
                                 trigger: Callable) -> None:
        guns = [Pistol, SMG, AK47, Shotgun, Sniper]
        part_x = screen.get_width() // 4
        part_y = screen.get_height() // 3
        for i in range(1, 4):
            x = part_x * i
            y = part_y
            self.buttons.append(GunButton(x, y, gun_receiver, trigger,
                                          screen, cores.BRANCO,
                                          cores.BRANCO, cores.BRANCO, 
                                          cores.PRETO, guns[i - 1]))
            
        part_x = screen.get_width() // 3
        for i in range(2):
            x = part_x * (i + 1)
            y = part_y * 2
            self.buttons.append(GunButton(x, y, gun_receiver, trigger,
                                          screen, cores.BRANCO,
                                          cores.BRANCO, cores.BRANCO, 
                                          cores.PRETO, guns[i + 3]))