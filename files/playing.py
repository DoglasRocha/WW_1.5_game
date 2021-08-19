from image_loader import ImageLoader
from enemies import Captain, Enemy, General, Recruit, Soldier
from bullet import Bullet
from movable import Movable
from typing import Callable
from pygame import Surface
from matrix import Matrix
from character import Character
from pygame.time import Clock
from score_manager import ScoreManager
from game_element import GameElement
from button import Button
from pygame.font import SysFont, Font
from pygame.event import Event
import pygame
import cores

font_15 = SysFont('arial', 15, True)
font_20 = SysFont('arial', 20, True)


class Playing(GameElement):
    
    
    def __init__(self, screen: Surface, state_changer: Callable,
                 character: Character, score_manager: ScoreManager) -> None:
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
        self.character = character
        self.movables = [self.character]
        self.movables_instantiation()
        self.clock = Clock()
        self.state_changer = state_changer
        self.score_manager = score_manager
        self.define_fps()
        self.images = ImageLoader.load_scenary()
        back_button = Button(10, 10, 150, 25, self.state_changer,
                                 'PAUSED', self.screen, 'PAUSAR',
                                 cores.BRANCO, cores.BRANCO,
                                 cores.BRANCO, cores.PRETO, font_15)
        self.buttons = [back_button]
        
    '''----------------------CALCULATING THE RULES----------------------'''
        
    def calculate_rules(self, mouse_position: tuple) -> None:
        '''Method reponsible for calculating the rules of the game. It calculate the rules
        of the buttons and the game itself.
        
        Receives the buttons pressed in the mouse and the position of the mouse.'''
        
        for button in self.buttons:
            button.calculate_rules(mouse_position)
            
        # if the character dies, the level has to be reinited
        if self.state == 'DEAD':
            self.reinit_level()
            self.state_changer('DEAD')
            
        if len(self.movables) > 1:
            
            # calculate the rules of the movables
            for movable in self.movables:
                # calculating the rules of all movables
                movable.calculate_rules()
                    
                # special actions to alive movables
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
                        
                    # checking if the movable collides with a wall or another movable
                    # and doing the respective actions
                    if self.collides_with_anything(movable):
                        # if the movable is an enemy, it has to receive a list
                        # with the possible directions to take
                        if isinstance(movable, Enemy):
                            possible_directions = self.get_directions(movable.line, movable.column)
                            movable.refuse_movement(possible_directions)
                            
                        # if the movable is the character, it just refuses the movement
                        else: 
                            movable.refuse_movement()
                            
                    # if does not collide with anything, accepts the movement
                    else:
                        movable.accept_movement()
                        
                # special actions if the movable is dead
                elif movable.state == 'DEAD':
                    
                    # if the movable is an enemy, it has to be removed 
                    # from the list of movables, add his reward to the
                    # score and get deleted from the memory
                    if isinstance(movable, Enemy):
                        self.movables.remove(movable)
                        self.score_manager.add_points(movable.reward)
                        del movable
                        
                    # if the character is dead, the game has to be reinited    
                    elif isinstance(movable, Character):
                        self.state = 'DEAD'
        # if the length of the movables list is equal to one and the 
        # character still alive, the level has to be past
        else:
            # passing the level
            self.pass_level()
            # changing the state of the game manager
            self.state_changer('PASSING LEVEL')
                    
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
                
    def movable_collides_with_wall(self, movable: Movable) -> bool:
        '''Method that checks if the movable, in any point of its hitbox, hits
        a wall. If, in any point, it hits a wall, the method returns True.'''
        
        directions_that_can_move = []
        
        for line, column in movable.hitbox:
            collides = self.matrix[line][column] in self.walls
            directions_that_can_move.append(collides)
            
        return any(directions_that_can_move)
    
    def movable_collides_with_movable(self, movable: Movable) -> bool:
        '''Method that checks if the movable, in any point of its
        hitbox, hits another movable. If collides, the method returns
        True'''
        
        if isinstance(movable, Character):
        
            collides_with_movable = []
            
            for new_line, new_colunm in movable.hitbox:
                # taking the other movables
                for another_movable in self.movables:  
                    # checking if the other movable is not the movable
                    # analised and is not an enemy (enemies don't collide 
                    # with each other)  
                    if id(movable) != id(another_movable) \
                            and isinstance(movable, Enemy):
                        collides = another_movable.line == new_line \
                                and another_movable.column == new_colunm
                        collides_with_movable.append(collides)
                        
            return any(collides_with_movable)
        return False
                        
    def collides_with_anything(self, movable: Movable) -> bool:
        '''Method that checks if the movable collides with another
        movable or a wall'''
        
        return self.movable_collides_with_movable(movable) \
               or self.movable_collides_with_wall(movable)
               
    def get_directions(self, line: int, column: int) -> list:
        '''Method that returns the possible directions to a movable take.'''
        
        directions = []
        
        if self.matrix[int(line - 1)][int(column)] not in self.walls:
            directions.append('NORTH')
            
        if self.matrix[int(line + 1)][int(column)] not in self.walls:
            directions.append('SOUTH')
            
        if self.matrix[int(line)][int(column - 1)] not in self.walls:
            directions.append('WEST')
            
        if self.matrix[int(line)][int(column + 1)] not in self.walls:
            directions.append('EAST')
            
        if self.matrix[int(line - 1)][int(column + 1)] not in self.walls:
            directions.append('NORTH EAST')
            
        if self.matrix[int(line - 1)][int(column - 1)] not in self.walls:
            directions.append('NORTH WEST')
            
        if self.matrix[int(line + 1)][int(column + 1)] not in self.walls:
            directions.append('SOUTH EAST')
            
        if self.matrix[int(line + 1)][int(column - 1)] not in self.walls:
            directions.append('SOUTH WEST')
            
        return directions
        
    def movables_instantiation(self):
        '''Method that instantiate all the movables that are going to
        be in the level.'''
        
        self.movables = [self.character]
        
        # the number of recruits in the level is equal to the level number
        for i in range(int(self.level)):
            self.movables.append(Recruit(self.screen, self.character))
            
        # the number of soldiers in the level is equal to half the level number
        for i in range(int(self.level * 0.5)):
            self.movables.append(Soldier(self.screen, self.character))
            
        # the number of capitains in the level is equal to quarter of the level number
        for i in range(int(self.level * 0.2)):
            self.movables.append(Captain(self.screen, self.character))
            
        # the number of generals in the level is equal to the level number divided by 10
        for i in range(int(self.level * 0.1)):
            self.movables.append(General(self.screen, self.character))
            
        # defining the position and the size of the movables
        for movable in self.movables:
            if isinstance(movable, Character):
                # instantiating the enemies in the first position of the matrix
                movable.define_geometric_stats(len(self.matrix[0]) - 2, 
                                               len(self.matrix[0]) - 2, 
                                               self.size)
                
            else:
                movable.define_geometric_stats(1, 1, self.size)


    '''----------------------PROCESSING THE EVENTS----------------------'''
    
    def process_events(self, event: Event, keyboard: tuple, 
                       mouse: tuple) -> None:
        '''Method that process the events (keydown, mouse button down, etc)
        
        Receives a event, the keyboard tuple (that contains the keys pressed)
        and the mouse tuple, that contains the mouse position and the mouse
        buttons that are being pressed'''
        
        # process the events in the button
        for button in self.buttons:
            button.process_events(event, mouse)
        
        # checking if the player wants to pause the game
        is_a_key_pressed = event.type == pygame.KEYDOWN
        if is_a_key_pressed:
            key = event.key
            
            esc = pygame.K_ESCAPE
            
            if key == esc:
                self.state_changer('PAUSED')
                
        # calculating the rules of the movables
        for movable in self.movables:
            # if the movable is the Character, it has to receive the
            # event, the keyboard and the mouse 
            if isinstance(movable, Character):
                movable.process_events(event, keyboard, mouse)
            
            else:
                movable.process_events()
            
        
    '''----------------------PAINTING----------------------'''
    
    def paint(self) -> None:
        '''Method that paints the scenary in the screen. It access the matrix
        and paints according to the information contained in the matrix,
        paint the movables, the side bar and the buttons'''
        
        # paint the scenary
        for line_number, line in enumerate(self.matrix):
            self.paint_line(line_number, line)
        # paint the side bar
        self.paint_side_bar()
        # paint the movables
        for movable in self.movables:
            movable.paint()
        # paint the buttons
        for button in self.buttons:
            button.paint()
            
    def paint_text(self, text: str, x: int, y: int, fonte: Font,
                   color: tuple) -> None:
        '''Method that paint a text in a centered position'''
        
        render = fonte.render(text, True, color)
        cent_x = render.get_width() / 2
        cent_y = render.get_height() / 2
        self.screen.blit(render, (x - cent_x, y - cent_y))
    
    def paint_line(self, line_number: int, line: list) -> None:
        '''Paint the a line of 5 height units (5 squares) and all 
        the width of the scenary. It is generated randomly in lines,
        so, it is painted in lines.'''
        
        # accessing the scenary itself
        for column_number, column in enumerate(line):
            # determinating the positon of the squares
            x = column_number * self.size + (self.screen.get_width() // 5)
            y = line_number * self.size
            
            # process to know the color of the square
            all_colors = {0: self.images['grass'], 1: self.images['path'], 
                          2: self.images['scenary_limit'], 3: self.images['stone_path'], 
                          4: self.images['high_fence'], 5: self.images['spawn_wall'],
                          6: self.images['heavy_mud'], 7: self.images['light_mud'], 
                          8: cores.PRATA,
                          9: cores.LARANJA_FEIO, 10: cores.AZUL_ACO, 11: cores.VERMELHO,
                          12: cores.MARROM_FEIO}
            
            color = all_colors[column]
            
            if type(color) != tuple:
                image = pygame.transform.scale(color, (self.size, self.size))
                self.screen.blit(image, (x, y))
            else:
                # painting the square
                pygame.draw.rect(self.screen, color, (x, y, self.size, self.size))
            
    def paint_side_bar(self) -> None:
        '''Method that paints the side bar, which contains the pontuation,
        the ammo remaining, the HP and the previous pontuation records'''
        
        self.paint_score()
        self.paint_records()
        
    def paint_score(self) -> None:
        '''Paint the general score (earned in the previous levels), the score
        earned in the current level, the level and the current attempt'''
        
        general_score = f'Pontuação Geral: {round(self.score_manager.get_general_score(), 2)}'
        level = f'Nível: {self.level}'
        level_pontuation = f'Pontuação no Nível: {round(self.score_manager.get_level_score(), 2)}'
        attempt = f'Tentativa nº: {self.score_manager.get_attempt()}'
        
        # calculating the position in the x axis
        x = self.screen.get_width() - (self.screen.get_width() // 10)
        
        # calculating the initial position in the y axis
        y = self.screen.get_height() // 40
        
        # calculating the increment to the y axis
        y_increment = self.screen.get_height() // 20
        
        self.paint_text(general_score, x, y, font_20, cores.BRANCO)
        y += y_increment
        
        self.paint_text(level, x, y, font_20, cores.BRANCO)
        y += y_increment
        
        self.paint_text(level_pontuation, x, y, font_20, cores.BRANCO)
        y += y_increment
        
        self.paint_text(attempt, x, y, font_20, cores.BRANCO)
    
    def paint_records(self) -> None:
        '''Method that paint the 5 biggest scores.'''
        
        # calculating the position in the x axis and the y axis initial positon 
        x = self.screen.get_width() - (self.screen.get_width() // 10)
        y = self.screen.get_height() // 2.5
        
        # painting the title
        title = 'RECORDES DE PONTUAÇÃO'
        self.paint_text(title, x, y, font_20, cores.BRANCO)
        
        # getting the five biggest scores from the score manager
        five_biggest_scores = self.score_manager.get_five_biggest_scores()
        
        # painting the records
        position_y = y + y // 10
        for key, value in five_biggest_scores.items():
            date = key
            text = f'{date} ... {value:5.2f} pontos'
            
            self.paint_text(text, 1350, position_y, font_15, cores.BRANCO)
            position_y += y // 20
            
    '''----------------------LEVEL LOGIC----------------------'''
    
    def init_level(self) -> None:
        '''Method that execut all the methods needed to
        init the level'''
        
        self.character.reinit_stats()
        self.matrix_object = Matrix(self.level, self.screen)
        self.matrix = self.matrix_object.get_matrix()
        self.size = self.matrix_object.get_size()
        self.blocks_in_the_matrix = self.matrix_object.get_number_of_blocks()
        self.movables_instantiation()
        self.define_fps()
        self.state = 'PLAYING'
        
    def pass_level(self) -> None:
        '''Method used when the Character kills all the enemies'''
        
        self.level += 1
        self.score_manager.to_next_level()
        self.init_level()
        
    def reinit_level(self) -> None:
        '''Method used when the Character dies'''
        
        self.score_manager.re_init_level()
        self.init_level()
        
    def reset_game(self) -> None:
        '''Method used when the player goes to the menu'''
        self.level = 1
        self.reinit_level()
        
    def define_fps(self) -> None:
        '''Method that defines the fps (and ultimatelly, the speed
        of the game'''
        
        fps = 2420 // self.blocks_in_the_matrix
        self.clock.tick(fps)