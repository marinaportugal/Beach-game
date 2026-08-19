import os
import subprocess
import sys
import pygame
import random

pygame.init()

# ==========================
# JANELA
# ==========================

WIDTH = 600
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sand Escape")

clock = pygame.time.Clock()

# ==========================
# IMAGENS
# ==========================

base_path = os.path.dirname(__file__)

background = pygame.image.load(
    os.path.join(base_path, "imagens", "background2.png")
).convert()

pip = pygame.image.load(
    os.path.join(base_path, "imagens", "pip.png")
).convert_alpha()

moeda_img = pygame.image.load(
    os.path.join(base_path, "imagens", "moeda.png")
).convert_alpha()

espada_img = pygame.image.load(
    os.path.join(base_path, "imagens", "espada.png")
).convert_alpha()

machado_img = pygame.image.load(
    os.path.join(base_path, "imagens", "machado.png")
).convert_alpha()

inimigo_img = pygame.image.load(
    os.path.join(base_path, "imagens", "inimigo.png")
).convert_alpha()


# ==========================
# JOGADOR
# ==========================

x = 100
y = 200

largura = pip.get_width()
altura = pip.get_height()

velocidade = 4

# ==========================
# STATUS
# ==========================


vida = 100
moedas = 0
eliminacoes = 0

arma = None
dano = 0


# ==========================
# OBJETOS
# ==========================

moedas_rect = []

for i in range(5):
    moeda = moeda_img.get_rect(
        topleft=(
            random.randint(20, 560),
            random.randint(20, 560)
        )
    )

    moedas_rect.append(moeda)

espada_rect = espada_img.get_rect(
    topleft=(450,400)
)

machado_rect = machado_img.get_rect(
    topleft=(450,400)
)

inimigo_rect = inimigo_img.get_rect(
    topleft=(200,350)
)


vida_inimigo = 500
inimigo_vivo = True


# ==========================
# ARMA ALEATÓRIA
# ==========================

tipo_arma = None


def gerar_arma():

    global tipo_arma

    tipo_arma = random.choice(
        ["Espada","Machado"]
    )


    pos_x = random.randint(50,550)
    pos_y = random.randint(50,550)


    if tipo_arma == "Espada":

        espada_rect.x = pos_x
        espada_rect.y = pos_y


    else:

        machado_rect.x = pos_x
        machado_rect.y = pos_y


# primeira arma do jogo
gerar_arma()


# ==========================
# FONTE
# ==========================

fonte = pygame.font.SysFont(
    None,
    30
)


running = True

velocidade_inimigo = 2

while running:


    # EVENTOS

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False


    teclas = pygame.key.get_pressed()


    # ======================
    # MOVIMENTO
    # ======================

    if teclas[pygame.K_LEFT]:
        x -= velocidade

    if teclas[pygame.K_RIGHT]:
        x += velocidade

    if teclas[pygame.K_UP]:
        y -= velocidade

    if teclas[pygame.K_DOWN]:
        y += velocidade

    # LIMITES

    x = max(0,min(x,WIDTH-largura))
    y = max(0,min(y,HEIGHT-altura))


    jogador = pygame.Rect(
        x,
        y,
        largura,
        altura
    )

    if inimigo_rect.x < x:
        inimigo_rect.x += velocidade_inimigo

    elif inimigo_rect.x > x:
        inimigo_rect.x -= velocidade_inimigo

    if inimigo_rect.y < y:
        inimigo_rect.y += velocidade_inimigo

    elif inimigo_rect.y > y:
        inimigo_rect.y -= velocidade_inimigo


    # ======================
    # MOEDA
    # ======================
    for moeda in moedas_rect:

        if jogador.colliderect(moeda):

            moedas += 1

            moeda.x = random.randint(20, 560)
            moeda.y = random.randint(20, 560)

            if moedas == 10:

                print("Voce coletou 10 moedas! Ganhou 50 de vida!")
                vida += 50


    # ======================
    # PEGAR ARMA
    # ======================

    if tipo_arma == "Espada":

        if jogador.colliderect(espada_rect):

            arma = "Espada -15"
            dano = 15

            gerar_arma()


    elif tipo_arma == "Machado":

        if jogador.colliderect(machado_rect):

            arma = "Machado -30"
            dano = 30

            gerar_arma()
        

    # ======================
    # ATAQUE
    # ======================

    if jogador.colliderect(inimigo_rect):

        vida_inimigo -= dano
        vida -= 1  # jogador perde vida ao colidir com o inimigo

        if vida <= 0:
                print("Game Over! Você perdeu todas as suas vidas.")
                running = False

        if vida_inimigo <= 0:

            eliminacoes += 1
            print(eliminacoes)

            vida_inimigo = 100  # reinicia a vida do inimigo

            inimigo_rect.x = random.randint(0, 560 - inimigo_rect.width)
            inimigo_rect.y = random.randint(0, 560 - inimigo_rect.height)


            if eliminacoes == 3:

                inimigo_vivo = False
                print("Inimigo derrotado! Avançando para a próxima fase...")
                caminho_fase2 = os.path.join(os.path.dirname(__file__), "fase2.py")
                print(caminho_fase2)
                subprocess.Popen([sys.executable, caminho_fase2])
                pygame.quit()
                sys.exit()
            


    # ======================
    # DESENHO
    # ======================

    screen.blit(
        background,
        (0,0)
    )

    for moeda in moedas_rect:
        screen.blit(
            moeda_img,
            moeda
        )


    # mostra arma atual

    if tipo_arma == "Espada":

        screen.blit(
            espada_img,
            espada_rect
        )


    else:

        screen.blit(
            machado_img,
            machado_rect
        )


    if inimigo_vivo:

        screen.blit(
            inimigo_img,
            inimigo_rect
        )


    screen.blit(
        pip,
        (x,y)
    )


    texto = fonte.render(
        f"Vida: {vida}  Moedas: {moedas}  Eliminações: {eliminacoes}  Arma: {arma}",
        True,
        (255,255,255)
    )

    screen.blit(
        texto,
        (10,10)
    )

    pygame.display.flip()

    clock.tick(60)


pygame.quit()