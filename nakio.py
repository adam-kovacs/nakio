#-------------------------------------------------------------------------------
# Name:        Nakio
#
# Author:      Adam Kovacs
# Version:     1.1
#
# Created:     08/03/2018
# Copyright:   ---
# Licence:     ---
#-------------------------------------------------------------------------------


from pygame.locals import*
import pygame as pg
import random
from sys import exit
from time import sleep

#.py files in same directory
from player import Player
from obstacle import Obstacle
from menu import MainMenu
from intro import Intro
from obst_type import streetlist, obslist, movelist


#-------------------------------------------------------------------------------


def MainMenuStart():
    #Code below makes the first MainMenu instance work
    #and delete Game instances if a new MainMenu is created
    try:
        del(CurrentRun)
    except NameError:
           pass
    global MainMenu

    #Starts Main Menu loop in file menu.py
    MenuInstance = MainMenu()
    MenuInstance.mm_loop()
    IntroStart(MenuInstance)


def IntroStart(ParentMenu):
    #Deletes previous MainMenu instance to avoid redundancy
    del(ParentMenu)
    global CurrentIntro

    #Starts Intro loop in file menu.py
    CurrentIntro = Intro()
    CurrentIntro.auto()
    GameStart(CurrentIntro)


def GameStart(Parent):
    #Deletes previous Class instance (Game or Intro instance)
    del(Parent)
    global CurrentRun
    CurrentRun = Game(level)
    CurrentRun.mainloop()


#-------------------------------------------------------------------------------



