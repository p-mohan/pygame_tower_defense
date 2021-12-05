import pygame
import math
from menu.menu import Menu
menu_bg = pygame.transform.scale(pygame.image.load("game_assets/menu.png"),(120,50))
upgrade_btn = pygame.transform.scale(pygame.image.load("game_assets/menu/upgrade.png"),(40,40))
class Tower:
    """
    Abstract class
    """
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.sell_price = [0,0,0]
        self.level = 0
        self.price = [0,0,0]
        self.selected = False

        self.imgs = []
        self.tower_imgs = []
        self.damage = 1
        self.range = 0
        self.original_range = self.range
        self.original_damage = self.damage
        self.menu = Menu(self, menu_bg,[2000,5000])
        self.menu.add_btn(upgrade_btn,"Upgrade")
        self.is_moving = False

    def draw(self, win):
        img = self.tower_imgs[self.level]
        win.blit(img, (self.x-img.get_width()//2, self.y))
        #draw menu
        if self.selected:
            self.menu.draw(win)

    def click(self,X,Y):
        """
        Returns if tower is clicked and selects it.
        :param X: int
        :param Y: int
        :return: bool
        """
        img = self.tower_imgs[self.level]
       # print("I am at",self.x, self.y)
       # print ("boundaries ",self.x-img.get_width()//2,self.x+img.get_width()//2, self.y +  img.get_height()//2,self.y -  img.get_height()//2  )
        if X <= self.x + img.get_width()//2 and X >= self.x - img.get_width()//2:
            if Y <= self.y + img.get_height()//2 and Y >= self.y - img.get_height()//2:
                return True
        return False
    def sell(self):
        """
        return sell price
        :return:
        """
        return self.sell_price[self.level - 1]
    def upgrade(self):
        if self.level < len(self.tower_imgs) - 1:
            self.level += 1
            self.damage +=1
    def get_upgrade_cost(self):
        """
        if zero can't upgrade
        :return:
        """
        return self.price[self.level - 1 ]
    def move(self,x,y):
        """
        Moves tower to given xy
        :param x:
        :param y:
        :return:
        """
        self.x = x
        self.y = y
        self.menu.x = x
        self.menu.y = y
        self.menu.update()

    def isOverlap(self, otherTower):
        x2 = otherTower.x
        y2 = otherTower.y + 45
        d = math.sqrt((y2 - self.y)**2 + (x2 - self.x)**2)
        if d >  70:
            return False
        else:
            return True

