import pygame
import os
import random

pygame.init()

HEIGHT = 600
WEIGHT = 400

screen = pygame.display.set_mode((HEIGHT, WEIGHT))
pygame.display.set_caption("Sand Escape")

clock = pygame.time.Clock()

# determine base path for assets
base_path = os.path.dirname(os.path.abspath(__file__))

# load background once using base_path
background_path = os.path.join(base_path, "imagens", "Island.jpeg")



if os.path.exists(background_path):
    background = pygame.image.load(background_path).convert()

else:
    # fallback: try relative path
    background = pygame.Surface((HEIGHT, WEIGHT))
    background.fill((0, 0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # draw background then other elements
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    font = pygame.font.Font(None, 100)
    text = font.render("YOU WIN!", True, (255, 211, 69))
    text_rect = text.get_rect(center=(HEIGHT // 2, WEIGHT // 2))
    screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(60)
