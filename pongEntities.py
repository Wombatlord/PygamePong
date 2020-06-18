import pygame
import time
import random

scoreValue = 0
randomRGB = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),)


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
    Provides a pygame Surface for displaying text and score values.
    Controls size and position on screen.
    Handles updating the displayed score and displaying the game over message.
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
        self.colour = colour

    def getHitBox(self):
        """
        Returns a hit-box for collision detection which corresponds to paddle location and size.
        """
        return pygame.Rect((self.x, self.y), (Paddle.WIDTH, Paddle.HEIGHT))

    def update(self, borderSize, height):
        """
        Updates the paddle position and defines the boundaries of the play space.
        Positional tracking is used to prevent paddle leaving the screen, not hitbox collisions.
        """
        upperBound = Paddle.HEIGHT * 0.5 + borderSize
        lowerBound = height - Paddle.HEIGHT * 0.5 - borderSize
        outOfBoundsAbove = pygame.mouse.get_pos()[1] < upperBound
        outOfBoundsBelow = pygame.mouse.get_pos()[1] > lowerBound

        if not outOfBoundsAbove and not outOfBoundsBelow:
            """
            Controls the paddle Y position with the mouse.
            """
            self.y = pygame.mouse.get_pos()[1] - Paddle.HEIGHT * 0.5

        elif outOfBoundsAbove:
            """
            Prevent the paddle from moving beyond an upper limit.
            """
            self.y = upperBound - Paddle.HEIGHT * 0.5

        elif outOfBoundsBelow:
            """
            Prevent the paddle from moving beyond a lower limit.
            """
            self.y = lowerBound - Paddle.HEIGHT * 0.5

        else:
            raise ValueError('ya fucked it')


class Ball:
    """
    liveBalls are responsible for:
    Providing a hit-box,
    showing a ball,
    destroying a ball,
    tracking position,
    detecting collisions,
    incrementing score.
    """
    RADIUS = 10

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

    def destroy(self, liveBalls):
        """
        Removes ball object from list of liveBalls to ensure invalid liveBalls are not displayed.
        """
        liveBalls.remove(self)

    def update(self, paddle: Paddle, height, border, scrValue):
        """
        Updates x and y position of the ball based on original positions combined with time differential.
        Detects collision with paddle or walls and reverses travel direction.
        Increments Score Value for display on score board.
        Destroys the ball if it travels off screen right.
        """
        now = current_time()

        if self.timeOfLastUpdate is None:
            timeSinceLastUpdate = 0.0
        else:
            timeSinceLastUpdate = timeSince(self.timeOfLastUpdate)

        self.timeOfLastUpdate = now

        newX = self.x + timeSinceLastUpdate * self.vx
        newY = self.y + timeSinceLastUpdate * self.vy

        hasCollided = self.getHitBox().colliderect(paddle.getHitBox())
        horizontalOutOfBounds = newX < border + Ball.RADIUS

        if horizontalOutOfBounds:
            scrValue += 1
            self.vx = -self.vx + random.randint(25, 100)
            newX = self.x + timeSinceLastUpdate * self.vx

        if hasCollided:
            self.vx = -abs(self.vx) + random.randint(-25, 25)
            self.vy = -abs(self.vy) + random.randint(-200, 350)

        if newY < border + Ball.RADIUS:
            scrValue += 1
            self.vy = +abs(self.vy)
            newY = self.y + timeSinceLastUpdate * self.vy

        if newY > height - border - Ball.RADIUS:
            scrValue += 1
            self.vy = -abs(self.vy)
            newY = self.y + timeSinceLastUpdate * self.vy

        self.x = newX
        self.y = newY

        return scrValue


# I tried.
class GameState:

    def __init__(
        self,
        screen,
        ball: Ball,
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
        self.ball = ball
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

    def updateGameState(self):
        """
        Tracks position and collision of each ball. Updates total score value based on return value from each ball.
        Tracks paddle and collision with walls.
        """
        for self.ball in self.liveBalls:
            self.scoreValue = self.ball.update(self.paddle, self.height, self.border, self.scoreValue)
        self.paddle.update(self.border, self.height)

    def newBall(self):
        """
        Instantiates a new ball object and appends it to the liveBalls list.
        Initial X & Y Positions, and RGB colour value, are randomly determined at instantiation.
        """
        initialVelocityY = random.randint(-100, 200)
        initialVelocityX = random.randint(400, 600)
        ballColour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.ball = Ball(
            self.width - Ball.RADIUS - random.randint(50, 500),
            random.randint(50, self.height) - self.border,
            - initialVelocityX,
            initialVelocityY,
            ballColour,
        )

        self.liveBalls.append(self.ball)
        # print(initialVelocityX, initialVelocityY)

    def gameOver(self):
        """
        Sets a flag to trigger Game Over State.
        Used to display game over message and freeze game play.
        """
        self.gameIsOver = True

    def resetScore(self):
        self.scoreValue = 0

    def destroyBall(self):
        self.liveBalls.remove(self.ball)

    def changeBallColour(self):
        self.ball.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))