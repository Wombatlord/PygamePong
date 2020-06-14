import pygame
import time
from pongEntities import ScoreBoard, Ball, Paddle, GameState

pygame.init()
pygame.display.set_caption("PONGO!")
pygame.mouse.set_visible(0)

# Screen Variables
HEIGHT = 600
WIDTH = 1200
BORDER = 20


# Game Object Variables
borderColour = pygame.Color("red")
ballColour = pygame.Color("black")
paddleColour = pygame.Color("blue")

velocity = 300
scoreValue = 0


# Instantiate Game Objects
scoreBoard = ScoreBoard()
paddle = Paddle(WIDTH - BORDER * 3 - Paddle.WIDTH, HEIGHT // 2 - Paddle.HEIGHT // 2, paddleColour)
ball = Ball(WIDTH - Ball.RADIUS - 250, HEIGHT // 2, - velocity, velocity, ballColour)
balls = [ball]

# I really tried.
gameState = GameState(pygame.display.set_mode((WIDTH, HEIGHT)),
                      ball,
                      paddle,
                      scoreBoard,
                      WIDTH,
                      HEIGHT,
                      BORDER,
                      borderColour
                      )

# Game Loop Flags
gameOn = True

while gameOn:
    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        gameOn = False

    gameState.renderBackground()
    gameState.scoreBoard.show(gameState.screen)
    gameState.renderWalls()
    gameState.paddle.show(gameState.screen)

    if ball in balls:
        ball.show(gameState.screen)
    elif ball not in balls:
        gameState.scoreBoard.displayGameOver(gameState.screen)
        gameState.scoreBoard.reset()
        ball = Ball(WIDTH - Ball.RADIUS - 250, HEIGHT // 2, - velocity, 150, ballColour)
        balls.append(ball)
        pygame.display.flip()
        gameOver = False
        time.sleep(5)

    pygame.display.flip()
    ball.update(paddle, WIDTH, HEIGHT, BORDER, balls)
    gameState.paddle.update(BORDER, HEIGHT)

pygame.quit()
