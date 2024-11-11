import numpy as np
import pygame, random, sys

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)
RED = (255, 0, 0)
# Colores que se usan durante el juego

NUMBER_COLORS = {1: (0, 0, 255), 2: (0, 128, 0), 3: (255, 0, 0), 4: (0, 0, 128), 5: (128, 0, 0), 6: (0, 128, 128), 7: (0, 0, 0), 8: (128, 128, 128)}
# Colores para los números dentro del juego

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# Tamaño de la pantalla 800x600

font_path = "Grand9k_Pixel.ttf"
font = pygame.font.Font(font_path, 20)
# Fuente que se usa para el juego

class Field:
    def __init__(self, cols, rows, bombs):
        self.cols = cols
        self.rows = rows
        self.bombField = np.zeros((rows, cols))
        self.playingField = np.zeros((rows, cols))
        self.bombs = bombs
        self.flags = bombs

    def generateField(self, exclude_row, exclude_col):
        excluded = [(exclude_row, exclude_col)]
        for _ in range(self.bombs):
            while True:
                bombpos = (random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))
                if bombpos not in excluded:
                    excluded.append(bombpos)
                    self.bombField[bombpos[0], bombpos[1]] = 101
                    break

    def detectBomb(self, row, col):
        bombs = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= col + j < self.cols and 0 <= row + i < self.rows:
                    if self.bombField[row + i, col + j] == 101:
                        bombs += 1
        return bombs

    def checkFlagged(self):
        flaggedBombs = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if self.bombField[i, j] == 101 and self.playingField[i, j] == 2:
                    flaggedBombs += 1
        return flaggedBombs

    def cellAction(self, row, col, action):
        if self.playingField[row, col] != 1:
            if action == "clear":
                if self.playingField[row, col] != 2:
                    if self.bombField[row, col] == 101:
                        return "lose", 0
                    else:
                        self.playingField[row, col] = 1
                        bombs = self.detectBomb(row, col)
                        return "cell.clear", bombs
                return "none", 0
            elif action == "flag":
                if self.playingField[row, col] == 0 and self.flags >= 0:
                    self.playingField[row, col] = 2
                    self.flags -= 1
                    if self.checkFlagged() == self.bombs:
                        return "win", 0
                    return "cell.flag.add", 0
                elif self.playingField[row, col] == 2:
                    self.playingField[row, col] = 0
                    self.flags += 1
                    return "cell.flag.remove", 0
        return "none", 0

