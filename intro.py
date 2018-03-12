import pygame as pg
from pygame.locals import*
from time import sleep


#-------------------------------------------------------------------------------


def imgload(imgsrc):
    image = pg.image.load("images/intro_" + imgsrc + ".png").convert_alpha()
    return image


#-------------------------------------------------------------------------------



class SkipIntro(Exception):
    #This will be an ugly alternative to goto, found no easy way to
    #effectively skip through large chunks of code in Python
      pass




class Intro():

      def __init__(self):
          pg.init()

      #Window Options
          self.icon = pg.image.load("images/_nakio_.ico")
          pg.display.set_icon(self.icon)
          self.gameDisplay = pg.display.set_mode((768, 432))
          pg.display.set_caption("Nakio")


      #Loading Font Resources
          pg.font.init()
          self.font1 = pg.font.Font("font/DeeDooDah.ttf", 60)
          self.font2 = pg.font.Font("font/DeeDooDah.ttf", 24)


      #Loading Intro Resources
          self.phone = imgload("phoneoff")
          self.fx_buzz = pg.mixer.Sound("effects/fx_buzz.ogg")
          self.fx_type = pg.mixer.Sound("effects/fx_type.ogg")
          self.fx_pop = pg.mixer.Sound("effects/fx_pop.ogg")
          self.fx_hangup = pg.mixer.Sound("effects/fx_hangup.ogg")
          self.fx_run = pg.mixer.Sound("effects/fx_run.ogg")
          self.textbg = imgload("bg")
          self.face = imgload("chara")
          self.face2 = imgload("manager")
          self.skip = imgload("skip")


      #Creating Surfaces for fade-in and text rendering
          self.alpha_surface = pg.surface.Surface((768, 432))
          self.textsurface = pg.surface.Surface((60, 60))


      #Loading Intro Music
          pg.mixer.music.load("effects/mus_lullaby.ogg")
          pg.mixer.music.play(loops=-1)





      def chara_says(self, phrase, fx1):
      #Method to easily display the text bubble, player face, and text
      #Shares redundant code with manager_says.

      #Blitting all mentioned above, and updating the screen
          self.gameDisplay.blit (self.textbg, (0, 259))
          self.gameDisplay.blit (self.face, (10, 268))
          self.textsurface = pg.surface.Surface((768, 160))
          text1 = self.font2.render(phrase, False, (0,0,0))
          self.gameDisplay.blit (text1, (150, 280))

          pg.display.flip()

      #Playing sound effect for a time given in the attribute
          self.fx_type.play(-1)
          sleep(fx1)
          self.fx_type.stop()

      #Keyboard input
          pg.event.clear()
          pg.event.pump()
          keys = pg.key.get_pressed()

          while not (keys[K_RETURN]):
              pg.event.pump()
              keys = pg.key.get_pressed()
              if (keys[K_ESCAPE]):
                 raise SkipIntro

              sleep(0.1)



      def manager_says(self, phrase, fx1):
      #Method to easily display the text bubble, manager face, and text
      #Shares redundant code with chara_says.

      #Blitting all mentioned above, and updating the screen
          self.gameDisplay.blit (self.textbg, (0, 259))
          self.gameDisplay.blit (self.face2, (10, 268))
          text1 = self.font2.render(phrase, False, (0,0,0))
          self.gameDisplay.blit (text1, (150, 280))

          pg.display.flip()

      #Playing sound effect for a time given in the attribute
          self.fx_type.play(-1)
          sleep(fx1)
          self.fx_type.stop()

      #Keyboard input
          pg.event.clear()
          pg.event.pump()
          keys = pg.key.get_pressed()

          while not (keys[K_RETURN]):

              pg.event.pump()
              keys = pg.key.get_pressed()
              if (keys[K_ESCAPE]):
                 raise SkipIntro

              sleep(0.1)



      def auto(self):
      #Main method of Intro, huge chunk of code creating a video-like display
      #All other methods are called from here

          try:

          #Setting basic screen Surface
              self.alpha_surface.fill((0,0,0))
              self.alpha_surface.set_alpha(255)
              d_alpha = 255
              self.gameDisplay.fill((255,255,255))
              self.gameDisplay.blit(self.phone, (301, 20))

          #Declaring Z's coordinates as local variables
              Zxpos = [100, 200, 30]
              Zypos = [120, 250, 300]

              self.textsurface = self.font1.render("Z", False, (0,0,0))


          #Fade-in loop.
          #Surface alpha is gradually decreased
              while d_alpha >= 0:

                    #Handling keyboard input for skipping Intro
                    pg.event.pump()
                    keys = pg.key.get_pressed()
                    if(keys[K_ESCAPE]):
                        raise SkipIntro

                    #Setting basic screen Surface
                    self.gameDisplay.fill((255,255,255))
                    self.gameDisplay.blit(self.phone, (301, 20))

                    #d_alpha changing is used as a timer to display 'Z'
                    if d_alpha >= 252:
                       pass
                    elif d_alpha >= 210:
                       self.gameDisplay.blit (self.textsurface, (Zxpos[1], Zypos[1]))
                    elif d_alpha >= 168:
                       self.gameDisplay.blit(self.textsurface, (Zxpos[0], Zypos[0]))
                    elif d_alpha >= 126:
                       self.gameDisplay.blit(self.textsurface, (Zxpos[2], Zypos[2]))
                    elif d_alpha >= 84:
                       self.gameDisplay.blit(self.textsurface, (Zxpos[1], Zypos[1]))
                    elif d_alpha >= 42:
                       self.gameDisplay.blit(self.textsurface, (Zxpos[0], Zypos[0]))
                    else:
                       self.gameDisplay.blit (self.textsurface, (Zxpos[2], Zypos[2]))

                    d_alpha -= 0.08

                    #Filling screen with fade-in surface
                    self.alpha_surface.fill((0,0,0))
                    self.alpha_surface.set_alpha(d_alpha)
                    self.gameDisplay.blit(self.alpha_surface, (0,0))
                    self.gameDisplay.blit(self.skip, (0, 0))

                    pg.display.update()


              sleep(1.0)


            #Setting phone call screen Surface
              self.phone = imgload("phonecall")
              self.gameDisplay.fill((255,255,255))
              self.gameDisplay.blit(self.phone, (301, 20))

              pg.display.flip()


            #Phone buzz sequence
              pg.mixer.music.stop()
              self.fx_buzz.play()
              sleep(3.0)
              self.fx_buzz.play()
              sleep(3.0)
              self.fx_buzz.play()
              sleep(3.0)
              self.fx_buzz.play()
              sleep(0.5)
              pg.mixer.stop()
              self.fx_pop.play()
              sleep(0.5)


            #Resizing textsurface to make space for longer text
              self.textsurface = pg.surface.Surface((768, 160))


            #Dialogue sequence, input and calculation handled in called methods
              self.chara_says(". . .", 1)
              self.chara_says("Umm, hi!", 2)
              self.manager_says("Good morning. We planned an interview for 10\
               am.", 3)
              self.manager_says("Where are you?", 1)
              self.chara_says("Wha... Wasn't it 5 pm??", 2)
              self.manager_says(". . .", 1)
              self.fx_hangup.play()
              self.phone = imgload("phoneoff")
              self.gameDisplay.fill((255,255,255))
              self.gameDisplay.blit(self.phone, (301, 20))

              pg.display.flip()

              sleep(2.0)

              self.chara_says("DAMN!", 1)
              self.chara_says("I can make it! But I have to run!", 1)

              pg.mixer.stop()
              self.fx_run.play()

            #Fade-out
              self.alpha_surface.fill((0,0,0))
              self.alpha_surface.set_alpha(0)

              d_alpha = 0

              self.gameDisplay.fill((255,255,255))
              self.gameDisplay.blit(self.phone, (301, 20))

              while d_alpha <= 255:
                    d_alpha += 0.5
                    self.gameDisplay.fill((255,255,255))
                    self.gameDisplay.blit(self.phone, (301, 20))
                    self.alpha_surface.fill((0,0,0))
                    self.alpha_surface.set_alpha(d_alpha)
                    self.gameDisplay.blit(self.alpha_surface, (0,0))
                    pg.display.update()

            #When method terminates, code continues in nakyo.py, creating a
            #Game instance, and deleting this Intro instance


          except SkipIntro:
          #Code can terminate immaturely if above exception is raised
                 pass

