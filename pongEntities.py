import pygame
import time
import random

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
    Provides a pygame Surface for displaying text and score values.
    Controls size and position on screen.
    Handles updating the displayed score and displaying the game over message.
    """
    SIZE = (300, 100)
    POSITION = (50, 50)
    gameOverMessage = 'You Suck!'

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
        font = pygame.font.Font(None, 36)
        score = font.render(str(scoreValue), 1, (10, 10, 10))
        textPos = score.get_rect(
            centerx=ScoreBoard.POSITION[0] + ScoreBoard.SIZE[0] // 2,
            centery=ScoreBoard.POSITION[1] + ScoreBoard.SIZE[1] // 2
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
        font = pygame.font.Font(None, 36)
        text = font.render(ScoreBoard.gameOverMessage, 1, (10, 10, 10))
        textPos = text.get_rect(
            centerx=ScoreBoard.POSITION[0] + ScoreBoard.SIZE[0] // 2,
            centery=ScoreBoard.POSITION[1] + ScoreBoard.SIZE[1] // 2 + 25
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
        upperBound = Paddle.HEIGHT // 2 + borderSize
        lowerBound = height - Paddle.HEIGHT // 2 - borderSize
        outOfBoundsAbove = pygame.mouse.get_pos()[1] < upperBound
        outOfBoundsBelow = pygame.mouse.get_pos()[1] > lowerBound

        if not outOfBoundsAbove and not outOfBoundsBelow:
            self.y = pygame.mouse.get_pos()[1] - Paddle.HEIGHT // 2

        elif outOfBoundsAbove:
            self.y = upperBound - Paddle.HEIGHT // 2

        elif outOfBoundsBelow:
            self.y = lowerBound - Paddle.HEIGHT // 2

        else:
            raise ValueError('ya fucked it')


class Ball:
    """
    Balls are responsible for:
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

    def destroy(self, balls):
        """
        Removes ball object from list of balls to ensure invalid balls are not displayed.
        """
        balls.remove(self)

    def update(self, paddle: Paddle, width, height, border, balls):
        """
        Updates x and y position of the ball based on original positions combined with time.
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
        offScreen = newX > width

        if offScreen:
            self.destroy(balls)
            return

        if horizontalOutOfBounds:
            scoreValue += 1
            self.vx = -self.vx + random.randint(25, 100)
            newX = self.x + timeSinceLastUpdate * self.vx

        if hasCollided:
            self.vx = -abs(self.vx) + random.randint(-25, 25)
            self.vy = -abs(self.vy) + random.randint(-200, 350)

        if newY < border + Ball.RADIUS or newY > height - border - Ball.RADIUS:
            scoreValue += 1
            self.vy = -self.vy
            newY = self.y + timeSinceLastUpdate * self.vy

        self.x = newX
        self.y = newY


# I tried.
class GameState:
    def __init__(self, screen, ball: Ball, paddle: Paddle, scoreBoard: ScoreBoard):
        self.screen = screen
        self.ball = ball
        self.paddle = paddle
        self.scoreBoard = scoreBoard

    def updateGameState(self):
        self.ball.update(self.paddle)
        self.paddle.update()

    def show(self):
        self.ball.show(self.screen)
        self.paddle.show(self.screen)
        self.scoreBoard.show(self.screen)
