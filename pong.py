import pygame
import time
from pongEntities import ScoreBoard, Ball, Paddle, GameState

pygame.init()
pygame.display.set_caption("PONGO!")
pygame.mouse.set_visible(0)

# Screen Variables
HEIGHT = 720
WIDTH = 1080
BORDER = 20

# Game Object Variables
borderColour = pygame.Color("red")
backgroundColour = (0, 175, 0)
ballColour = pygame.Color("black")
paddleColour = pygame.Color("blue")

velocity = 300
scoreValue = 0

# Instantiate Game Objects
scoreBoard = ScoreBoard()
paddle = Paddle(WIDTH - BORDER * 3 - Paddle.WIDTH, HEIGHT * 0.5 - Paddle.HEIGHT * 0.5, paddleColour)
ball = Ball(WIDTH - Ball.RADIUS - 250, HEIGHT * 0.5, - velocity, velocity, ballColour)
liveBalls = []

# I really tried.
gameState = GameState(
    pygame.display.set_mode((WIDTH, HEIGHT)),
    ball,
    paddle,
    liveBalls,
    scoreBoard,
    WIDTH,
    HEIGHT,
    BORDER,
    borderColour,
    backgroundColour
)

# Game Loop Flags
gameOn = True
#print(pygame.font.get_fonts())

while gameOn:
    e = pygame.event.poll()
    keys = pygame.key.get_pressed()

    if e.type == pygame.QUIT:
        gameOn = False

    if e.type == pygame.KEYDOWN and keys[pygame.K_SPACE]:
        gameState.newBall()

    gameState.renderBackground()
    gameState.scoreBoard.show(gameState.screen)
    gameState.renderWalls()
    gameState.paddle.show(gameState.screen)

    if gameState.ball not in gameState.liveBalls:
        gameState.newBall()

    for gameState.ball in gameState.liveBalls:
        if gameState.ball.x < gameState.width:
            gameState.ball.show(gameState.screen)
            # print('live ball')

        if gameState.ball.x > gameState.width:
            #print('dead ball')
            gameState.ball.destroy(gameState.liveBalls)

    if len(gameState.liveBalls) == 0:
        gameState.gameOver()
        pygame.event.wait()
        # time.sleep(2)

    gameState.updateGameState()
    pygame.display.flip()

pygame.quit()

"""
if ball in gameState.liveBalls:
     print('okay')
     gameState.ball.show(gameState.screen)
elif ball not in gameState.liveBalls:
     gameState.scoreBoard.displayGameOver(gameState.screen)
     gameState.scoreBoard.reset()
     gameState.newBall(liveBalls)
     pygame.display.flip()
     gameOver = False
     time.sleep(2)
    
ball.update(gameState.paddle, WIDTH, HEIGHT, BORDER, gameState.liveBalls)
paddle.update(BORDER, HEIGHT)
"""


