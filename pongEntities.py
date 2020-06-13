import pygame
import time
import random

scoreValue = 0


def current_time():
    return time.time()


def timeSince(when):
    return current_time() - when


class ScoreBoard:
    SIZE = (300, 100)
    POSITION = (50, 50)
    gameOverMessage = 'You Suck!'

    def __init__(self):
        pass

    def show(self, screen):
        global scoreValue
        # Renders Score board
        surface = pygame.Surface((300, 100))
        surface = surface.convert()
        surface.fill((255, 255, 255))
        screen.blit(surface, ScoreBoard.POSITION)

        # Renders Score
        font = pygame.font.Font(None, 36)
        score = font.render(str(scoreValue), 1, (10, 10, 10))
        textPos = score.get_rect(
            centerx=ScoreBoard.POSITION[0] + ScoreBoard.SIZE[0] // 2,
            centery=ScoreBoard.POSITION[1] + ScoreBoard.SIZE[1] // 2
        )
        screen.blit(score, textPos)

    def displayGameOver(self, screen):
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
    WIDTH = 10
    HEIGHT = 150

    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.colour = colour

    def getHitBox(self):
        return pygame.Rect((self.x, self.y), (Paddle.WIDTH, Paddle.HEIGHT))

    def show(self, screen):
        pygame.draw.rect(screen, self.colour, pygame.Rect((self.x, self.y), (Paddle.WIDTH, Paddle.HEIGHT)))

    def update(self, borderSize, height):
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
    RADIUS = 10

    def __init__(self, x, y, vx, vy, colour):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.timeOfLastUpdate = None
        self.colour = colour

    def getHitBox(self):
        return pygame.Rect((int(self.x) - Ball.RADIUS, int(self.y) - Ball.RADIUS), (Ball.RADIUS * 2, Ball.RADIUS * 2))

    def show(self, screen):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), Ball.RADIUS)

    def destroy(self, balls):
        balls.remove(self)

    def update(self, paddle: Paddle, width, height, border, balls):
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
