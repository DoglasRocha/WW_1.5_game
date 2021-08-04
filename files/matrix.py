from math import sqrt
from random import choice
from pygame import Surface

# 0 = grama
# 1 = caminho
# 2 = parede limite do cenário
# 3 = caminhozinho de pedra
# 4 = cerca alta
# 5 = muro spawn
# 6 = barro pesado
# 7 = barro leve
# 8 = arame farpado
# 9 = muro ruim
# 10 = municao
# 11 = vida
# 12 = trincheira

caminho_aleatorio = [[0,3,3,0,0],
                     [0,3,0,3,0],
                     [0,0,3,3,3],
                     [0,3,0,3,3],
                     [3,0,3,3,3]] #

trincheira = [[0,0,0,0,0],
              [0,0,0,0,0],
              [12,12,12,12,12],
              [0,0,0,0,12],
              [0,0,0,0,12]] #

arame_farpado = [[0,0,0,0,0],
                 [0,0,0,0,0],
                 [8,8,8,8,8],
                 [0,0,0,0,0],
                 [0,0,0,0,0]] #

estrada = [[0,1,1,1,0],
           [1,1,1,1,1],
           [1,1,1,1,1],
           [1,1,1,1,1],
           [0,1,1,1,0]] #

local_que_recupera_vida = [[0,0,0,4,0],
                           [0,9,0,4,0],
                           [0,9,11,9,0],
                           [0,9,0,4,0],
                           [0,9,0,0,0]] #

local_que_recupera_municao = [[0,9,0,0,0],
                              [0,9,0,4,0],
                              [0,4,10,9,0],
                              [0,9,0,9,0],
                              [0,0,0,9,0]] #

parede_pura = [2,2,2,2,2] #

caminhozinho = [[0,1,1,0,0],
                [0,0,1,1,0],
                [0,0,1,1,0],
                [4,0,0,1,1],
                [4,4,0,0,1]] #

atoleiro = [[0,0,7,7,0],
            [0,7,7,6,7],
            [7,7,6,6,7],
            [7,6,7,7,0],
            [7,7,7,0,0]]

grama = [[0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0]] #

character_spawn = [[0,0,0,0,0],
                    [0,5,5,5,5],
                    [0,5,0,0,0],
                    [5,5,0,0,0],
                    [0,0,0,0,0]] #

enemies_spawn = [[0,0,0,0,0],
                  [0,0,0,0,0],
                  [0,0,0,0,0],
                  [0,0,0,0,0],
                  [0,0,0,0,0]] #

blocks = [grama for i in range(60)]

for i in range(10):
    blocks.append(caminhozinho)
    
for i in range(5):
    blocks.append(caminho_aleatorio)
    
for i in range(5):
    blocks.append(estrada)

for i in range(4):
    blocks.append(trincheira)
    blocks.append(arame_farpado)
    blocks.append(local_que_recupera_vida)
    blocks.append(local_que_recupera_municao)
    blocks.append(atoleiro)

walls = [2, 4, 5, 9]


class Matrix:
    def __init__(self, level: int, screen: Surface) -> None:
        self.lines = self.define_number_of_lines(level)
        self.matrixs_blocks = self.define_number_of_blocks()
        self.number_of_columns = self.define_number_of_columns() 
        self.size = self.define_size(screen)
        self.matrix = self.create_matrix()
        
    def define_number_of_lines(self, level: int) -> int:
        lines = level + 1
        return lines
    
    def define_number_of_blocks(self) -> int:
        numero_blocks = self.lines ** 2
        return numero_blocks
    
    def define_number_of_columns(self) -> int:
        number_of_columns = int((self.lines * 5) + 2)
        return number_of_columns
    
    def define_size(self, screen: Surface) -> int:
        environment_screen_width = screen.get_width() * 0.6
        size = int(environment_screen_width / self.number_of_columns)
        return size
    
    def make_5_lines(self, random_blocks: list) -> list:
        five_lines = []
        begin_and_end_matrix_element = [2]
        for i in range(5):
            line = begin_and_end_matrix_element.copy()
            for random_block in random_blocks:
                line.extend(random_block[i])
            line.extend(begin_and_end_matrix_element)
            five_lines.append(line)
        
        return five_lines
    
    def make_initial_line(self) -> list:
        initial_line = [2 for i in range(self.number_of_columns)]
        return initial_line
        
    def make_end_line(self) -> list:
        end_line = [2 for i in range(self.number_of_columns)]
        return end_line
        
    def create_matrix(self):
        blocks_per_line = int(sqrt(self.matrixs_blocks))
        
        initial_line = self.make_initial_line()
        end_line = self.make_end_line()
        
        matrix = [initial_line]
        
        for i in range(blocks_per_line):
            selected_blocks = []
            
            first_quadrant = (i + 1) ** 2 == 1
            last_quadrant = (i + 1) ** 2 == self.matrixs_blocks
            
            if first_quadrant:
                self.make_first_quadrant(blocks_per_line, selected_blocks)
            elif last_quadrant:
                self.make_last_quadrant(blocks_per_line, selected_blocks)
            else:
                self.make_quadrant(blocks_per_line, selected_blocks)

            line = self.make_5_lines(selected_blocks)
            matrix.extend(line)        
            
        matrix.append(end_line)
        return matrix
    
    def make_first_quadrant(self, blocks_per_line: int, selected_blocks: list) -> None:
        enemies_block = enemies_spawn.copy()
        selected_blocks.append(enemies_block)
        for x in range(1, blocks_per_line):
            selected_blocks.append(choice(blocks))
            
    def make_last_quadrant(self, blocks_per_line: int, selected_blocks: list) -> None:
        for x in range(1, blocks_per_line):
            selected_blocks.append(choice(blocks))
        selected_blocks.append(character_spawn)
        
    def make_quadrant(self, blocks_per_line: int, selected_blocks: list) -> None:
        for x in range(blocks_per_line):
            selected_blocks.append(choice(blocks))
    
    def clear_ammo(self, line:int, column: int) -> None:
        self.matrix[line][column] = 0
        
    def clear_health_kit(self, line:int, column: int) -> None:
        self.matrix[line][column] = 0
    
    def get_matrix(self) -> None:
        return self.matrix
    
    def get_size(self) -> None:
        return self.size
    
    def get_number_of_blocks(self) -> None:
        return self.matrixs_blocks
    
    @staticmethod
    def get_walls():
        return walls