class Game:
    def __init__(self, screen, cols, rows, bombs):
        self.screen = screen
        self.field = Field(cols, rows, bombs)
        self.cols = cols
        self.rows = rows
        self.bombs = bombs
        self.gameover=False
        self.first_click = True  # Indica si el jugador aún no ha hecho el primer clic
        self.bombs_image=pygame.transform.scale(pygame.image.load("bomb.png"),(SCREEN_WIDTH // self.cols,SCREEN_HEIGHT // self.rows))
        self.cell_width = SCREEN_WIDTH // self.cols
        self.cell_height = SCREEN_HEIGHT // self.rows

    def run(self):
        while not self.gameover:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN: #ve la configuracion de los botones
                    x, y = pygame.mouse.get_pos()
                    col, row = x // (SCREEN_WIDTH // self.cols), y // (SCREEN_HEIGHT // self.rows)
                    if event.button == 1:  #click izquierdo libera la casilla
                        if self.first_click: # Generar bombas después del primer clic
                            self.field.generateField(row, col)
                            self.first_click = False
                        action, bombs_near = self.field.cellAction(row, col, "clear")
                    elif event.button == 3:  #click derecho pone las banderas
                        action, bombs_near = self.field.cellAction(row, col, "flag")

                    if action == "win":
                        self.show_message("¡Ganaste!")
                        self.gameover = True
                    elif action == "lose":
                        for row in range(self.rows):
                            for col in range(self.cols): #Mostrará todas las bombas
                                rect = pygame.Rect(col * self.cell_width, row * self.cell_height, self.cell_width, self.cell_height)
                                if (action== "win" or "lose") and self.field.bombField[row,col]==101:
                                    self.screen.blit(self.bombs_image, rect.topleft)
                        self.show_message("¡Perdiste!")
                        self.gameover = True
            self.draw()

    def draw(self):
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(col * self.cell_width, row * self.cell_height, self.cell_width, self.cell_height)
                if self.field.playingField[row, col] == 1: #detectara las bombas cercanas
                    pygame.draw.rect(self.screen, WHITE, rect)
                    bombs_near = self.field.detectBomb(row, col)
                    if bombs_near > 0: #Colocará los numeros de bombas cercanas dentro de las celdas correspodientes
                        text_color = NUMBER_COLORS.get(bombs_near, BLACK)
                        text = font.render(str(bombs_near), True, text_color)
                        text_rect = text.get_rect(center=(col * self.cell_width + self.cell_width // 2, row * self.cell_height + self.cell_height // 2))
                        self.screen.blit(text, text_rect)
                elif self.field.playingField[row, col] == 2: #contiene el formato de las banderas y la posicion
                    pygame.draw.rect(self.screen, GRAY, rect)
                    flag_text = font.render("?", True, RED)
                    flag_rect = flag_text.get_rect(center=(col * self.cell_width + self.cell_width // 2, row * self.cell_height + self.cell_height // 2))
                    self.screen.blit(flag_text, flag_rect)
                else:
                    pygame.draw.rect(self.screen, GRAY, rect) #dibuja las celdas poniendole color gris
                pygame.draw.rect(self.screen, WHITE, rect, 1)  #dibuja los bordes de las celdas

        pygame.display.flip()

    def show_message(self, message): # contiene la configuracion del recuadro de texto que se mostrará cuando termine el juego
        endgame_msg = pygame.Rect(300, 250, 300, 60)
        pygame.draw.rect(self.screen, BLACK, endgame_msg)
        msg_text = font.render(message, True, WHITE)
        self.screen.blit(msg_text, (endgame_msg.x + 50, endgame_msg.y))
        pygame.display.flip()
        pygame.time.delay(2000)

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = font # Se usa la fuente especificada más arriba (Grand9k Pixel)
        self.buttons = [
            {"text": "Fácil", "rect": pygame.Rect(300, 150, 200, 30), "action": self.start_easy_game},
            {"text": "Intermedio", "rect": pygame.Rect(300, 250, 200, 30), "action": self.start_medium_game},
            {"text": "Difícil", "rect": pygame.Rect(300, 350, 200, 30), "action": self.start_hard_game},
            {"text": "Salir", "rect": pygame.Rect(300, 450, 200, 30), "action": self.quit_game},
        ] # Diccionario que contiene las palabras, posiciones y acciones de los botones

    def draw(self):
        self.screen.fill(BLACK) # Se llena la pantalla de color negro
        title = self.font.render("BUSCAMINAS", True, WHITE) # Titulo del menú
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 10)) # Posición del titulo
        for button in self.buttons:
            pygame.draw.rect(self.screen, BLACK, button["rect"], 2)
            label = self.font.render(button["text"], True, WHITE)
            self.screen.blit(label, (button["rect"].x + button["rect"].width // 2 - label.get_width() // 2,
                                     button["rect"].y + button["rect"].height // 2 - label.get_height() // 2))
            # Dibuja los rectángulos para las opciones del menú, obteniendo datos del diccionario en el constructor

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button["rect"].collidepoint(mouse_pos):
                    button["action"]() # Obteniendo la posición del mouse, si este colisiona con algún botón se realiza la acción correspondiente al botón

    def start_easy_game(self):
        Game(self.screen, 8, 8, 10).run()
        # Se inicia el juego en modo fácil, con 8 columnas, 8 filas y 10 bombas

    def start_medium_game(self):
        Game(self.screen, 16, 16, 40).run()
        # Se inicia el juego en modo fácil, con 16 columnas, 16 filas y 40 bombas

    def start_hard_game(self):
        Game(self.screen, 30, 16, 99).run()
        # Se inicia el juego en modo fácil, con 30 columnas, 16 filas y 99 bombas
    
    def quit_game(self):
        pygame.quit()
        sys.exit() # Se cierra el juego

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
        # Función para iniciar el menú

if __name__ == "__main__":
    main()
