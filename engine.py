import math
import random
import time

import pygame

from pongEntities import GameState, Ball, Paddle
from vector import Vector


def current_time():
    """
    Returns the current time.
    """
    return time.time()


def timeSince(when):
    """
    Returns the value of current_time minus a given value.
    """
    return current_time() - when


def updateGameState(gameState: GameState) -> GameState:
    """
    Checks event queue for user input.
    Tracks position and collision of each ball.
    Updates total score value based on return value from each ball.
    Tracks paddle and collision with walls.
    """
    e = pygame.event.poll()
    keys = pygame.key.get_pressed()

    if e.type == pygame.QUIT:
        gameState.gameOn = False

    if e.type == pygame.KEYDOWN and keys[pygame.K_SPACE]:
        gameState.spawnNewBall()

    for ball in gameState.liveBalls:
        if ball.x > gameState.width:
            gameState.liveBalls.remove(ball)

    if len(gameState.liveBalls) == 0:
        gameState.setGameOver()

    for ball in gameState.liveBalls:
        gameState.scoreValue = updateBall(
            ball,
            gameState.paddle,
            gameState.height,
            gameState.border,
            gameState.scoreValue,
        )
    updatePaddle(gameState.paddle, gameState.border, gameState.height)

    return gameState


def paddleBounce(ball: Ball, paddle: Paddle):
    """
    Calculates a return angle for a ball colliding with the paddle.
    Rebound angle is determined by where the ball strikes the paddle.
    """
    paddleCOM = paddle.y + int(paddle.HEIGHT * 0.5)
    speed = ball.getVelocity().getMagnitude()
    newSpeed = int(speed) + random.randint(-25, 50)
    newSpeed = max(newSpeed, 100)
    offset = -(paddleCOM - ball.y) * 2 / paddle.HEIGHT
    reboundAngle = offset * math.pi / 3

    newVelocity = Vector.fromPolarCoOrds(-newSpeed, -reboundAngle)
    ball.setVelocity(newVelocity)


def wallBounce(ball: Ball):
    """
    Inverts the x axis of a ball velocity vector.
    Increments the x value a random amount.
    """
    velocity = ball.getVelocity()
    invertedX = Vector.invertX(velocity)
    ball.setVelocity(invertedX)
    ball.vx += random.randint(50, 100)


def updateBall(ball: Ball, paddle: Paddle, height, border, scrValue):
    """
    Updates x and y position of the ball based on original positions combined with time differential.
    Detects collision with paddle or walls and reverses travel direction.
    Increments Score Value for display on score board.
    Destroys the ball if it travels off screen right.
    """
    now = current_time()

    if ball.timeOfLastUpdate is None:
        timeSinceLastUpdate = 0.0
    else:
        timeSinceLastUpdate = timeSince(ball.timeOfLastUpdate)

    ball.timeOfLastUpdate = now

    newX = ball.x + timeSinceLastUpdate * ball.vx
    newY = ball.y + timeSinceLastUpdate * ball.vy

    paddleCollision = ball.getHitBox().colliderect(paddle.getHitBox())

    if paddleCollision:
        paddleBounce(ball, paddle)

    hitBackWall = newX < border + ball.RADIUS

    if hitBackWall:
        scrValue += 1
        wallBounce(ball)
        newX = ball.x + timeSinceLastUpdate * ball.vx

    if newY < border + ball.RADIUS:
        scrValue += 1
        ball.vy = +abs(ball.vy)
        newY = ball.y + timeSinceLastUpdate * ball.vy

    if newY > height - border - ball.RADIUS:
        scrValue += 1
        ball.vy = -abs(ball.vy)
        newY = ball.y + timeSinceLastUpdate * ball.vy

    ball.x = newX
    ball.y = newY

    return scrValue


def updatePaddle(paddle: Paddle, borderSize, height):
    """
    Updates the paddle position and defines the boundaries of the play space.
    Positional tracking is used to prevent paddle leaving the screen, not hitbox collisions.
    """
    upperBound = paddle.HEIGHT * 0.5 + borderSize
    lowerBound = height - paddle.HEIGHT * 0.5 - borderSize
    outOfBoundsAbove = pygame.mouse.get_pos()[1] < upperBound
    outOfBoundsBelow = pygame.mouse.get_pos()[1] > lowerBound

    if not outOfBoundsAbove and not outOfBoundsBelow:
        """
        Controls the paddle Y position with the mouse.
        """
        paddle.y = pygame.mouse.get_pos()[1] - Paddle.HEIGHT * 0.5

    elif outOfBoundsAbove:
        """
        Prevent the paddle from moving beyond an upper limit.
        """
        paddle.y = upperBound - Paddle.HEIGHT * 0.5

    elif outOfBoundsBelow:
        """
        Prevent the paddle from moving beyond a lower limit.
        """
        paddle.y = lowerBound - Paddle.HEIGHT * 0.5

    else:
        raise ValueError('ya fucked it')
