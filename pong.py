import pygame
import time

import engine
from configReader import reader
from pongEntities import ScoreBoard, Ball, Paddle, GameState
from renderer import initialise, render, renderScoreboard, blitBackground

pygame.init()
pygame.display.set_caption("PONGO!")
pygame.mouse.set_visible(0)

configPaths = [
    'config/config.yml',
    'config/config.local.yml',
]

config = reader.get(configPaths)

# Screen Variables
HEIGHT: int = config["display"]["resolution"]["height"]
WIDTH: int = config["display"]["resolution"]["width"]
BORDER: int = config["gameplay"]["border"]

# Game Object Variables
borderColour: pygame.Color = pygame.Color(
    config["display"]["colours"]["border"]
)
backgroundColour: tuple = config["display"]["colours"]["background"]
ballColour: pygame.Color = pygame.Color(
    config["display"]["colours"]["ball"]
)
paddleColour: pygame.Color = pygame.Color(
    config["display"]["colours"]["paddle"]
)

velocity: list = config["gameplay"]["balls"][0]["velocity"]

# Instantiate Game Objects
scoreBoard: ScoreBoard = ScoreBoard()
paddle: Paddle = Paddle(WIDTH - BORDER * 3 - Paddle.WIDTH, HEIGHT * 0.5 - Paddle.HEIGHT * 0.5, paddleColour)
paddle.height = config["gameplay"]["paddle"]["height"]
paddle.width = config["gameplay"]["paddle"]["width"]
ball: Ball = Ball(WIDTH - Ball.RADIUS - 250, HEIGHT * 0.5, velocity[0], velocity[1], ballColour)
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
