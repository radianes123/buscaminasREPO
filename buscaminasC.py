import numpy as np
import pygame, random, sys

class bomb:
    def __init__(self,col,row):
        self.posx=col
        self.posy=row

    def __repr__(self):
        return f'Bomba en c:{self.col} r:{self.row}'
    
class field:
    def __init__(self,cols,rows):
        self.cols=cols
        self.rows=rows
        self.gameField=np.zeros((rows,cols)) # Crear matriz de juego
        self.playField=np.zeros((rows,cols)) # Crear matriz de jugadas

    def generateField(self,bombs):
        for i in range(bombs-1):
            excluded=[] # Elementos excluídos para que no se repitan
            if i==0:
                excluded.append(ra.randint(0,self.rows-1),ra.randint(0,self.cols-1))
            else:
                for j in excluded:
                    if excluded
        
