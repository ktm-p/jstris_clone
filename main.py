# IMPORTS
import pygame, sys, random
from game import Game

# RANDOM SEED
random.seed(690)

# CONSTANTS
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

def is_fullscreen():
    return (screen.get_flags() & pygame.FULLSCREEN)

# INITIALIZATION
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("A Tetris Clone")
clock = pygame.time.Clock()
game = Game()

# AUTOMATIC BLOCK FALL
TIMEREVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMEREVENT, 900)

# HELD DOWN KEYS
moveLeft = False
moveRight = False
moveDown = False

# MAIN GAMEPLAY LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # if (event.type == pygame.KEYDOWN and event.key == pygame.K_f):
        #     if is_fullscreen():
        #         pygame.display.set_mode(SIZE)
        #     else:
        #         pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
        if event.type == TIMEREVENT:
            game.move_down()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moveLeft = True
            if event.key == pygame.K_RIGHT:
                moveRight = True
            if event.key == pygame.K_DOWN:
                moveDown = True
            if event.key == pygame.K_UP:
                game.rotate_up()
            if event.key == pygame.K_z:
                game.rotate_down()
            if event.key == pygame.K_SPACE:
                game.hard_drop()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moveLeft = False
            if event.key == pygame.K_RIGHT:
                moveRight = False
            if event.key == pygame.K_DOWN:
                moveDown = False

    if moveLeft:
        game.move_left()
        pygame.time.delay(50)

    if moveRight:
        game.move_right()
        pygame.time.delay(50)

    if moveDown:
        game.move_down()
        pygame.time.delay(10)
    
    screen.fill((99, 99, 99))
    game.draw(screen)

    pygame.display.update()
    clock.tick(60)
    