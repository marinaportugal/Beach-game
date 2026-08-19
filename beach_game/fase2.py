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

flor_img = pygame.image.load(
    os.path.join(base_path, "imagens", "flor.png")
).convert_alpha()   

flor2_img = pygame.image.load(
    os.path.join(base_path, "imagens", "flor2.png")
).convert_alpha()       

flor3_img = pygame.image.load(
    os.path.join(base_path, "imagens", "flor3.png")
).convert_alpha()   

inimigo2_img = pygame.image.load(   
    os.path.join(base_path, "imagens", "inimigo2.png")
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

flor_rect = flor_img.get_rect(
    topleft=(540,530)
)

flor2_rect = flor_img.get_rect(
    topleft=(450, 500)
)   

flor3_rect = flor_img.get_rect(
    topleft=(500,400)
)   

inimigo2_rect = inimigo2_img.get_rect(
    topleft=(150,300)
)


vida_inimigo = 500
inimigo_vivo = True

inimigo2_vivo = True    
vida_inimigo2 = 500


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

direcao2_x = random.choice([-1, 0, 1])
direcao2_y = random.choice([-1, 0, 1])
tempo_direcao2 = 0

running = True

velocidade_inimigo = 1
velocidade_inimigo2 = 1

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

    # Movimento aleatório do inimigo 2

    tempo_direcao2 += 1

# Troca de direção a cada 40 frames
    if tempo_direcao2 >= 40:

        while True:
            direcao2_x = random.choice([-1, 0, 1])
            direcao2_y = random.choice([-1, 0, 1])

        # Evita que fique completamente parado
            if direcao2_x != 0 or direcao2_y != 0:
                break

        tempo_direcao2 = 0

# Move o inimigo
    inimigo2_rect.x += direcao2_x * velocidade_inimigo2
    inimigo2_rect.y += direcao2_y * velocidade_inimigo2

# Se bater na parede, inverte a direção
    if inimigo2_rect.x <= 0 or inimigo2_rect.x >= WIDTH - inimigo2_rect.width:
        direcao2_x *= -1

    if inimigo2_rect.y <= 0 or inimigo2_rect.y >= HEIGHT - inimigo2_rect.height:
        direcao2_y *= -1

# Mantém o inimigo dentro da tela
    inimigo2_rect.x = max(0, min(inimigo2_rect.x, WIDTH - inimigo2_rect.width))
    inimigo2_rect.y = max(0, min(inimigo2_rect.y, HEIGHT - inimigo2_rect.height))
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

            if moedas == 20:
                print("Voce coletou 20 moedas! Ganhou 30 de vida!")
                vida += 30

            if moedas == 30:
                print("Voce coletou 30 moedas! Ganhou 25 de vida!")
                vida += 25
            
            if moedas == 40:
                print("Voce coletou 40 moedas! Ganhou 20 de vida!")
                vida += 20
            
            if moedas == 50:
                print("Voce coletou 50 moedas! Ganhou 10 de vida!")
                vida += 10
            
            if moedas == 60:
                print("Voce coletou 60 moedas! Ganhou 10 de vida!")
                vida += 10


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
    # ATAQUE NO INIMIGO 1
    # ======================

    if jogador.colliderect(inimigo_rect):

        vida -= 1
        vida_inimigo -= dano

        if vida <= 0:
            print("Game Over!")
            running = False

        if vida_inimigo <= 0:

            eliminacoes += 1
            print(eliminacoes)

            vida_inimigo = 500

            inimigo_rect.x = random.randint(0, WIDTH - inimigo_rect.width)
            inimigo_rect.y = random.randint(0, HEIGHT - inimigo_rect.height)


    # ======================
    # ATAQUE NO INIMIGO 2
    # ======================

    if jogador.colliderect(inimigo2_rect):

        vida -= 1
        vida_inimigo2 -= dano

        if vida <= 0:
            print("Game Over!")
            running = False

        if vida_inimigo2 <= 0:

            eliminacoes += 1
            print(eliminacoes)

            vida_inimigo2 = 500

            inimigo2_rect.x = random.randint(0, WIDTH - inimigo2_rect.width)
            inimigo2_rect.y = random.randint(0, HEIGHT - inimigo2_rect.height)

    if eliminacoes == 5:

        inimigo_vivo = False

        print("Inimigo derrotado! You Win")
        youwin = os.path.join(os.path.dirname(__file__), "youwin.py")
        subprocess.Popen([sys.executable, youwin])
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

    if inimigo2_vivo:
        
        screen.blit(
            inimigo2_img,
            inimigo2_rect
        )


    screen.blit(
        pip,
        (x,y)
    )

    screen.blit(
        flor_img, flor_rect
    )


    screen.blit(
        flor2_img, flor2_rect
    )

    screen.blit(
        flor3_img, flor3_rect)


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