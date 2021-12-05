import pygame
import os
from enemies.scorpion import Scorpion
from enemies.club import Club
from towers.archerTower import ArcherTowerLong, ArcherTowerShort
from towers.supportTower import RangeTower, DamageTower
from enemies.wizard import Wizard
from menu.menu import VerticalMenu, PlayPauseButton
from menu.message import Message
import time
import random
import threading



pygame.font.init()
path = [(-5, 247), (5, 247), (164, 248), (267, 300), (597, 308), (705, 202), (774, 83), (902, 79), (966, 227), (1053, 300), (1135, 327), (1188, 390), (1147, 522), (849, 563), (757, 605), (164, 585), (65, 412), (1, 375),(-20,355)]

lives_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "heart.png")), (16, 16))
star_img = pygame.image.load(os.path.join("game_assets", "star.png"))
side_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "side.png")), (75, 350))

buy_archer = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/menu", "buy_archer.png")), (50,50))
buy_archer_2 = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/menu", "buy_archer_2.png")), (50,50))
buy_damage = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/menu", "buy_damage.png")), (50,50))
buy_range = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/menu", "buy_range.png")), (50,50))

play_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/menu", "button_play.png")), (50,50))
pause_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/menu", "button_pause.png")), (50,50))

sound_on_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/menu", "button_music.png")), (50,50))
sound_off_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/menu", "button_music_off.png")), (50,50))

wave_bg = pygame.image.load(os.path.join("game_assets", "wave.png"))

attack_tower_names = ["archer","archer2"]
support_tower_names =["damage", "range"]
pygame.init()
pygame.mixer.music.load(os.path.join("game_assets", "gmusic.ogg"))
#(scorp, wiz, club)

