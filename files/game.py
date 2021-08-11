import pygame; pygame.init()
import cores
from passing_level import PassingLevel
from dead import Dead
from paused import Paused
from playing import Playing
from score_manager import ScoreManager
from game_element import GameElement
from character import Character
from main_menu import MainMenu


class Game(GameElement):
    
    
    def __init__(self) -> None:
        '''Python special method that constructs the class.
        
        In this case, it creates the screen, instantiaties the playing,
        paused, dead, passing level and menu states'''
        
        self.screen = pygame.display.set_mode((1500, 1000))
        self.character = Character(self.screen)
        self.score_manager = ScoreManager()
        self.playing = Playing(self.screen, self.state_changer, self.character,
                               self.score_manager)
        self.paused = Paused(self.state_changer, self.screen, 
                             self.score_manager.save_score, 
                             self.playing.reset_game)
        self.dead = Dead(self.state_changer, self.screen, 
                             self.score_manager.save_score, 
                             self.playing.reset_game)
        self.passing_level = PassingLevel(self.state_changer, self.screen, 
                             self.score_manager.save_score, 
                             self.playing.reset_game)
        self.menu = MainMenu(self.screen, self.state_changer, self.character)
        self.state = 'MAIN MENU'
        self.states_and_classes = {'PLAYING': self.playing,
                                   'MAIN MENU': self.menu,
                                   'DEAD': self.dead,
                                   'PASSING LEVEL': self.passing_level,
                                   'PAUSED': self.paused}
    
    def calculate_rules(self, mouse: tuple) -> None:
        '''Method that calculate the rules of the game.
        
        Receives a tuple which contains the mouse buttons pressed
        and the mouse position'''
        
        environment = self.states_and_classes[self.state]
        mouse_pressed, mouse_position = mouse
        environment.calculate_rules(mouse_position)
            
    def state_changer(self, new_state: str):
        self.state = new_state
    
    def process_events(self, eventos, teclado, mouse):
        '''Method that process the events of the game.
        
        Receives all the events, the keyboard events and the mouse
        buttons pressed and its position'''
        
        environment = self.states_and_classes[self.state]
        
        for e in eventos:
            if e.type == pygame.QUIT:
                self.score_manager.save_score()
                exit()

            if isinstance(environment, Playing):
                environment.process_events(e, teclado, mouse)
                
            elif e.type == pygame.MOUSEBUTTONDOWN \
                    and isinstance(environment, MainMenu):
                environment.process_events(e, mouse)
                
            elif not isinstance(environment, MainMenu): 
                environment.process_events(e, mouse)
                
    def paint(self):
        '''Method that draws the game in the screen'''
        
        environment = self.states_and_classes[self.state]
        environment.paint()
    
    def run(self) -> None:
        '''Method that runs the game'''
        
        while True:
        
            pygame.display.update()
            
            # captura eventos
            events = pygame.event.get()
            keyboard = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed(), pygame.mouse.get_pos()
                
            # calcula as regras
            self.calculate_rules(mouse)
                
            # pinta
            self.screen.fill(cores.PRETO)
            self.paint()
                
            # processa eventos
            self.process_events(events, keyboard, mouse)
        