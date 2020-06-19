import math
import random
import time

import pygame

from pongEntities import GameState, Ball, Paddle


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
    Tracks position and collision of each ball. Updates total score value based on return value from each ball.
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

    hasCollided = ball.getHitBox().colliderect(paddle.getHitBox())
    horizontalOutOfBounds = newX < border + ball.RADIUS

    paddleCOM = paddle.y + int(paddle.HEIGHT * 0.5)

    if horizontalOutOfBounds:
        scrValue += 1
        ball.vx = -ball.vx + random.randint(25, 100)
        newX = ball.x + timeSinceLastUpdate * ball.vx

    if hasCollided:
        speed = math.sqrt(float(ball.vx) ** 2.0 + float(ball.vy) ** 2.0)
        newSpeed = int(speed) + random.randint(-25, 50)
        newSpeed = max(newSpeed, 100)
        offset = -(paddleCOM - ball.y) * 2 / paddle.HEIGHT
        reboundAngle = offset * math.pi / 3

        ball.vy = newSpeed * math.sin(reboundAngle)
        ball.vx = -abs(newSpeed * math.cos(reboundAngle))

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