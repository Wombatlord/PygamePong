import pygame
from pongEntities import ScoreBoard, Ball, Paddle, GameState
from renderer import initialise, render, renderScoreboard

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

initialise(
    backgroundColour,
    borderColour,
    (WIDTH, HEIGHT),
    BORDER
)

# Game Loop Flags
gameOn = True

while gameOn:
    e = pygame.event.poll()
    keys = pygame.key.get_pressed()

    if e.type == pygame.QUIT:
        gameOn = False

    if e.type == pygame.KEYDOWN and keys[pygame.K_SPACE]:
        gameState.newBall()

    render(gameState)

    if gameState.ball not in gameState.liveBalls:
        gameState.newBall()

    for gameState.ball in gameState.liveBalls:
        if gameState.ball.x > gameState.width:
            gameState.ball.destroy(gameState.liveBalls)

    if len(gameState.liveBalls) == 0:
        print('end')
        gameState.gameOver()
        renderScoreboard(gameState)
        pygame.event.wait()
        gameState.resetScore()
        gameState.gameIsOver = False

    gameState.updateGameState()
    pygame.display.flip()

pygame.quit()


