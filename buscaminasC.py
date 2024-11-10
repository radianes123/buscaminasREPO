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
    def __init__(self,cols,rows,bombs):
        self.cols=cols
        self.rows=rows
        self.bombField=np.zeros((rows,cols)) # Crear matriz de juego
        self.playingField=np.zeros((rows,cols)) # Crea una matriz en la cual se guardarán las jugada hechas por que jugador
        self.bombs=bombs
        self.flags=bombs
        self.flaggedBombs=0
    def __repr__(self):
        return f'Campo de bombas:\n{self.bombField}\nCampo de jugadas\n{self.playingField}'
    def generateField(self):
        excluded=[] # Lista de elementos excluídos para que no se repitan
        for i in range(self.bombs):
            if i==0: # Si e3s la primer bomba, se salta el proceso de verificación
                bombpos=[random.randint(0,self.rows-1),random.randint(0,self.cols-1)] # Posición de la bomba
                excluded.append(bombpos) # Excluir dicha posición
                self.bombField[bombpos[0],bombpos[1]]=101 # Colocar la bomba en la matriz de juego
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
                        self.bombField[bombpos[0],bombpos[1]]=101
                        break
    def detectBomb(self,row,col):
        """
        Detecta bombas cercanas en un cuadrado 3x3, con centro en la celda seleccionada, devuelve
        dicho número de bombas.
        """
        bombs=0
        for i in range(-1,2,1):
            for j in range(-1,2,1):
                if col+j>=0 and col+j<=self.cols and row+i>=0 and row+i<=self.rows:
                    if self.bombField[row+i,col+j]==101:
                        bombs+=1
        return bombs
    def getFlags(self):
        flags=self.flags
        return flags
    def checkFlagged(self):
        """
        Revisa las bombas acertadas, devuelve la cantidad de estas.
        """
        flaggedBombs=0
        for i in range(0,self.rows-1):
            for j in range(0,self.cols-1):
                if((self.bombField[i,j]==101) and (self.playingField[i,j]==2)):
                    flaggedBombs+=1
        return flaggedBombs

    def cellAction(self,row,col,action):
        """
        Devuelve dos valores, el primero es el <comando> y el segundo es para traspasar valores cuando se necesite.
        <action> es lo que se hace con la celda, dependiendo de si se quiere despejar o añadir una bandera.
        """
        if self.playingField[row,col]!=1: # Verificar si la celda no se despejó antes
            if action=="clear":
                if self.playingField[row,col]!=2: # Revisa si la celda no está <<Bandereada>>
                    if self.bombField[row,col]==101:
                        return "lose",0 # Esto ejectuará una función de derrota
                    else:
                        self.playingField[row,col]=1
                        bombs=self.detectBomb(row,col)
                        return "cell.clear",bombs # Ejecutará una función que graficará el número de bombas cerca de la celda
                return "none",0
            elif action=="flag":
                i=-1 # Es el índice de <orders>
                orders=["cell.flag.add","cell.flag.remove"]
                if self.playingField[row,col]==0 and self.flags>0: 
                    self.playingField[row,col]=2
                    self.flags-=1
                    i+=1
                elif self.playingField[row,col]==2 and self.flags<self.bombs:
                    self.playingField[row,col]=0
                    self.flags+=1
                    i+=2
                if((self.playingField[row,col]==0 and self.flags>0) or (self.playingField[row,col]==2 and self.flags<self.bombs)):  
                    n=self.checkFlagged()
                    if n==self.bombs:
                        return "win",0 # Si el número de banderas acertadas es igual al número de bombas, se termina el juego
                    else:
                        return orders[i],0
                        # Para "cell.flag.add", ejectuará una función que dibuje una bandera
                        # Para "cell.flag.remove", ejecutará una función que borre gráficamente la bandera previamente puesta
                return "none",0
        else:
            return "none",0



class Game:
    def __init__(self, screen, cols, rows, bombs):
        self.screen = screen
        self.field = field(cols,rows,bombs)
        self.cols = cols
        self.rows = rows
        self.bombs = bombs

    def run(self):
        gameover=False
        while gameover==False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x,y=pygame.mouse.get_pos()
                    col,row =x//(SCREEN_WIDTH//self.cols), y//(SCREEN_HEIGHT//self.rows)
                    action,_=self.field.cellAction(row,col,"clear") #realiza la accion de limpiar el campo
                    if action =="win":
                        self.show_message("!Ganaste¡")
                        gameover=True
                    elif action=="lose":
                        self.show_message("!Perdiste¡")
                        gameover=True
            self.draw()

    def draw(self):
        cell_width=SCREEN_WIDTH//self.cols
        cell_height=SCREEN_HEIGHT//self.rows
        for row in range(self.rows):
            for col in range(self.cols):
                if self.field.playingField[row,col] == 1:
                    color = WHITE
                else:
                    color = BLACK
                pygame.draw.rect(self.screen, color, pygame.Rect(col*cell_width,row*cell_height,cell_width,cell_height))
        pygame.display.flip()

    def show_message(self,msg):
        endgame_msg=pygame.Rect(50,120,300,60)
        pygame.draw.rect(self.screen, BLACK, endgame_msg)
        msg_text=font.render(msg, True, WHITE)
        self.screen.blit(msg_text, (endgame_msg.x + 50, endgame_msg.y + 15))
        pygame.display.flip()
        pygame.time.delay(2000)



class Menu:
    def __init__(self,screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Visitor TT1 BRK", 30)
        self.buttons = [
            {"text": "Fácil", "rect": pygame.Rect(100,50,200,80), "action": self.start_easy_game},
            {"text": "Intermedio", "rect": pygame.Rect(100,150,200,80), "action": self.start_medium_game},
            {"text": "Difícil", "rect": pygame.Rect(100,250,200,80), "action": self.start_hard_game},
            {"text": "Salir", "rect": pygame.Rect(100,350,200,80), "action": self.quit_game},
        ]

    def draw(self):
        self.screen.fill(BLACK)
        title = self.font.render("Buscaminas", True, WHITE)
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
        Game(self.screen, 8, 8,10).run()

    def start_medium_game(self):
        Game(self.screen, 16,16,40).run()

    def start_hard_game(self):
        Game(self.screen, 30,16,99).run()

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
