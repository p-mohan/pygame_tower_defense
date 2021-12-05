import pygame
from .tower import Tower
import os
import math

range_imgs =[pygame.transform.scale(pygame.image.load(os.path.join("game_assets/support_towers","4.png")),(90,90)),
                                    pygame.transform.scale(pygame.image.load(os.path.join("game_assets/support_towers","5.png")),(90,90))]
class RangeTower(Tower):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.range = 75
        self.tower_imgs = range_imgs[:]
        self.effect =[0.2,0.4]
        self.name = "range"
    
    def draw(self, win):
        super().draw(win)
        # range circle
        if self.selected:
            pygame.draw.circle(win, (0, 0, 255), (self.x, self.y), self.range, 1)

    def support(self, towers):
        """
        Modify towers
        :param towers: list
        :return: None
        """

        for tower in towers:
            x = tower.x
            y = tower.y
            dis = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
            if dis < self.range:
                tower.range = tower.original_range + round(tower.range * self.effect[self.level - 1])


damage_imgs=[pygame.transform.scale(pygame.image.load(os.path.join("game_assets/support_towers","8.png")),(90,90)),
                                          pygame.transform.scale( pygame.image.load(os.path.join("game_assets/support_towers","9.png")),(90,90))]

class DamageTower(RangeTower):
    """
    Add damage to surrounding towers
    """
    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 100
        self.tower_imgs = damage_imgs[:]
        self.effect = [0.5, 1]
        self.name = "damage"


    def support(self, towers):
        """
        Modify towers
        :param towers: list
        :return: None
        """
        for tower in towers:
            x = tower.x
            y = tower.y
            dis = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
            if dis < self.range:
                tower.damage = tower.original_damage + round(tower.original_damage * self.effect[self.level - 1])