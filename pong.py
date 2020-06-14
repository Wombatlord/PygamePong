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


def current_time():
    return time.time()


def timeSince(when):
    return current_time() - when


def renderBackground():
    background = pygame.Surface(gameState.screen.get_size())
    background = background.convert()
    background.fill((0, 175, 0))
    gameState.screen.blit(background, (0, 0))


def renderWalls():
    global borderColour, WIDTH, BORDER, HEIGHT

    pygame.draw.rect(gameState.screen, borderColour, pygame.Rect((0, 0), (WIDTH, BORDER)))
    pygame.draw.rect(gameState.screen, borderColour, pygame.Rect((0, 0), (BORDER, HEIGHT)))
    pygame.draw.rect(gameState.screen, borderColour, pygame.Rect((0, HEIGHT - BORDER), (WIDTH, BORDER)))


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
    scoreBoard.show(gameState.screen)
    gameState.renderWalls()
    paddle.show(gameState.screen)

    if ball in balls:
        ball.show(gameState.screen)
    elif ball not in balls:
        scoreBoard.displayGameOver(gameState.screen)
        scoreBoard.reset()
        ball = Ball(WIDTH - Ball.RADIUS - 250, HEIGHT // 2, - velocity, 150, ballColour)
        balls.append(ball)
        pygame.display.flip()
        gameOver = False
        time.sleep(5)

    pygame.display.flip()
    ball.update(paddle, WIDTH, HEIGHT, BORDER, balls)
    paddle.update(BORDER, HEIGHT)

pygame.quit()
