import pygame, sys, random
from pygame.math import Vector2
import os
import sys


# define some constants to be used
CELL_SIZE = 30 # in pixels
CELL_NUMBER = 20 # also in pixels
FRAMERATE = 60 # so how many frames per second does the game runs


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class SNAKE:
    def __init__(self):
        # the initial body of the snake that the player will see when the game starts
        # we store it is Vector2s because it's easier to do maths with them
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        # the direction is an unit vector that represents the direction in which the snake's head is facing
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load(resource_path('Graphics/head_up.png')).convert_alpha()
        self.head_down = pygame.image.load(resource_path('Graphics/head_down.png')).convert_alpha()
        self.head_right = pygame.image.load(resource_path('Graphics/head_right.png')).convert_alpha()
        self.head_left = pygame.image.load(resource_path('Graphics/head_left.png')).convert_alpha()

        self.tail_up = pygame.image.load(resource_path('Graphics/tail_up.png')).convert_alpha()
        self.tail_down = pygame.image.load(resource_path('Graphics/tail_down.png')).convert_alpha()
        self.tail_right = pygame.image.load(resource_path('Graphics/tail_right.png')).convert_alpha()
        self.tail_left = pygame.image.load(resource_path('Graphics/tail_left.png')).convert_alpha()

        self.body_vertical = pygame.image.load(resource_path('Graphics/body_vertical.png')).convert_alpha()
        self.body_horizontal = pygame.image.load(resource_path('Graphics/body_horizontal.png')).convert_alpha()

        self.body_tr = pygame.image.load(resource_path('Graphics/body_tr.png')).convert_alpha()
        self.body_tl = pygame.image.load(resource_path('Graphics/body_tl.png')).convert_alpha()
        self.body_br = pygame.image.load(resource_path('Graphics/body_br.png')).convert_alpha()
        self.body_bl = pygame.image.load(resource_path('Graphics/body_bl.png')).convert_alpha()

        self.crunch_sound = pygame.mixer.Sound(resource_path('Sound/crunch.wav'))
    
    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            # create a rectangle
            # we are multiplying the block's X and Y position with CELL_SIZE and then covering it with int()
            # because we want the snake's body to always move in grid pattern
            x_position = int(block.x * CELL_SIZE)
            y_position = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_position, y_position, CELL_SIZE, CELL_SIZE)
            
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)
    
    def move_snake(self):
        # the head is moved to a new block
        # the block before the head gets the position where the head used to be
        # each block is moved to the position of the block that used to be before it
        # this deletes the last block
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
    
    def add_block(self):
        self.new_block = True
    
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down
    
    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def play_crunch_sound(self):
        self.crunch_sound.play( )

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class FRUIT:
    def __init__(self):
        self.randomize()
    
    def draw_fruit(self):
        # create a rectangle
        fruit_rect = pygame.Rect(int(self.position.x * CELL_SIZE), int(self.position.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        screen.blit(apple, fruit_rect)
        # draw the rectangle
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rect)
    
    def randomize(self):
        # create a X and Y position
        # they should be random, but inside the window
        # the - 1 is because randint is inclusive, so if the number comes out to be CELL_NUMBER,
        # then the fruit will be outside of the window
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.position = Vector2(self.x, self.y)


class MAIN:
    def __init__(self):
        # create an instance of the snake class
        self.snake = SNAKE()
        # create an instance of the fruit class
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
    
    def draw_elements(self):
        self.draw_grass()
        self.snake.draw_snake()
        self.fruit.draw_fruit()
        self.draw_score()
    
    def check_collision(self):
        if self.fruit.position == self.snake.body[0]:
            # reposition the fruit
            self.fruit.randomize()
            # add another block to the snake
            self.snake.add_block()
            # play the crunch sound
            self.snake.play_crunch_sound()
        
        # if the fruit spawns on top of the snake's body, then respawn it somewhere else
        for block in self.snake.body[1:]:
            if block == self.fruit.position:
                self.fruit.randomize()
    
    def check_fail(self):
        # check if snake is outside of screen
        if not 0 <=self.snake.body[0].x < CELL_NUMBER or not 0 <=self.snake.body[0].y < CELL_NUMBER:
            self.game_over()
        # check if snake hit itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    
    def game_over(self):
        self.snake.reset()
    
    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(CELL_NUMBER):
            if row % 2 == 0:
                for column in range(CELL_NUMBER):
                    if column % 2 == 0:
                        grass_rect = pygame.Rect(column * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for column in range(CELL_NUMBER):
                    if column % 2 != 0:
                        grass_rect = pygame.Rect(column * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        # the score to be shown is simply be the length of the body of the snake
        # but since we initially have 3 elements in our body list, we need to subtract by 3
        score_text = str(len(self.snake.body) - 3)
        # then we need to call the render() method from the loaded font to get the surface to draw the font on
        # it takes 3 agruments : 1. the text to draw, 2. bool if we want Anti-Alias or not, 3. the color of the text
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        # the X position of the text. CELL_SIZE * CELL_NUMBER means it's at the bottom right corner of the screen.
        # the - 60 means it's 60 pixels to the left of the window border
        score_x = int(CELL_SIZE * CELL_NUMBER - 60)
        # the Y position of the text. CELL_SIZE * CELL_NUMBER means it's at the bottom right corner of the screen.
        # the - 40 means it's 40 pixels up of the window border
        score_y = int(CELL_SIZE * CELL_NUMBER - 40)
        # the score rect will be placed 60 pixels left and 40 pixels up of the window border
        score_rect = score_surface.get_rect(center =(score_x, score_y))
        # we place the apple rect left of the score rect and centered the same as the score rect
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        # add a background behind the score and the apple
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6, apple_rect.height)
        # draw the background
        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        # draw the text on to the surface
        screen.blit(score_surface, score_rect)
        # draw the apple left of our scroe
        screen.blit(apple, apple_rect)
        # draw a small thin frame around the background to make it pop-out a bit more
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)


# preinitialize the pygame mixer so that the crunch sound play at the right timer
# pygame.mixer.pre_init(4410, -16, 2, 512) # BUG : preinitialization is messing with the sounds !!!
# initialize pygame
pygame.init()
# set the title of the pygame window to be the name of the game
pygame.display.set_caption("Snake")
# create a display surface aka a screen
screen = pygame.display.set_mode((CELL_NUMBER * CELL_SIZE, CELL_NUMBER * CELL_SIZE))
# create a clock object to control the amount of time the game updates
clock = pygame.time.Clock()
apple = pygame.image.load(resource_path('Graphics/apple.png')).convert_alpha()
game_font = pygame.font.Font(resource_path('Font/PoetsenOne-Regular.ttf'), 25)
# set the apple as the icon for the pygame window
pygame.display.set_icon(apple)


SCREEN_UPDATE = pygame.USEREVENT # a user defined pygame event
# set the timer to update the screen every 150 milliseconds
pygame.time.set_timer(SCREEN_UPDATE, 150)


# create an instance of the main class
main_game = MAIN()


# create a while loop to run the game logic
while True:
    # get all the events
    for event in pygame.event.get():
        # if we want to quit the game by pressing the X icon on the top right corner of the pyagme window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() # sys.exit() is because pygame.quit() may sometimes fail or not completely work !
        if event.type == SCREEN_UPDATE:
            main_game.update()
        # if the event is a keyboard button press
        if event.type == pygame.KEYDOWN:
            # if the button pressed is the up arrow key
            if event.key == pygame.K_UP:
                # check if we are not moving downward, otherwise it's impossible to move up when going down
                if main_game.snake.direction.y != 1:
                    # change the snake's direction to be up
                    main_game.snake.direction = Vector2(0, -1)
            # if the button pressed is the right arrow key
            if event.key == pygame.K_RIGHT:
                # check if we are not moving leftward, otherwise it's impossible to move right when going left
                if main_game.snake.direction.x != -1:
                    # change the snake's direction to be right
                    main_game.snake.direction = Vector2(1, 0)
            # if the button pressed is the down arrow key
            if event.key == pygame.K_DOWN:
                # check if we are not moving upward, otherwise it's impossible to move down when going up
                if main_game.snake.direction.y != -1:
                    # change the snake's direction to be down
                    main_game.snake.direction = Vector2(0, 1)
            # if the button pressed is the left arrow key
            if event.key == pygame.K_LEFT:
                # check if we are not moving rightward, otherwise it's impossible to move left when going right
                if main_game.snake.direction.x != 1:
                    # change the snake's direction to be left
                    main_game.snake.direction = Vector2(-1, 0)
    
    # fill the screen with a color so that we can differentiate it from the rest of the objects
    # to do so, we can use fill() function of the pygame display window/surface
    # we can pass in the colors in 2 different ways :
    # 1. RGB tuple : aka a tuple with 3 values, (R,G,B), each going from 0 to 255, where 0 = 0% and 255 = 100%
    # 2. Color object : so we write pygame.Color('a predefined color name')
    screen.fill((175, 215, 70))

    # draw all the elements on to the screen
    main_game.draw_elements()

    # update the display
    pygame.display.update()

    # set the framerate of the game window
    clock.tick(FRAMERATE)
