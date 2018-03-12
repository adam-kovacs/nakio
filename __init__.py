import pygame

pygame.init()

gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tinkering Yo")

movein = 0.02
xpos = 400
ypos = 300
clock = pygame.time.Clock()
pygame.key.set_repeat(1, 10)

#Main Loop
gameExit = False

while not gameExit:
        for keyPressed in pygame.event.get():
            if keyPressed.type == pygame.QUIT:
                gameExit = True
            if keyPressed.key == KEYDOWN:
                if keyPressed.




        pygame.draw.rect(gameDisplay, (255, 0, 0), [xpos, ypos, 10, 10])
        pygame.display.update()
        clock.tick(60)





#Game Exit
pygame.quit()