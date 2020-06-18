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

    def show(self, screen):
        global scoreValue
        """
        Creates the pygame surface for score display.
        Converts the surface for fast display.
        Fills the surface according to RGB values.
        Blits the surface to the main screen.
        """
        surface = pygame.Surface((300, 100))
        surface = surface.convert()
        surface.fill((255, 255, 255))
        screen.blit(surface, ScoreBoard.POSITION)

        """
        Creates the font object for displaying score values.
        Score is integer and must be converted to string for display, colour is provided as RGB.
        Positions the string within the score board surface.
        Blits the surface to the main screen.
        """
        font = pygame.font.SysFont("comicsansms", 36)
        score = font.render(str(scoreValue), 1, (10, 10, 10))
        textPos = score.get_rect(
            centerx=ScoreBoard.POSITION[0] + ScoreBoard.SIZE[0] * 0.5,
            centery=ScoreBoard.POSITION[1] + ScoreBoard.SIZE[1] * 0.5
        )
        screen.blit(score, textPos)

    def displayGameOver(self, screen):
        """
        Creates the font object for game over message display.
        Passes the game over message to be rendered along with colour as RGB.
        Positions the message within the score board surface.
        Blits the surface to the main screen.
        """
        global scoreValue
        font = pygame.font.SysFont('comicsansms', 36)
        text = font.render(ScoreBoard.gameOverMessage, 1, (10, 10, 10))
        textPos = text.get_rect(
            centerx=ScoreBoard.POSITION[0] + ScoreBoard.SIZE[0] * 0.5,
            centery=ScoreBoard.POSITION[1] + ScoreBoard.SIZE[1] * 0.5 + 25
        )
        screen.blit(text, textPos)

    def reset(self):
        global scoreValue
        scoreValue = 0


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

    def show(self, screen):
        """
        Draws a rectangle on the main game Surface.
        """
        pygame.draw.rect(screen, self.colour, pygame.Rect((self.x, self.y), (Paddle.WIDTH, Paddle.HEIGHT)))

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

    def show(self, screen):
        """
        Draws a circle on the main game Surface.
        """
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), Ball.RADIUS)

    def destroy(self, liveBalls):
        """
        Removes ball object from list of liveBalls to ensure invalid liveBalls are not displayed.
        """
        liveBalls.remove(self)

    def update(self, paddle: Paddle, width, height, border, liveBalls):
        """
        Updates x and y position of the ball based on original positions combined with time differential.
        Detects collision with paddle or walls and reverses travel direction.
        Increments Score Value for display on score board.
        Destroys the ball if it travels off screen right.
        """
        global scoreValue
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
            scoreValue += 1
            self.vx = -self.vx + random.randint(25, 100)
            newX = self.x + timeSinceLastUpdate * self.vx

        if hasCollided:
            self.vx = -abs(self.vx) + random.randint(-25, 25)
            self.vy = -abs(self.vy) + random.randint(-200, 350)

        if newY < border + Ball.RADIUS:
            scoreValue += 1
            self.vy = +abs(self.vy)
            newY = self.y + timeSinceLastUpdate * self.vy

        if newY > height - border - Ball.RADIUS:
            scoreValue += 1
            self.vy = -abs(self.vy)
            newY = self.y + timeSinceLastUpdate * self.vy

        self.x = newX
        self.y = newY


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

    def updateGameState(self):
        for self.ball in self.liveBalls:
            self.ball.update(self.paddle, self.width, self.height, self.border, self.liveBalls)
        self.paddle.update(self.border, self.height)

    def newBall(self):
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
        self.scoreBoard.displayGameOver(self.screen)
        self.scoreBoard.reset()
        pygame.display.flip()

    def destroyBall(self):
        self.liveBalls.remove(self.ball)

    def changeBallColour(self):
        self.ball.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def show(self):
        self.ball.show(self.screen)
        self.paddle.show(self.screen)
        self.scoreBoard.show(self.screen)

    def renderBackground(self):
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill(self.backgroundColour)
        self.screen.blit(background, (0, 0))

    def renderWalls(self):
        pygame.draw.rect(
            self.screen,
            self.borderColour,
            pygame.Rect((0, 0), (self.width, self.border)),
        )
        pygame.draw.rect(
            self.screen,
            self.borderColour,
            pygame.Rect((0, 0), (self.border, self.height)),
        )
        pygame.draw.rect(
            self.screen,
            self.borderColour,
            pygame.Rect((0, self.height - self.border), (self.width, self.border)),
        )