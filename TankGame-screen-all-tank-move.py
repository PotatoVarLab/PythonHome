#encoding=UTF-8
#先是游戏的界面

import pygame,sys,time
from pygame.locals import *
from random import randint

class TankMain():
    width=600
    height=500

    enemy_list=[]

    #从无到有是一种行为变化，定义对应的方法
    def startGame(self):
        #初始化pygame --就是这么做
        pygame.init()
        #生成游戏的窗口，
        screen = pygame.display.set_mode((TankMain.width,TankMain.height),0,32)
        pygame.display.set_caption("TankGame")

        #创建我方坦克
        my_tank=My_Tank(screen)
        #创造敌方坦克
        for i in range(1,6):
            TankMain.enemy_list.append(Enemy_Tank(screen))
        #开始持续显示动画内容
        while True:
            #没有这一句将出现重影现象
            screen.fill((0,0,0))
            #捕获退出事件
            self.get_event(my_tank)
            #我方坦克显示
            my_tank.display()
            my_tank.move()
            #敌方坦克显示和移动
            for enemy in TankMain.enemy_list:
                enemy.display()
                enemy.random_move()
            #帧更新
            time.sleep(0.1)
            pygame.display.update()


    #捕获按键事件
    def get_event(self,my_tank):
        for event in pygame.event.get():
            #退出按键
            if event.type == QUIT:
                self.stopGame()
            #移动
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    my_tank.direction="L"
                    my_tank.stop = False
                if event.key == K_RIGHT:
                    my_tank.direction="R"
                    my_tank.stop = False
                if event.key == K_UP:
                    my_tank.direction="U"
                    my_tank.stop = False
                if event.key == K_DOWN:
                    my_tank.direction="D"
                    my_tank.stop = False
            if event.type==KEYUP:
                if event.key==K_LEFT or event.key==K_RIGHT or event.key==K_DOWN or event.key==K_UP :
                    my_tank.stop=True
    #退出游戏界面
    def stopGame(self):
        sys.exit()

#所有动画元素的父类
class BaseItem(pygame.sprite.Sprite):
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen=screen

    def display(self):
        if self.live:
            self.image = self.images[self.direction]
            self.screen.blit(self.image, self.rect)

class Tank(BaseItem):
    width=50
    height=50

    def __init__(self,screen,left,top):
        super().__init__(screen)

        self.direction="U"
        self.speed=5
        self.images={}
        self.images['L']=pygame.image.load("images/tankL.gif")
        self.images['R']=pygame.image.load("images/tankR.gif")
        self.images['U']=pygame.image.load("images/tankU.gif")
        self.images['D']=pygame.image.load("images/tankD.gif")
        self.image=self.images[self.direction]
        self.rect=self.image.get_rect()
        self.rect.left=left
        self.rect.top=top
        self.live=True

    def move(self):
        if not self.stop:
            if self.direction == "L":
                if self.rect.left > 0:
                    self.rect.left-=self.speed
                else:
                    self.rect.left=0
            elif self.direction == "R":
                if self.rect.right < TankMain.width:
                    self.rect.right+=self.speed
                else:
                    self.rect.right=TankMain.width
            elif self.direction == "U":
                if self.rect.top > 0:
                    self.rect.top-=self.speed
                else:
                    self.rect.top=0
            elif self.direction == "D":
                if self.rect.bottom < TankMain.height:
                    self.rect.bottom+=self.speed
                else:
                    self.rect.bottom=TankMain.height

    def fire(self):
        pass

class My_Tank(Tank):
    def __init__(self,screen):
        super().__init__(screen,275,400)
        self.stop=True



class Enemy_Tank(Tank):
    def __init__(self,screen):
        super().__init__(screen,randint(1,5)*100,200)
        self.speed=4
        self.step=8
        self.get_random_direction()

    def get_random_direction(self):
        r=randint(0,4)
        if r==4:
            self.stop=True
        elif r==1:
            self.direction="L"
            self.stop=False
        elif r==2:
            self.direction="R"
            self.stop=False
        elif r==3:
            self.direction="U"
            self.stop=False
        elif r==0:
            self.direction="D"
            self.stop=False

    def random_move(self):
        if self.live:
            if self.step==0:
                self.get_random_direction()
                self.step=6
            else:
                self.move()
                self.step-=1

s = TankMain()
s.startGame()
