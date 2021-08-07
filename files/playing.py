from files.bullet import Bullet
from files.movable import Movable
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
        self.matrix = self.matrix_object.get_matrix()
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
        for movable in self.movables:
            
            # calculating the rules of all movables
            if len(self.movables) > 1:
                movable.calculate_rules()
                
            # special conditions to alive movables
            if movable.state == 'ALIVE':
                
                # checking if any bullet collided with a movable of a wall
                for bullet in movable.weapon.fired_bullets:
                    self.bullet_collided_with_movable(movable, bullet)
                    self.bullet_collided_with_wall(movable, bullet)
                    
                # checking if the movable is in a "trap"
                movable_column = self.matrix[movable.line][movable.column]
                if movable_column in (6, 7, 8, 12): # places where the movable receives damage
                    self.movable_take_damage(movable, movable_column)
                
                # checking if the movable is in a ammo point
                elif movable_column == 10:
                    movable.receive_ammo(50)
                    self.matrix_object.clear_ammo(movable.line,
                                                  movable.column)
                
                # checking if the movable is in a hp point
                elif movable_column == 11:
                    movable.gain_hp(50)
                    self.matrix_object.clear_health_kit(movable.line,
                                                        movable.column)
                    
                # now, check if the movable collides with a wall or another movable
                    
    def movable_take_damage(self, movable: Movable, 
                            movable_column: int) -> None:
        '''Method that damages the movable based on which "trap" it is'''
        damages_and_times = {6: (5, 5),
                                     7: (10, 5),
                                     8: (4, 2),
                                    12: (3, 2)}
                        
        damage_and_time = damages_and_times[movable_column]
        movable.take_damage_from_environment(damage_and_time)
                    
    def bullet_collided_with_movable(self, movable: Movable, 
                                     bullet: Bullet) -> None:
        '''Method that checks if the bullet collided with a movable'''
        
        for other_movable in self.movables:
            if movable != other_movable:
                other_movable.analyse_shot(bullet, movable)
                    
    def bullet_collided_with_wall(self, movable: Movable,
                                  bullet: Bullet) -> None:
        '''Method that checks if the bullet collided with a wall'''
        
        for line, column in bullet.hitbox:
            if self.matrix[line][column] in self.walls:
                movable.weapon.fired_bullets.remove(bullet)
                del bullet
        
        
    def movables_instantiation(self):
        '''Method that instantiate all the movables that are going to be in the level.'''
        pass
        