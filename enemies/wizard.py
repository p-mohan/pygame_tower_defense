import pygame
import os
from .enemy import Enemy
imgs = []
for x in range(19):
    if x < 10:
        imgs.append(pygame.transform.scale(
            pygame.image.load(os.path.join("game_assets/enemies/2", "2_enemies_1_run_00" + str(x)) + ".png"),
            (64, 64)))
    else:
        imgs.append(pygame.transform.scale(
            pygame.image.load(os.path.join("game_assets/enemies/2", "2_enemies_1_run_0" + str(x)) + ".png"), (64, 64)))
class Wizard(Enemy):
    def __init__(self):
        super().__init__()
        self.name = "wiz"
        self.max_health = 3
        self.health = self.max_health
        self.imgs = imgs[:]
        self.reward = 3

