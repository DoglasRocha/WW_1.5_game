from typing import Callable
from pygame import Surface
from matrix import Matrix
from character import Character
from pygame.time import Clock
from score_manager import ScoreManager
from game_element import GameElement
from back_button import BackButton
import cores
from pygame.font import SysFont

font_10 = SysFont('arial', 10, True)


class Playing(GameElement):
    
    
    def __init__(self, screen: Surface, state_changer: Callable) -> None:
        '''Python special method that constructs the class.
        Receives the screen, that is Pygame Surface and the state changer, 
        which is the method that changes the state of the mother class'''
        
        self.state = 'ALIVE'
        self.level = 1
        self.matrix_object = Matrix(self.level, screen)
        self.matriz = self.matrix_object.get_matrix()
        self.size = self.matrix_object.get_size()
        self.blocks_in_the_matrix = self.matrix_object.get_number_of_blocks()
        self.walls = self.matrix_object.get_walls()
        self.screen = screen
        self.character = Character(screen)
        self.movables_instantiation()
        self.clock = Clock()
        self.state_changer = state_changer
        self.score_manager = ScoreManager()
        self.define_fps()
        back_button = BackButton(10, 10, 150, 25, self.state_changer,
                                 'MENU PRINCIPAL', self.score_manager.save_score,
                                 self.tela, 'VOLTAR', cores.BRANCO, cores.BRANCO,
                                 cores.BRANCO, cores.PRETO, font_10)
        self.buttons = [back_button]
        self.movables = []
        
    def calculate_rules(self, mouse: tuple) -> None:
        '''Method reponsible for calculating the rules of the game. It calculate the rules
        of the buttons and the game itself.
        
        Receives the buttons pressed in the mouse and the position of the mouse.'''
        
        mouse_pressed, mouse_position = mouse
        
        for button in self.buttons:
            button.calculate_rules(mouse_position)
        
        # calculate the rules of the movables
        if len(self.movables) > 1:
            for movable in self.movables:
                movable.calculate_rules()
                
        # continue implementing the rules calculation base on the "cenario" file
        
    def movables_instantiation(self):
        '''Method that instantiate all the movables that are going to be in the level.'''
        pass
        