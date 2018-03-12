import pygame as pg
pg.init()
from pygame.locals import*


#-------------------------------------------------------------------------------


def imgload(imgsrc):
#Basic Image Loading Function
    image = pg.image.load(imgsrc).convert_alpha()
    return image


#-------------------------------------------------------------------------------


class Obstacle (pg.sprite.Sprite):
    #This is the main Obstacle class. Everything in the game but menus and
    #the player is an Obstacle. To avoid clogging, once an Obstacle instance
    #leaves the screen, it's resources and references are released.
    #Background elements are not deleted, but repositioned in nakio.py
    #Obstacles are the subclass of pygame.Sprite



    def __init__(self, imgsrc, ypos, animated, speed, jumpspeed):
    #Obstacle attributes are given at creation in nakio.py


        pg.sprite.Sprite.__init__(self)


    #Declaring Movement Variables
        self.yvelo = 0
        self.xpos = 768
        self.ypos = ypos
        self.bottom = ypos
        self.speed = speed
        self.jumpspeed= jumpspeed
        self.jumping = False


    #Declaring Animation Variables
        self.tickcount = 0
        self.animspeed = 12
        self.animated = animated


    #Animated Obstacles have the self.images list with all the frames
        if ( animated ):
           self.index = 0
           self.images = []
           self.images.append(imgload(imgsrc + "_1.png"))
           self.images.append(imgload(imgsrc + "_2.png"))
           self.images.append(imgload(imgsrc + "_3.png"))
           self.image = self.images[1]
        else:
           self.image = imgload(imgsrc + ".png")
        self.rect = self.image.get_rect(topleft=(self.xpos, self.ypos))





    def update(self):
    #Basic Update Method, called from nakio.py
        self.rect = self.image.get_rect(topleft=(self.xpos, self.ypos))

        if ( self.animated ):
           self.anim()
        self.xpos -= self.speed


    #Handles Obstacle jump, if any
        if self.jumpspeed != 0:
            if ( self.jumping ):
                if self.yvelo > 0:
                    ymov = ( (self.yvelo*self.yvelo) )
                else:
                    ymov = -( (self.yvelo*self.yvelo) )

                self.ypos = self.ypos - ymov
                self.yvelo = self.yvelo - 0.3

                if self.ypos >= self.bottom:
                    self.ypos = self.bottom
                    self.jumping = False
                    self.yvelo = self.jumpspeed
            else:
                 self.jumping = True
        else:
             pass



    def anim(self):
    #Obstacle animation is handled here
        self.tickcount += 1
        if self.tickcount >= self.animspeed:
           self.tickcount = 0
           self.index += 1
           if self.index >= 3:
              self.index = 0
           self.image = self.images[self.index]



    def draw(self, surface):
    #Basic Display Method, called from nakio.py
        surface.blit(self.image, (self.xpos, self.ypos))



    def selfdestruct(self):
    #This method deletes the instance. Called from nakio.py
        self.kill()


