import pygame
import math
import os
class Enemy:
    def __init__(self):

        self.animation_count = 0
        self.health = 1
        self.path = [(-5, 247), (5, 247), (164, 248), (267, 300), (597, 308), (705, 202), (774, 83), (902, 79), (966, 227), (1053, 300), (1135, 327), (1188, 390), (1147, 522), (849, 563), (757, 605), (164, 585), (65, 412), (1, 375),(-20,355)]
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.height = 64
        self.width = 64
        self.path_pos = 0
        self.move_count = 0
        self.dis= 0
        self.imgs = []
        self.flipped = False
        self.max_health= 0
        self.img = pygame.image.load(os.path.join("game_assets/enemies/1","1_enemies_1_run_000.png"))
    def draw(self, win):
        """
        Draws the enemy with images
        :param win:
        :return:
        """

        # for dot in self.path:
        #     pygame.draw.circle(win, (255,0,0), dot, 10,0)
        win.blit(self.img,(self.x -self.img.get_width()/2 ,self.y - self.img.get_height()/2 ))
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        length = 50
        move_by = round(length/self.max_health)
        health_bar = move_by * self.health
        pygame.draw.rect(win, (255,0,0), (self.x - 30, self.y -50, length,5),0)
        pygame.draw.rect(win, (0, 255, 0), (self.x - 30, self.y - 50, health_bar, 5), 0)


    def collide(self,X,Y):
        """
        Projectile hit enemy
        :param x: int
        :param y: int
        :return: Bool
        """
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True

        return False

    def move(self):
        """
        Move enemy
        :return: none

        """
        """
             Move enemy
             :return: none
             """
        self.img = self.imgs[self.animation_count]
        self.animation_count += 1
        if self.animation_count >= len(self.imgs):
            self.animation_count = 0
        x1, y1 = self.path[self.path_pos]
        if self.path_pos + 1 >= len(self.path):
            x2, y2 = (-10, 375)
        else:
            x2, y2 = self.path[self.path_pos + 1]
        dirn = ((x2 - x1) * 2, (y2 - y1) * 2)
        length = math.sqrt((dirn[0]) ** 2 + (dirn[1]) ** 2)
        dirn = (dirn[0] / length, dirn[1] / length)

        if dirn[0] < 0 and not (self.flipped):
            self.flipped = True
            for x, img in enumerate(self.imgs):
                self.imgs[x] = pygame.transform.flip(img, True, False)

        move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))

        self.x = move_x
        self.y = move_y

        # Go to next point
        if dirn[0] >= 0:  # moving right
            if dirn[1] >= 0:  # moving down
                if self.x >= x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x >= x2 and self.y <= y2:
                    self.path_pos += 1
        else:  # moving left
            if dirn[1] >= 0:  # moving down
                if self.x <= x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x <= x2 and self.y >= y2:
                    self.path_pos += 1


    def hitWithDamageIsDead(self, damage):
        """
        Report death and removes one unit of health
        :return:
        """
        self.health -= damage
        if self.health <= 0:
            return True
        return False



