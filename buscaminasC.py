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
        
class Menu:
    def __init__(self,screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Visitor TT1 BRK", 30)
        self.buttons = [
            {"text": "Fácil", "rect": pygame.Rect(100,50,200,80), "action": self.start_easy_game}
            {"text": "Intermedio", "rect": pygame.Rect(100,150,200,80), "action": self.start_medium_game}
            {"text": "Difícil", "rect": pygame.Rect(100,250,200,80), "action": self.start_hard_game}
            {"text": "Salir", "rect": pygame.Rect(100,350,200,80), "action": self.quit_game}
        ]

    def start_easy_game(self):
        Game(self.screen, "Fácil").run()

    def start_medium_game(self):
        Game(self.screen, "Intermedio").run()

    def start_hard_game(self):
        Game(self.screen, "Difícil").run()

    def quit_game(self):
        pygame.quit()
        sys.exit()
