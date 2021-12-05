import pygame
from .tower import Tower
import os
import math
from menu.menu import Menu
menu_bg = pygame.transform.scale(pygame.image.load("game_assets/menu.png"),(120,50))
upgrade_btn = pygame.transform.scale(pygame.image.load("game_assets/menu/upgrade.png"),(40,40))

long_tower_imgs = []
long_archer_imgs = []
for x in range(7, 10):
    long_tower_imgs.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/archer_towers/archer_1", str(x) + ".png")),
        (90, 90)))
# archer
for x in range(37, 43):
    long_archer_imgs.append(
        pygame.image.load(os.path.join("game_assets/archer_towers/archer_top", str(x) + ".png")))


class ArcherTowerLong(Tower):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.tower_imgs = long_tower_imgs[:]
        self.archer_imgs = long_archer_imgs[:]
        self.archer_count = 0
        self.range = 200
        self.inRange = False
        self.left = False
        self.damage = 1
        self.menu = Menu(self, menu_bg, [2000, 5000])
        self.menu.add_btn(upgrade_btn, "Upgrade")
        self.name = "archer"


    def draw(self, win):
        super().draw(win)

        if self.inRange and not(self.is_moving):
            self.archer_count += 1
            if self.archer_count >= len(self.archer_imgs) * 20:
                self.archer_count = 0
        else:
            self.archer_count = 0
        archer = self.archer_imgs[self.archer_count // 20]
        if self.left == True:
            win.blit(archer, ((self.x + self.width / 2 - archer.get_width() + 10), (self.y + 20 - archer.get_height())))
        else:
            win.blit(archer, ((self.x + self.width / 2 - 20), (self.y + 20 - archer.get_height())))
        if self.selected:
            #range circle
            pygame.draw.circle(win, (0,255,0), (self.x,self.y), self.range,1)

    def change_range(self, r):
        self.range = r
    def attack(self, enemies):
        """
        Attacks enemy list and modify it.
        :param enemies:
        :return:money
        """
        money = 0
        self.inRange = False
        enemy_closest = []
        for enemy in enemies:
            x = enemy.x
            y = enemy.y
            dis = math.sqrt((self.x -  enemy.img.get_width()/2 - x)**2 +(self.y - enemy.img.get_height()/2  - y)**2)
            if dis < self.range:
                self.inRange = True
                enemy_closest.append(enemy)

        enemy_closest.sort(key= lambda x: x.path_pos)
        enemy_closest = enemy_closest[::-1]
        if len(enemy_closest) > 0:
            first_enemy = enemy_closest[0]
            if self.archer_count == 5:
                if first_enemy.hitWithDamageIsDead(self.damage) == True:
                     enemies.remove(first_enemy)
                     money = first_enemy.reward * 2

            if first_enemy.x < self.x and not(self.left):
                self.left = True
                for x, img in enumerate(self.archer_imgs):
                    self.archer_imgs[x] = pygame.transform.flip(img, True, False)
            elif first_enemy.x > self.x and self.left:
                self.left = False
                for x, img in enumerate(self.archer_imgs):
                    self.archer_imgs[x] = pygame.transform.flip(img, True, False)
        return money

    def get_upgrade_cost(self):
        return  self.menu.get_item_cost()


short_tower_imgs = []
short_archer_imgs = []

for x in range(10, 13):
    short_tower_imgs.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/archer_towers/archer_2", str(x) + ".png")),
        (90, 90)))
# archer
for x in range(43, 49):
    short_archer_imgs.append(
        pygame.image.load(os.path.join("game_assets/archer_towers/archer_top_2", str(x) + ".png")))


class ArcherTowerShort(ArcherTowerLong):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.tower_imgs = short_tower_imgs[:]
        self.archer_imgs = short_archer_imgs[:]
        self.archer_count = 0
        self.range = 100
        self.inRange = False
        self.left = False
        self.damage = 2
        self.menu = Menu(self, menu_bg, [2500, 5500])
        self.menu.add_btn(upgrade_btn, "Upgrade")
        self.name ="archer2"