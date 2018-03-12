import pygame as pg
from pygame.locals import*
from sys import exit
from time import sleep


#-------------------------------------------------------------------------------


def imgload(imgsrc):
#Basic Image Loading Function
    image = pg.image.load("images/menu_" + imgsrc + ".png").convert_alpha()
    return image


#-------------------------------------------------------------------------------


class MainMenu():
    #The first Class to be called at program execution.
    #Either leads to the creation of a Game instance (with a Level of 0),
    #or terminates the program.



      def __init__(self):
          pg.init()

      #Window Options
          self.icon = pg.image.load("images/_nakio_.ico")
          pg.display.set_icon(self.icon)
          self.gameDisplay = pg.display.set_mode((768, 432))
          pg.display.set_caption("Nakio")


      #Declaring Core Menu Variables
          self.userchoice = 0
          self.buttondelay = 0.3
          self.running = True



      #Loading Menu Resources
          self.newgame = imgload("new")
          self.newgame_pop = pg.transform.scale(self.newgame, (286, 80))
          self.controls = imgload("controls")
          self.controls_pop = pg.transform.scale(self.controls, (286, 80))
          self.quit = imgload("quit")
          self.quit_pop = pg.transform.scale(self.quit, (286, 80))
          self.title = imgload("title")


      #Loading Menu Music
          self.fx_pop = pg.mixer.Sound("effects/fx_pop.ogg")
          pg.mixer.music.load("effects/mus_mennyorszag.ogg")
          pg.mixer.music.play(loops=-1)





      def get_input(self):
      #Handles user keyboard input and QUIT events.
      #Shares some redundant code with the Game Class, I kept it separated for
      #better organization and ease of nesting

      #QUIT event handling
          quit = pg.event.poll()
          if quit.type == pg.QUIT:
            self.endgame()

      #Keyboard input
          pg.event.pump()
          keys = pg.key.get_pressed()

          if (keys[K_UP]):
             if self.userchoice <= 0:
                pass
             else:
                  self.userchoice -= 1
                  self.fx_pop.play()
             sleep(self.buttondelay)
          if (keys[K_DOWN]):
             if self.userchoice >= 2:
                pass
             else:
                  self.fx_pop.play()
                  self.userchoice += 1
             sleep(self.buttondelay)
          if (keys[K_RETURN]):
             if self.userchoice == 0:
                self.fx_pop.play()
                self.running = False
                sleep(self.buttondelay)
             elif self.userchoice == 1:
                  self.fx_pop.play()
                  self.controls_loop()
                  sleep(self.buttondelay)
             else:
                  self.fx_pop.play()
                  self.endgame()



      def controls_loop(self):
      #This is the Controls submenu loop, fairly straightforward

          ctrlsrunning = True
          ctrlscr = imgload("controlscr")
          sleep(self.buttondelay)

          while ( ctrlsrunning ):
                self.gameDisplay.blit(ctrlscr, (0, 0))
                pg.display.update()

          #Keyboard input
                pg.event.pump()
                keys = pg.key.get_pressed()
                if (keys[pg.K_ESCAPE]):
                   ctrlsrunning = False
                   pg.event.clear()
                   self.mm_loop()
                sleep(0.02)



      def scrupdate(self):
      #Basic Display Method, called from mm_loop.
      #Blitted images are loaded at Class initialization

          self.gameDisplay.fill((255,255,255))

          if self.userchoice == 0:
             self.gameDisplay.blit(self.newgame_pop, (221, 195))
             self.gameDisplay.blit(self.controls, (239, 270))
             self.gameDisplay.blit(self.quit, (239, 340))

          elif self.userchoice == 1:
             self.gameDisplay.blit(self.newgame, (239, 200))
             self.gameDisplay.blit(self.controls_pop, (221, 265))
             self.gameDisplay.blit(self.quit, (239, 340))

          else:
             self.gameDisplay.blit(self.newgame, (239, 200))
             self.gameDisplay.blit(self.controls, (239, 270))
             self.gameDisplay.blit(self.quit_pop, (221, 335))

          self.gameDisplay.blit(self.title, (44, 40))
          pg.display.update()



      def endgame(self):
      #De-initializes PyGame and terminates the program

          pg.quit()
          pg.mixer.quit()
          exit(0)



      def mm_loop(self):
      #The main Menu loop, all other Menu methods are called from here
      #If loop is broken, code continues at intro.py, creating an Intro instance,
      #and deleting this MainMenu instance

          while( self.running ):
            self.get_input()
            self.scrupdate()
            sleep(0.05)

