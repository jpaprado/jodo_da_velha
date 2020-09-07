import pygame
import math

from pathlib import Path

mypath = Path().absolute()
print('Caminho Absoluto : {}'.format(mypath))

pygame.init()

# Screen
LARGURA = 300
LINHAS = 3
win = pygame.display.set_mode((LARGURA, LARGURA))
pygame.display.set_caption("Jogo-da-Velha")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Imagens
X_IMAGEM = pygame.transform.scale(pygame.image.load("./imagens/x.png"), (80, 80))
O_IMAGEM = pygame.transform.scale(pygame.image.load("./imagens/o.png"), (80, 80))

# Fontes
FONTE_FINAL = pygame.font.SysFont('courier', 40)


def desenha_tabuleiro():
    gap = LARGURA // LINHAS

    # Pontos iniciais
    x = 0
    y = 0

    for i in range(LINHAS):
        x = i * gap
        pygame.draw.line(win, GRAY, (x, 0), (x, LARGURA), 3)
        pygame.draw.line(win, GRAY, (0, x), (LARGURA, x), 3)


def inicia_tabuleiro():
    dis_to_cen = LARGURA // LINHAS // 2

    # Inicia array
    game_array = [[None, None, None], [None, None, None], [None, None, None]]

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x = dis_to_cen * (2 * j + 1)
            y = dis_to_cen * (2 * i + 1)

            # Coloca coordenadas do centro
            game_array[i][j] = (x, y, "", True)

    return game_array


def click(game_array):
    global x_turno, o_turno, imagens

    # Posicao do mouse
    m_x, m_y = pygame.mouse.get_pos()

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x, y, peca, pode_jogar = game_array[i][j]

            # Distancia entre o mouse e o centro da cada quadrado
            dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)

            # se estah dentro de algum quadrado
            if dis < LARGURA // LINHAS // 2 and pode_jogar:
                if x_turno:  # se o X joga
                    imagens.append((x, y, X_IMAGEM))
                    x_turno = False
                    o_turno = True
                    game_array[i][j] = (x, y, 'x', False)

                elif o_turno:  # se o O joga
                    imagens.append((x, y, O_IMAGEM))
                    x_turno = True
                    o_turno = False
                    game_array[i][j] = (x, y, 'o', False)


# Verifica se alguem ganhou
def teve_vitoria(game_array):
    # verifica linhas
    for linha in range(len(game_array)):
        if (game_array[linha][0][2] == game_array[linha][1][2] == game_array[linha][2][2]) and game_array[linha][0][2] != "":
            display_mensagem(game_array[linha][0][2].upper() + " ganhou!")
            return True

    # verifica colunas
    for col in range(len(game_array)):
        if (game_array[0][col][2] == game_array[1][col][2] == game_array[2][col][2]) and game_array[0][col][2] != "":
            display_mensagem(game_array[0][col][2].upper() + " ganhou!")
            return True

    # verifica diagonal principal
    if (game_array[0][0][2] == game_array[1][1][2] == game_array[2][2][2]) and game_array[0][0][2] != "":
        display_mensagem(game_array[0][0][2].upper() + " ganhou!")
        return True

    # verifica diagonal oposta
    if (game_array[0][2][2] == game_array[1][1][2] == game_array[2][0][2]) and game_array[0][2][2] != "":
        display_mensagem(game_array[0][2][2].upper() + " ganhou!")
        return True

    return False


def teve_empate(game_array):
    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            if game_array[i][j][2] == "":
                return False

    display_mensagem("Empatou!")
    return True


def display_mensagem(msg):
    pygame.time.delay(500)
    win.fill(WHITE)
    texto = FONTE_FINAL.render(msg, 1, BLACK)
    win.blit(texto, ((LARGURA - texto.get_width()) // 2, (LARGURA - texto.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(3000)


def render():
    win.fill(WHITE)
    desenha_tabuleiro()

    # Desenha  X's e O's
    for imagem in imagens:
        x, y, IMAGEM = imagem
        win.blit(IMAGEM, (x - IMAGEM.get_width() // 2, y - IMAGEM.get_height() // 2))

    pygame.display.update()


def main():
    global x_turno, o_turno, imagens

    imagens = []

    run = True

    x_turno = True
    o_turno = False

    game_array = inicia_tabuleiro()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click(game_array)

        render()

        if teve_vitoria(game_array) or teve_empate(game_array):
            run = False


while True:
    if __name__ == '__main__':
        main()