class Game():
      #This is the main Game class
      #Main objective is to, get user input and create various Class instances.
      #Also, temporary screens, and some of the game logic is handled here



    def __init__(self, level):
        pg.init()
        self.running = True

    #Window Options
        self.icon = pg.image.load("images/_nakio_.ico")
        pg.display.set_icon(self.icon)
        self.gameDisplay = pg.display.set_mode((768, 432))
        pg.display.set_caption("Nakio")


    #Declaring Core Game Variables
        self.ObstGr = pg.sprite.Group()              #Obstacle Sprite Group
        self.BgGr = pg.sprite.Group()                #Background Sprite Group

        self.health = 3
        self.levelprogress = 0
        self.ghost_tick = 0
        self.ghost_time = 300
        self.bginit = True
        self.obstacle = None                         #This later becomes Object
        self.running = True


    #Loading Game Resources
        self.health_pic = pg.image.load("images/health.png").convert_alpha()
        self.go_title = pg.image.load("images/menu_gameover.png").convert_alpha()
        self.go_retry = pg.image.load("images/menu_gameover_retry.png").convert_alpha()
        self.lvl_comp = pg.image.load("images/menu_lvlcomp.png").convert_alpha()
        self.lvl_cont = pg.image.load("images/menu_lvlcont.png").convert_alpha()
        self.game_win = pg.image.load("images/menu_gamewin.png").convert_alpha()
        self.game_restart = pg.image.load("images/menu_gamerestart.png").convert_alpha()
        self.fx_collision = pg.mixer.Sound("effects/fx_collision.ogg")


    #Changing Game variables and loading resources according to Level
        if int(level / 2) == 0:
           self.slolist = movelist[0]
           self.carlist = movelist[1]
           self.bg = ("images/bgloop_1")
           self.house = ("images/houseloop_1")
        elif int(level / 2) == 1:
           self.slolist = movelist[2]
           self.carlist = movelist[3]
           self.bg = ("images/bgloop_2")
           self.house = ("images/houseloop_2")
        elif int(level / 2) == 2:
           self.slolist = movelist[4]
           self.carlist = movelist[5]
           self.bg = ("images/bgloop_2")
           self.house = ("images/houseloop_3")
        else:
             #Game Victory is called at the 'lvl.complete' method by default
             #This only stands here as a failsafe
             self.game_victory()


    #Declaring Tick Variables
    #These handle how often various Obstacle instances are created
        self.placefreq = 2 + level * 2
        self.obsTick = 0
        self.obsNext = 800
        self.sloTick = 0
        self.sloNext = 400
        self.carTick = 0
        self.carNext = 600

    #Loading Game Music
        pg.mixer.music.load("effects/mus_apuveddmeg.ogg")
        pg.mixer.music.play(-1)

    #Creating Player instance
        self.player = Player()





    def get_input(self):
    #Handles user keyboard input and QUIT events

    #QUIT event handling
        quit = pg.event.poll()
        if quit.type == pg.QUIT:
            self.running = False

    #Keyboard input
        pg.event.pump()
        keys = pg.key.get_pressed()

    #Player movement is calculated in player.py
        if (keys[K_RIGHT]):
            self.player.moveRight()

        if (keys[K_LEFT]):
            self.player.moveLeft()

        if (keys[K_UP]):
           if not ( self.player.jumping ):
              self.player.jumping = True

        if (keys[K_ESCAPE]):
            self._running = False
            pg.event.clear()
            MainMenuStart()



    def scrupdate(self):
    #Main updating and displaying routine
    #Also sets blitting order, which creates the illusion of layers

        #0. Fill background with white color (normally not visible)
        self.gameDisplay.fill((210,255,255))

        #1. Update and draw background elements
        self.bgscroll()

        #2. Update and draw Player sprite
        self.player.update()
        self.player.draw(self.gameDisplay)

        #3. Place new Obstacle instances
        #---If level already ended, no more Obstacles are placed
        if self.levelprogress <= 16:
           self.obstPlacement()

        #4. Update and draw Obstacles and health
        self.obstUpdate()
        self.health_update()

        #5. Update all existing surfaces
        pg.display.flip()



    def obstUpdate(self):
    #Handles Obstacle Updating
        for item in self.ObstGr:

        #Obstacle movement and display is handled in obstacle.py
            item.update()
            item.draw(self.gameDisplay)


        #Collision checking and deleting Obstacles which leave the screen
        #---If level already ended, Collision check is passed
            if (item.xpos + item.rect[2]) <= 0:
               item.selfdestruct()
            if self.levelprogress <= 16:
                if self.player.ifghost == False:
                   if pg.sprite.collide_rect(self.player, item) == True:
                      self.fx_collision.play()
                      self.health -= 1
                      self.player.ifghost = True
                elif self.ghost_tick >= self.ghost_time:
                     self.ghost_tick = 0
                     self.player.ifghost = False
                else:
                     self.ghost_tick += 1



    def obstPlacement(self):
    #Basic Obstacle Placement Method

    #There are three types of Obstacles: Obstacles, Slow, and Cars
    #Parameteres are imported from obst_type.py
    #Obstacle placement becomes more frequent as level progresses

        self.obsTick += 1
        if self.obsTick >= self.obsNext:
           self.obsTick = 0
           self.obsNext = self.obsNext * random.randint((100 - self.placefreq), 100) / 100
           ot = random.choice(obslist)
           self.obstacle = Obstacle(ot[0], ot[1], ot[2], ot[3], ot[4])
           self.ObstGr.add(self.obstacle)
        self.sloTick += 1

        if self.sloTick >= self.sloNext:
           self.sloTick = 0
           self.sloNext = self.sloNext * random.randint((100 - self.placefreq), 100) / 100
           ot = random.choice(self.slolist)
           self.obstacle = Obstacle(ot[0], ot[1], ot[2], ot[3], ot[4])
           self.ObstGr.add(self.obstacle)
        self.carTick += 1

        if self.carTick >= self.carNext:
           self.carTick = 0
           self.carNext = self.carNext * random.randint((100 - self.placefreq), 100) / 100
           ot = random.choice(self.carlist)
           self.obstacle = Obstacle(ot[0], ot[1], ot[2], ot[3], ot[4])
           self.ObstGr.add(self.obstacle)



    def bgscroll(self):
    #Handles Background Updating

    #Backgrounds are special Obstacle instances with no Collision check
    #Background (re)placement, updating, and draw function calling
    #is handled here, unlike other Obstacle instances

        if ( self.bginit ):
        #Initial Background placement, runs only when Game instance starts
           sl = random.choice(streetlist)
           street1 = Obstacle(sl[0], sl[1], sl[2], sl[3], sl[4])
           bg1 = Obstacle(self.bg, -21, False, 1, 0)
           house1 = Obstacle(self.house, 0, False, 1.5, 0)
           sl = random.choice(streetlist)
           street2 = Obstacle(sl[0], sl[1], sl[2], sl[3], sl[4])
           bg2 = Obstacle(self.bg, -21, False, 1, 0)
           house2 = Obstacle(self.house, 0, False, 1.5, 0)

           self.BgGr.add(street1, street2, bg1, bg2, house1, house2)

        #Declaring local position variables
           street1.xpos = 0
           bg1.xpos = 0
           house1.xpos = 0
           street2.xpos= 1300
           bg2.xpos = 1000
           house2.xpos = 1000

           self.bginit = False


        for item in self.BgGr:
        #After initial placement, only repositioning and drawing takes place
        #Level progress calculation is based on Background instances which
        #left the screen
            item.update()
            if item.xpos <= -(item.rect[2]):
               item.xpos = item.rect[2]
               self.levelprogress += 1
            item.draw(self.gameDisplay)



    def health_update(self):
    #Updates and draws player health, pretty straightforward
        health_xpos = 10

        for n in range (0, self.health):
            self.gameDisplay.blit(self.health_pic, (health_xpos, 10))
            health_xpos += 50
        if self.health < 0:
           self.running = False
           self.game_over()



    def game_over(self):
    #Temporary Game Over screen and loop
    #Either creates a MainMenu or a Game instance (with same Level)

        go_running = True
        self.running = False

        while ( go_running ):

        #QUIT even handling
            quit = pg.event.poll()
            if quit.type == pg.QUIT:
               self.endgame()

            self.gameDisplay.fill((0,0,0))
            self.gameDisplay.blit(self.go_title, (44, 40))
            self.gameDisplay.blit(self.go_retry, (44, 300))
            pg.display.update()

        #Keyboard input
            pg.event.pump()
            keys = pg.key.get_pressed()
            if (keys[pg.K_ESCAPE]):
               go_running = False
               MainMenuStart()
            if (keys[pg.K_RETURN]):
               GameStart(CurrentRun)

            sleep(0.015)



    def lvl_complete(self):
    #Temporary Level Complete screen and loop
    #Either creates a MainMenu, a Game instance (with Level + 1), or
    #calls game_victory method, which ends the game session

        self.running = False
        lvl_running = True

        global level
        if level >= 5:
           self.game_victory()

        while ( lvl_running ):

        #QUIT even handling
            quit = pg.event.poll()
            if quit.type == pg.QUIT:
               self.endgame()
            self.running = False

            self.gameDisplay.fill((0,0,0))
            self.gameDisplay.blit(self.lvl_comp, (44, 40))
            self.gameDisplay.blit(self.lvl_cont, (44, 300))
            pg.display.update()

        #Keyboard input
            pg.event.pump()
            keys = pg.key.get_pressed()
            if (keys[pg.K_ESCAPE]):
               go_running = False
               MainMenuStart()
            if (keys[pg.K_RETURN]):
               level += 1
               GameStart(CurrentRun)

            sleep(0.015)



    def game_victory(self):
    #Temporary Game Victory screen and loop
    #Ends game session and creates a MainMenu instance, setting level to 0

        self.running = False
        win_running = True

        while ( win_running ):

        #QUIT even handling
            quit = pg.event.poll()
            if quit.type == pg.QUIT:
               self.endgame()


            self.gameDisplay.fill((0,0,0))
            self.gameDisplay.blit(self.game_win, (44, 40))
            self.gameDisplay.blit(self.game_restart, (44, 250))
            pg.display.update()

        #Keyboard input
            pg.event.pump()
            keys = pg.key.get_pressed()
            if (keys[pg.K_ESCAPE]) or (keys[pg.K_RETURN]):
               global level
               level == 0
               go_running = False
               MainMenuStart()

            sleep(0.015)



    def endgame(self):
    #De-initializes PyGame and terminates the program

        pg.quit()
        exit(0)



    def mainloop(self):
    #The main Game loop, all other methods are first called from here
    #If level already ended, get_input is passed, and transition to
    #lvl_complete begins
        while( self.running ):

               if self.levelprogress <= 16:
                   self.get_input()
               else:
                    self.player.moveRight()
                    if self.player.xpos >= 726:
                       pg.mixer.music.stop()
                       pg.mixer.music.load("effects/mus_victory.ogg")
                       pg.mixer.music.play()
                       self.lvl_complete()

               self.scrupdate()
               sleep(0.01)

    #end_game method is usually called directly, this is only a failsafe
        self.endgame()



#-------------------------------------------------------------------------------


#PROGRAM EXECUTION STARTS HERE

if __name__ == "__main__" :

   global level
   level = 0
   MenuInstance = 0
   MainMenuStart()