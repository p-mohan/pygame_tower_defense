import pygame
from game import Game
import os
start_btn = pygame.image.load("game_assets/menu/button_start.png")
logo = pygame.transform.scale(pygame.image.load("game_assets/logo.png"),(700,300))
pygame.display.set_caption('Pygame Tower Defense')
class MainMenu:
    def __init__(self):
        self.width = 1366
        self.height = 768
        self.win = pygame.display.set_mode((self.width, self.height))
        self.bg = pygame.image.load(os.path.join("game_assets", "bg.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.btn = (self.width/2 - start_btn.get_width()/2, self.height/2 - start_btn.get_height()/2)
    def run(self):
       
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONUP:
                    #start button click
                    x,y = pygame.mouse.get_pos()
                    if self.btn[0] <=x <= self.btn[0] + start_btn.get_width():
                        if self.btn[1] <= y <= self.btn[1] + start_btn.get_height():
                            game = Game(self.win)
                            game.run()
                            del game
            self.draw()

        pygame.quit()

    def draw(self):
        self.win.blit(self.bg, (0,0))
        self.win.blit(logo, (self.width/2 - logo.get_width()/2, 0))
        self.win.blit(start_btn,(self.btn[0],self.btn[1]))
        pygame.display.update()