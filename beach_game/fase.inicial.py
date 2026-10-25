import pygame
import os
import subprocess
import sys

pygame.init()

LARGURA, ALTURA = 600, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Sand Escape")
relogio = pygame.time.Clock()

base_path = os.path.dirname(os.path.abspath(__file__))

# Fundo do menu
caminho = os.path.join(base_path, "imagens", "background2.png")
fundo = pygame.image.load(caminho).convert()
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

# Fontes
titulo = pygame.font.Font(None, 80)
fonte = pygame.font.Font(None, 45)
pequena = pygame.font.Font(None, 28)

# Botões
botao_jogar = pygame.Rect(175, 300, 250, 65)
botao_sair = pygame.Rect(175, 390, 250, 65)

rodando = True

while rodando:
    tela.blit(fundo, (0, 0))

    # Camada escura para destacar o texto
    sombra = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    sombra.fill((0, 0, 0, 100))
    tela.blit(sombra, (0, 0))

    # Título
    texto = titulo.render("SAND ESCAPE", True, (255, 220, 100))
    tela.blit(texto, texto.get_rect(center=(300, 180)))

    subtitulo = pequena.render(
        "Sobreviva e derrote os inimigos!",
        True, (255, 255, 255)
    )
    tela.blit(subtitulo, subtitulo.get_rect(center=(300, 240)))

    # Botão JOGAR
    pygame.draw.rect(tela, (46, 139, 87), botao_jogar, border_radius=12)
    jogar = fonte.render("JOGAR", True, (255, 255, 255))
    tela.blit(jogar, jogar.get_rect(center=botao_jogar.center))

    # Botão SAIR
    pygame.draw.rect(tela, (160, 45, 45), botao_sair, border_radius=12)
    sair = fonte.render("SAIR", True, (255, 255, 255))
    tela.blit(sair, sair.get_rect(center=botao_sair.center))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if botao_jogar.collidepoint(event.pos):
                pygame.quit()
                caminho_fase = os.path.join(base_path, "fase1.py")
                subprocess.Popen([sys.executable, caminho_fase])
                sys.exit()

            if botao_sair.collidepoint(event.pos):
                rodando = False

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()