import numpy as np
import pygame, random, sys


pygame.init()

WHITE = (255,255,255)
BLACK = (0,0,0)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300

font_path = "Grand9k_Pixel.ttf"
font = pygame.font.Font(font_path, 30)

class field:
    def __init__(self,cols,rows):
        self.cols=cols
        self.rows=rows
        self.gameField=np.zeros((rows,cols)) # Crear matriz de juego
    def __repr__(self):
        return f'{self.gameField}'
    def generateField(self,bombs):
        excluded=[] # Lista de elementos excluídos para que no se repitan
        for i in range(bombs):
            if i==0: # Si e3s la primer bomba, se salta el proceso de verificación
                bombpos=[random.randint(0,self.rows-1),random.randint(0,self.cols-1)] # Posición de la bomba
                excluded.append(bombpos) # Excluir dicha posición
                self.gameField[bombpos[0],bombpos[1]]=101 # Colocar la bomba en la matriz de juego
            else:
                k=0
                while True:
                    fail=0
                    bombpos=[random.randint(0,self.rows-1),random.randint(0,self.cols-1)]
                    for j in range(len(excluded)):
                        if bombpos[0]==excluded[j][0] and bombpos[1]==excluded[j][1]:
                            fail+=1
                    if fail==0:
                        excluded.append(bombpos)
                        self.gameField[bombpos[0],bombpos[1]]=101
                        break
    def detectBomb(self,row,col):
        if self.gameField[row,col]==101:
            return "b"
        else:
            bombs=0
            for i in range(-1,2,1):
                for j in range(-1,2,1):
                    if col+j>=0 and col+j<=self.cols and row+i>=0 and row+i<=self.rows:
                        if self.gameField[row+i,col+j]==101:
                            bombs+=1
            return bombs
       

class Menu:
    def __init__(self,screen):
        self.screen = screen
        self.font = font
        self.buttons = [
            {"text": "Fácil", "rect": pygame.Rect(100,65,200,30), "action": self.start_easy_game},
            {"text": "Intermedio", "rect": pygame.Rect(100,125,200,30), "action": self.start_medium_game},
            {"text": "Difícil", "rect": pygame.Rect(100,185,200,30), "action": self.start_hard_game},
            {"text": "Salir", "rect": pygame.Rect(100,245,200,30), "action": self.quit_game}
        ]

    def draw(self):
        self.screen.fill(BLACK)
        title = self.font.render("BUSCAMINAS", True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 10))

        for button in self.buttons:
            pygame.draw.rect(self.screen, BLACK, button["rect"])
            label = self.font.render(button["text"], True, WHITE)
            self.screen.blit(label, (button["rect"].x + button["rect"].width // 2 - label.get_width() // 2,
                                     button["rect"].y + button["rect"].height // 2 - label.get_height() // 2))

    def event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button["rect"].collidepoint(mouse_pos):
                    button["action"]()
                    
    def start_easy_game(self):
        Game(self.screen, "Fácil").run()

    def start_medium_game(self):
        Game(self.screen, "Intermedio").run()

    def start_hard_game(self):
        Game(self.screen, "Difícil").run()

    def quit_game(self):
        pygame.quit()
        sys.exit()

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Buscaminas")
    
    menu = Menu(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            menu.event(event)
    
        menu.draw()
        pygame.display.flip()

if __name__ == "__main__":
    main()
