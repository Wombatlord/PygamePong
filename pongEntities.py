import pygame
import time
import random
import os

from vector import Vector

scoreValue = 0


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


class ScoreBoard:
    """
    Variables for ScoreBoard Surface and Game Over Message.
    """
    SIZE = (300, 100)
    POSITION = (50, 50)
    gameOverMessage = 'fucked it'

    def __init__(self):
        pass


class Paddle:
    """
    Paddle objects are responsible for providing a hit-box, showing the paddle, and tracking position.
    """
    WIDTH = 10
    HEIGHT = 150

    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.height = Paddle.HEIGHT
        self.width = Paddle.WIDTH
        self.colour = colour

    def getHitBox(self):
        """
        Returns a hit-box for collision detection which corresponds to paddle location and size.
        """
        return pygame.Rect((self.x, self.y), (self.width, self.height))


class Ball:
    """
    liveBalls are responsible for:
    Providing a hit-box for collision detection,
    Tracking position,
    Provide Velocity Vector interface,
    Change colour.
    """
    RADIUS = 10
    BALLSPRITE = pygame.image.load(os.path.join("assets", "earthball20x20.png"))

    def __init__(self, x, y, vx, vy, colour):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.timeOfLastUpdate = None
        self.colour = colour

    def getHitBox(self):
        """
        Returns a rectangular hit-box corresponding to ball size for collision detection.
        """
        return pygame.Rect((int(self.x) - Ball.RADIUS, int(self.y) - Ball.RADIUS), (Ball.RADIUS * 2, Ball.RADIUS * 2))

    def getVelocity(self) -> Vector:
        return Vector(self.vx, self.vy)

    def setVelocity(self, vector: Vector):
        self.vx = vector.x
        self.vy = vector.y

# I tried.
class GameState:

    def __init__(
            self,
            screen,
            paddle: Paddle,
            liveBalls,
            scoreBoard: ScoreBoard,
            width,
            height,
            border,
            borderColour,
            backgroundColour,
    ):
        self.screen = screen
        self.paddle = paddle
        self.liveBalls = liveBalls
        self.scoreBoard = scoreBoard
        self.width = width
        self.height = height
        self.border = border
        self.borderColour = borderColour
        self.backgroundColour = backgroundColour
        self.scoreValue = 0
        self.gameIsOver = False
        self.gameOn = True

    def spawnNewBall(self):
        """
        Instantiates a new ball object and appends it to the liveBalls list.
        Initial X & Y Positions, and RGB colour value, are randomly determined at instantiation.
        """
        initialVelocityY = random.randint(-100, 200)
        initialVelocityX = random.randint(400, 600)
        ballColour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.liveBalls.append(
            Ball(
                self.width - Ball.RADIUS - random.randint(50, 500),
                random.randint(50, self.height) - self.border,
                - initialVelocityX,
                initialVelocityY,
                ballColour,
            )
        )

    def setGameOver(self):
        """
        Sets a flag to trigger Game Over State.
        Used to display game over message and freeze game play.
        """
        self.gameIsOver = True

    def resetGame(self):
        """
        Resets Game Over flag, resets score, and instantiates a new ball.
        """
        self.gameIsOver = False
        self.resetScore()
        self.spawnNewBall()

    def resetScore(self):
        self.scoreValue = 0
