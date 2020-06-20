import pygame
import time

import engine
from pongEntities import ScoreBoard, Ball, Paddle, GameState
from renderer import initialise, render, renderScoreboard, blitBackground

pygame.init()
pygame.display.set_caption("PONGO!")
pygame.mouse.set_visible(0)

# Screen Variables
HEIGHT: int = 720
WIDTH: int = 1080
BORDER: int = 20

# Game Object Variables
borderColour: pygame.Color = pygame.Color("red")
backgroundColour: tuple = (0, 175, 0)
ballColour: pygame.Color = pygame.Color("black")
paddleColour: pygame.Color = pygame.Color("blue")

velocity: int = 300

# Instantiate Game Objects
scoreBoard: ScoreBoard = ScoreBoard()
paddle: Paddle = Paddle(WIDTH - BORDER * 3 - Paddle.WIDTH, HEIGHT * 0.5 - Paddle.HEIGHT * 0.5, paddleColour)
ball: Ball = Ball(WIDTH - Ball.RADIUS - 250, HEIGHT * 0.5, - velocity, velocity, ballColour)
liveBalls: list = [ball]

# Instantiate GameState and pass screen config parameters.
gameState: GameState = GameState(
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

# MAIN LOOP

while gameState.gameOn:

    render(gameState)

    if gameState.gameIsOver:
        renderScoreboard(gameState)
        time.sleep(2)
        pygame.event.wait()
        gameState.resetGame()

    gameState = engine.updateGameState(gameState)

pygame.quit()