waves = [
    [10,0,0],
    [10,2,0],
    [10,5,1],
    [10,10,2],
    [15,10,5],
    [15,15,8],
    [15,15,10],
    [30,15,12],
    [35,30,15],
    [38,35,18],
    [40,40,20],
    [45,41,21],
    [50,42,22],
    [55,43,21]

]
class Game:
    def __init__(self,win):
        self.width = 1366
        self.height = 768
        self.clicks =[]
        self.win = win
        self.enemies = [Wizard()]  # Scorpion(),Club()
        self.attack_towers = []
        self.support_towers = []
        self.lives = 10
        self.money = 2000
        self.vel = 3
        self.bg = pygame.image.load(os.path.join("game_assets", "bg.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.timer = time.time()
        self.lives_font = pygame.font.SysFont("constantia", 30)
        self.selected_tower = None
        self.menu = VerticalMenu(self.width - side_img.get_width() + 40, 200,side_img)
        self.menu.add_btn(buy_archer, "buy_archer","Light Archerer", 500)
        self.menu.add_btn(buy_archer_2, "buy_archer_2","Super Archerer",750)
        self.menu.add_btn(buy_damage, "buy_damage","Damage multiplier",1000)
        self.menu.add_btn(buy_range, "buy_range","Range Increaser",1000)
        self.moving_item = None
        self.wave = 0
        self.current_wave = waves[self.wave][:]
        self.pause = False
        self.is_music_on = False
        self.playPauseBtn = PlayPauseButton(play_btn,pause_btn, 10, self.height - 85)
        self.soundBtn = PlayPauseButton(sound_on_btn, sound_off_btn, 70, self.height - 85)
        self.firstTimePlay = True
        self.showInfoMessage = False
        self.displayMessage = ""
        self.game_run = True


    def gen_enemies(self):
        if sum(self.current_wave) == 0:
            if len(self.enemies) == 0:
                self.wave += 1
                if self.wave < len(waves):
                    self.current_wave = waves[self.wave]
                else:
                    self.pause = True
                    self.displayMessage = "You Win!!!"
                    self.showInfoMessage = True
                    self.setMessageInterval(5,False)

                #self.pause = True
        else:
            wave_enemies = [Scorpion(), Wizard(), Club()]
            for x in range(len(self.current_wave)):
                if self.current_wave[x] !=0:
                    self.enemies.append(wave_enemies[x])
                    self.current_wave[x] = self.current_wave[x] - 1
                    break

    def setMessageInterval(self, sec, run=True):
        def func_wrapper(run):
            self.showInfoMessage = False
            self.game_run = run
        t = threading.Timer(sec, func_wrapper,args=[run])
        t.start()
        return t

    def run(self):
        self.game_run = True
        clock = pygame.time.Clock();
        while self.game_run:
            clock.tick(60)
            #generate enemies
            if self.pause == False:
                if time.time() - self.timer >= random.randrange(1, 60) / 2:
                    self.timer = time.time()
                    #self.enemies.append(random.choice([Club(), Scorpion(), Wizard()]))
                    #print("Gen enemies")
                    self.gen_enemies()
            pos = pygame.mouse.get_pos()

            #check moving
            if self.moving_item:
                self.moving_item.move(pos[0], pos[1])

            # pygame.time.delay(500)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_run = False

                if event.type == pygame.MOUSEBUTTONUP:
                    # self.clicks.append((pos[0], pos[1]))
                    # print((pos[0], pos[1]))
                    #if moving?
                    if self.moving_item:
                        is_overlapping = False
                        t_list = self.attack_towers[:] + self.support_towers[:]
                        for t in t_list:
                            if t.isOverlap(self.moving_item):
                                is_overlapping = True
                                break
                        if not is_overlapping and not self.isOnMyPath(self.moving_item.x, self.moving_item.y):
                            if self.moving_item.name in attack_tower_names:
                                self.attack_towers.append(self.moving_item)
                            elif self.moving_item.name in support_tower_names:
                                self.support_towers.append(self.moving_item)
                            self.moving_item.moving = False
                            self.moving_item = None
                    else:
                        #check for play or pause
                        if self.playPauseBtn.click(pos[0],pos[1]):
                            self.pause = not(self.pause)
                            self.playPauseBtn.swap_img()

                        if self.soundBtn.click(pos[0], pos[1]):
                            self.is_music_on = not (self.is_music_on)
                            self.soundBtn.swap_img()
                            if self.is_music_on:
                                if self.firstTimePlay:
                                    pygame.mixer.music.play(-1)
                                    self.firstTimePlay = False
                                pygame.mixer.music.unpause()
                            else:
                                pygame.mixer.music.pause()


                        #On side menu?
                        side_menu_button = self.menu.get_clicked(pos[0], pos[1])
                        if side_menu_button:
                            cost = self.menu.get_item_cost(side_menu_button)
                            if self.money >= cost:
                                self.money -= cost
                                self.add_tower(side_menu_button)


                        #On towers?
                        btn_clicked = None
                        if self.selected_tower:
                            btn_clicked = self.selected_tower.menu.get_clicked(pos[0], pos[1])
                            if btn_clicked:
                                if btn_clicked == "Upgrade":
                                    cost = self.selected_tower.get_upgrade_cost()
                                    print(cost)
                                    if self.money >= cost:
                                        self.money -= cost
                                        self.selected_tower.upgrade()
                                    else:
                                        self.displayMessage = "Not enough money to Upgrade"
                                        self.showInfoMessage = True
                                        self.setMessageInterval(3)
                        if not btn_clicked:
                            for tw in self.attack_towers:
                                if tw.click(pos[0], pos[1]):
                                    tw.selected = True
                                    self.selected_tower = tw
                                else:
                                    tw.selected = False
                            for tw in self.support_towers:
                                if tw.click(pos[0], pos[1]):
                                    tw.selected = True
                                    self.selected_tower = tw
                                else:
                                    tw.selected = False

            # loop through enemies
            if not(self.pause):
                to_del = []
                for en in self.enemies:
                    en.move()
                    if en.x < -15:
                        to_del.append(en)
                # delete all enemies of the screen
                for d in to_del:
                    self.lives -= 1
                    self.enemies.remove(d)

                for tw in self.attack_towers:
                    self.money += tw.attack(self.enemies)
                for tw in self.support_towers:
                    tw.support(self.attack_towers)

                if self.lives <= 0:
                    print("Game Over")
                    self.pause = True
                    self.displayMessage = "Game Over!!!"
                    self.showInfoMessage = True
                    self.setMessageInterval(5,False)
                    #self.game_run = False
            self.draw();


    def draw(self):
        self.win.blit(self.bg, (0, 0))
        # enemies
        for en in self.enemies:
            en.draw(self.win)
        # if self.moving_item:
        #     for t in self.attack_towers:
        #         pygame.draw.circle(self.win, (255, 0, 0), (t.x , t.y+ 45), 65, 1)
        #     for t in self.support_towers:
        #         pygame.draw.circle(self.win, (255, 0, 0), (t.x , t.y+ 45),  65, 1)
            #pygame.draw.circle(self.win, (255, 0, 0), (self.moving_item.x, self.moving_item.y + 45), 65, 1)
        # towers
        for tw in self.attack_towers:
            tw.draw(self.win)
            #pygame.draw.circle(self.win, (0, 255, 255), (tw.x,tw.y +45), 5, 0)
        for tw in self.support_towers:
            tw.draw(self.win)

        # lives
        text = self.lives_font.render(str(self.lives), 1, (0, 0, 0))
        start_x = self.width - lives_img.get_width() - 10
        for x in range(self.lives):
            self.win.blit(lives_img, (start_x - lives_img.get_width() * x + 5, 10))
        #self.win.blit(lives_img, (start_x, 10))
        #self.win.blit(text, (start_x - text.get_width() - 10, 10))

        # currency
        text = self.lives_font.render(str(self.money), 1, (255, 255, 255))
        money = pygame.transform.scale(star_img,(25,25))
        start_x = self.width - star_img.get_width() - 10
        self.win.blit(text, (start_x - text.get_width(), 28))
        self.win.blit(money, (start_x, 30))
        # redraw selected tower
        if self.selected_tower:
            self.selected_tower.draw(self.win)
        # draw moving tower
        if self.moving_item:
            self.moving_item.draw(self.win)

        #menu
        self.menu.draw(self.win)
        if self.showInfoMessage:
            msg = Message(self.displayMessage, (self.width*3/8),10,300)
            msg.draw(self.win)
        #buttons
        self.playPauseBtn.draw(self.win)
        self.soundBtn.draw(self.win)

        #wave
        self.win.blit(wave_bg, (10,10))
        text = self.lives_font.render("Wave "+str(self.wave +1),1,(255,255,255))
        self.win.blit(text,(10 + wave_bg.get_width()/2 - text.get_width()/2, 20))

        for dot in self.clicks:
            pygame.draw.circle(self.win, (255, 255, 0), dot, 10, 0)

        pygame.display.update()

    def add_tower(self, name):
        x,y = pygame.mouse.get_pos()
        name_list = ["buy_archer","buy_archer_2","buy_damage","buy_range"]
        object_list = [ArcherTowerLong(x,y), ArcherTowerShort(x,y),DamageTower(x,y),RangeTower(x,y)]
        try:
            tower = object_list[name_list.index(name)]
            self.moving_item = tower
        except Exception as e:
            print(str(e)+ " invalid name")

    def isOnMyPath(self, target_x, target_y):
        rad = 50
        target_y += 45
        for i, point in enumerate(path):
            if i < len(path) -1:
                x1 = path[i][0]
                y1 = path[i][1]
                x2 = path[i + 1][0]
                y2 = path[i + 1][1]
                m = (y2 - y1) / (x2 - x1)
                direction = -1 if (x2 < x1) else 1

                for x in range(x1, x2, direction):
                    y = m * (x - x1) + y1
                    #print(x, y)
                   # self.clicks.append((x,y))
                    # Compare radius of circle
                    # with distance of its center
                    # from given point
                    if ((target_x - x) * (target_x - x) +
                            (target_y - y) * (target_y - y) <= rad * rad):
                        return True
        return False


