import pygame, time

import engine
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

# Instantiate Game Objects
scoreBoard = ScoreBoard()
paddle = Paddle(WIDTH - BORDER * 3 - Paddle.WIDTH, HEIGHT * 0.5 - Paddle.HEIGHT * 0.5, paddleColour)
ball = Ball(WIDTH - Ball.RADIUS - 250, HEIGHT * 0.5, - velocity, velocity, ballColour)
liveBalls = [ball]

# I really tried.
gameState = GameState(
    pygame.display.set_mode((WIDTH, HEIGHT)),
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

while gameState.gameOn:

    render(gameState)

    if gameState.gameIsOver:
        renderScoreboard(gameState)
        time.sleep(2)
        pygame.event.wait()
        gameState.resetGame()

    gameState = engine.updateGameState(gameState)

pygame.quit()
