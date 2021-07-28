from math import sqrt
from random import choice

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

spawn_personagem = [[0,0,0,0,0],
                    [0,5,5,5,5],
                    [0,5,0,0,0],
                    [5,5,0,0,0],
                    [0,0,0,0,0]] #

spawn_inimigos = [[0,0,0,0,0],
                  [0,0,0,0,0],
                  [0,0,0,0,0],
                  [0,0,0,0,0],
                  [0,0,0,0,0]] #

blocos = [grama for i in range(60)]

for i in range(10):
    blocos.append(caminhozinho)
    
for i in range(5):
    blocos.append(caminho_aleatorio)
    
for i in range(5):
    blocos.append(estrada)

for i in range(4):
    blocos.append(trincheira)
    blocos.append(arame_farpado)
    blocos.append(local_que_recupera_vida)
    blocos.append(local_que_recupera_municao)
    blocos.append(atoleiro)

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

paredes = [2, 4, 5, 9]


class Matriz:
    def __init__(self, nivel):
        self.linhas = self.define_numero_linhas(nivel)
        self.blocos_na_matriz = self.define_numero_blocos()
        self.numero_colunas = self.define_numero_colunas() 
        self.tamanho = self.define_tamanho()
        self.matriz = self.cria_matriz()
        
    def define_numero_linhas(self, nivel):
        linhas = nivel + 1
        return linhas
    
    def define_numero_blocos(self):
        numero_blocos = self.linhas ** 2
        return numero_blocos
    
    def define_numero_colunas(self):
        numero_colunas = int((self.linhas * 5) + 2)
        return numero_colunas
    
    def define_tamanho(self):
        tamanho = int(900 / self.numero_colunas)
        return tamanho
    
    def faz_5_linhas(self, blocos_aleatorios):
        cinco_linhas = []
        comeco_e_fim_matriz = [2]
        for i in range(5):
            linha = comeco_e_fim_matriz.copy()
            for bloco_aleatorio in blocos_aleatorios:
                linha.extend(bloco_aleatorio[i])
            linha.extend(comeco_e_fim_matriz)
            cinco_linhas.append(linha)
        
        return cinco_linhas
    
    def faz_linha_inicial(self):
        linha_inicial = [2 for i in range(self.numero_colunas)]
        return linha_inicial
        
    def faz_linha_final(self):
        linha_final = [2 for i in range(self.numero_colunas)]
        return linha_final
        
    def cria_matriz(self):
        blocos_por_linha = int(sqrt(self.blocos_na_matriz))
        
        linha_inicial = self.faz_linha_inicial()
        linha_final = self.faz_linha_final()
        
        matriz = [linha_inicial]
        
        for i in range(blocos_por_linha):
            blocos_selecionados = []
            
            primeiro_quadrante = (i + 1) ** 2 == 1
            ultimo_quadrante = (i + 1) ** 2 == self.blocos_na_matriz
            
            if primeiro_quadrante or ultimo_quadrante:
                if primeiro_quadrante:
                    bloco_inimigos = spawn_inimigos.copy()
                    blocos_selecionados.append(bloco_inimigos)
                    for x in range(1, blocos_por_linha):
                        blocos_selecionados.append(choice(blocos))    
                elif ultimo_quadrante:
                    for x in range(1, blocos_por_linha):
                        blocos_selecionados.append(choice(blocos))
                    blocos_selecionados.append(spawn_personagem)
            else:
                for x in range(blocos_por_linha):
                    blocos_selecionados.append(choice(blocos))

            linha = self.faz_5_linhas(blocos_selecionados)
            matriz.extend(linha)        
            
        matriz.append(linha_final)
        return matriz
    
    def clear_ammo(self, line:int, column:int):
        self.matriz[line][column] = 0
        
    def clear_health_kit(self, line:int, column:int):
        self.matriz[line][column] = 0
    
    def get_matriz(self):
        return self.matriz
    
    def get_tamanho(self):
        return self.tamanho
    
    def get_numero_blocos(self):
        return self.blocos_na_matriz
    
    @staticmethod
    def get_paredes():
        return paredes