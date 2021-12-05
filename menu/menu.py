import pygame
star = pygame.transform.scale(pygame.image.load("game_assets/star.png"),(25,25))
star2 = pygame.transform.scale(pygame.image.load("game_assets/star.png"),(20,20))
import threading
from menu.message import Message
class Button:
    def __init__(self,menu, img,name):
        self.name = name
        self.img = img
        self.x = menu.x - 50
        self.y = menu.y - 70
        self.menu = menu
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        

    def draw(self,win):
        win.blit(self.img, (self.x,self.y))

    def click(self,X,Y):
        """
        Returns if button is clicked.
        :param X: int
        :param Y: int
        :return: bool
        """
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

    def update(self):
        self.x = self.menu.x -50
        self.y = self.menu.y - 70

class Menu:
    def __init__(self,tower, img, item_cost):
        self.x = tower.x
        self.y = tower.y
        self.width = img.get_width()
        self.height = img.get_height()
        self.items = 0
        self.buttons = []
        self.menu_bg = img
        self.item_cost = item_cost
        self.font =  pygame.font.SysFont("constantia", 20)
        self.tower = tower
      

    def add_btn(self, img,name):
        self.items += 1
        btn_x = self.x - self.menu_bg.get_width()/2 #self.x - (self.width - img.get_width())/2
        btn_y = self.y - (self.menu_bg.get_height() + img.get_height()/2)
        self.buttons.append(Button(self,img,name))



    def draw(self,win):
        win.blit(self.menu_bg,(self.x - self.menu_bg.get_width()/2,self.y- 75))
        for button in self.buttons:
            button.draw(win)
            win.blit(star,(button.x + button.width + 10, button.y - 5) )
            text = self.font.render(str(self.item_cost[self.tower.level]),1,(255,255,255))
            win.blit(text, (button.x + button.width + 10, button.y + star.get_height() - 5))


    def get_clicked(self,X,Y):
        """
        return clicked item from menu
        :param X:
        :param Y:
        :return:
        """
        for btn in self.buttons:
             if btn.click(X,Y):
                return btn.name
        return None

    def get_item_cost(self):
        return self.item_cost[self.tower.level - 1]

    def update(self):
        """
        update menu & button location
        :return:
        """
        for btn in self.buttons:
            btn.update()

class PlayPauseButton(Button):
    def __init__(self,play_img, pause_img, X,Y):
        self.img = pause_img
        self.x = X
        self.y = Y
        self.play = play_img
        self.pause = pause_img
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def swap_img(self):
        if self.img == self.play:
            self.img = self.pause
        else:
            self.img = self.play


class VerticalButton(Button):
    def __init__(self,x,y, img,name,cost,desc):
        self.name = name
        self.img = img
        self.x = x
        self.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.cost = cost
        self.desc = desc


class VerticalMenu(Menu):
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.width = img.get_width()
        self.height = img.get_height()
        self.items = 0
        self.buttons = []
        self.menu_bg = img
        self.font = pygame.font.SysFont("constantia", 20)
        self.showInfoMessage = False
        self.displayMessage = ""

    def setMessageInterval(self, sec, run=True):
        def func_wrapper(run):
            self.showInfoMessage = False
            self.game_run = run
        t = threading.Timer(sec, func_wrapper,args=[run])
        t.start()
        return t

    def add_btn(self, img,name, desc, cost):
        self.items += 1
        btn_x = self.x  - self.width/2  + 10 #self.x - (self.width - img.get_width())/2
        btn_y = self.y  + (self.items -1) * 80 - 55
        self.buttons.append(VerticalButton(btn_x,btn_y,img,name, cost,desc))

    def get_item_cost(self, name):
        for btn in self.buttons:
            if btn.name == name:
                self.displayMessage =  btn.desc
                self.showInfoMessage = True
                self.setMessageInterval(5,False)
                return btn.cost
        return -1


    def draw(self, win):
        win.blit(self.menu_bg, (self.x - self.menu_bg.get_width() / 2, self.y - 75))
        if self.showInfoMessage:
            msg = Message(self.displayMessage, (self.width*2),10,300)
            msg.draw(win)
        for button in self.buttons:
            button.draw(win)
            win.blit(star2, (button.x - button.width/2 + 25, button.y + button.height ))
            text = self.font.render(str(button.cost), 1, (255, 255, 255))
            win.blit(text, (button.x + button.width/2 - 5, button.y + button.height/2+  star2.get_height() + 5))