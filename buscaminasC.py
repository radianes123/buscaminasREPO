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
        self.gameField=np.zeros(cols,rows) # Crear matriz de ceros

    def generateField(self):
        
