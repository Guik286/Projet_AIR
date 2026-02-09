# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    font = pygame.font.Font(None, 30)
    text = font.render(f'Temps: {clock.tick(60)/1000}', True, (0, 0, 0))
    pygame.draw.rect(screen,pygame.Color("Black"),(100,100,200,50))
    screen.blit(text,(0,0))

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()


    