import pygame as pg
pg.init()
from time import sleep


#-------------------------------------------------------------------------------


def imgload(imgsrc):
#Basic Image Loading Function
    image = pg.image.load(imgsrc).convert_alpha()
    return image


#-------------------------------------------------------------------------------


class Player (pg.sprite.Sprite):
    #This Class handles the player character and the player character alone.
    #There is never more than one instance of this Class at any given time.
    #Shares some redundant code with the Obstacle Class, but I decided to
    #keep it separated for better organization.
    #Player instances are a subclass of pygame.Sprite




    def __init__(self):
        pg.sprite.Sprite.__init__(self)


    #Declaring Movement Variables
        self.bottom = 307
        self.jumpspeed = 4.5
        self.startxpos = 16
        self.yvelo = self.jumpspeed
        self.xpos = self.startxpos
        self.ypos = self.bottom
        self.speed = 5
        self.jumping = False
        self.ifghost = False


    #Declaring Animation Variables
        self.animspeed = 8
        self.tickcount = 0
        self.index = 0


    #Player instances have the self.images list with all the frames
        self.images = []
        self.images.append(imgload("images/pc_1.png"))
        self.images.append(imgload("images/pc_2.png"))
        self.images.append(imgload("images/pc_3.png"))
        self.image = self.images[self.index]

    #At Collision, Player becomes ghost, passing Obstacles, being tranlucent
    #Instead of built-in PyGame code, I used separate translucent images
        self.ghost_images = []
        self.ghost_images.append(imgload("images/pcghost_1.png"))
        self.ghost_images.append(imgload("images/pcghost_2.png"))
        self.ghost_images.append(imgload("images/pcghost_3.png"))

        self.rect = self.image.get_rect(topleft=(self.xpos, self.ypos))





    def moveRight(self):
        if self.xpos < 728:
           self.xpos = self.xpos + self.speed
        else:
             pass



    def moveLeft(self):
        if self.xpos > 8:
           self.xpos = self.xpos - self.speed
        else:
             pass



    def update(self):
    #Basic Update Method, called from nakio.py
        self.anim()
        self.rect = self.image.get_rect(topleft=(self.xpos, self.ypos))

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



    def anim(self):
    #Player animation is handled here
       self.tickcount += 1
       if self.tickcount >= self.animspeed:
          self.tickcount = 0
          self.index += 1
          if self.index >= 3:
             self.index = 0
       if ( self.ifghost ):
          self.image = self.ghost_images[self.index]
       else:
            self.image = self.images[self.index]



    def draw(self, surface):
    #Basic Display Method, called from nakio.py
       surface.blit(self.image, (self.xpos, self.ypos))








