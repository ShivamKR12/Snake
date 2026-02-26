import pygame, sys

# define some constants to be used
WIDTH = 400 # in pixels
HEIGHT = 500 # also in pixels
FRAMERATE = 60 # so how many frames per second does the game runs

# initialize pygame
pygame.init()
# create a display surface aka a screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# create a clock object to control the amount of time the game updates
clock = pygame.time.Clock()
# create a test surface to draw soemthing
test_surface = pygame.Surface((100, 200))
# fill the test surface with the blue color
test_surface.fill((0, 0, 255))
# create a test rectangle using the pygame.Rect()
# the pyagem.Rect(x, y, w, h) needs 4 things : a X position, a Y position, a width and a height
# test_rect = pygame.Rect(100, 200, 100, 100)
# the benefit of making a rect using a surface is that you can change it's center
# we can set the center as center = (X, Y), where X and Y are the co-ordinates of the rectangle in pixxels
test_rect = test_surface.get_rect(center = (200, 250))
# or we can also do topright = (200, 250) to set the center of rectangle to it's topright corner, 
# that being at 200 down and 250 pixels right of the top left corner of the pygame window

# create a while loop to run the game logic
while True:
    # get all the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # fill the screen with a color so that we can differentiate it from the test surface
    # to do so, we can use fill() function of the pygame display window/surface
    # we can pass in the colors in 2 different ways :
    # 1. RGB tuple : aka a tuple with 3 values, (R,G,B), each going from 0 to 255, where 0 = 0% and 255 = 100%
    # 2. Color object : so we write pygame.Color('a predefined color name')
    screen.fill((175, 215, 70))

    # to draw a rectangle inside of thr pygame display surface/window, use pygame.draw.rect()
    # it takes 3 parameters : the surafce to draw the rectangle on, the color of the rectangle and the rectangle itself
    # pygame.draw.rect(screen, pygame.Color('red'), test_rect)

    # put our test suface on top of our screen display surface
    # blit = block image transfer
    # blit needs a surface and a X and a Y position inside a tuple
    # screen.blit(test_surface, (200, 250))
    # or we can just pass in a rect instead of the position tuple
    screen.blit(test_surface, test_rect)

    # update the display
    pygame.display.update()

    # set the framerate of the game window
    clock.tick(FRAMERATE)