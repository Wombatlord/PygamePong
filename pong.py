import pygame
import time
import random

pygame.init()

# Screen Variables
HEIGHT = 600
WIDTH = 1200
BORDER = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Game Object Variables
fgColour = pygame.Color("red")
ballColour = pygame.Color("black")
paddleColour = pygame.Color("blue")
velocity = 300

# Scoreboard Variables
scoreBoard = pygame.Surface((300, 100))
scoreBoardPos = (50, 50)
scoreBoardSize = (300, 100)
scoreValue = 0


def current_time():
    return time.time()


def timeSince(when):
    return current_time() - when


def renderBackground():
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 175, 0))
    screen.blit(background, (0, 0))


def renderWalls():
    global screen, fgColour, WIDTH, BORDER, HEIGHT

    pygame.draw.rect(screen, fgColour, pygame.Rect((0, 0), (WIDTH, BORDER)))
    pygame.draw.rect(screen, fgColour, pygame.Rect((0, 0), (BORDER, HEIGHT)))
    pygame.draw.rect(screen, fgColour, pygame.Rect((0, HEIGHT - BORDER), (WIDTH, BORDER)))


def renderScoreBoard():
    global screen, scoreBoard, scoreBoardPos
    scoreBoard = scoreBoard.convert()
    scoreBoard.fill((255, 255, 255))
    screen.blit(scoreBoard, scoreBoardPos)


def renderScore():
    global screen, scoreBoard, scoreBoardPos, scoreBoardSize, scoreValue
    font = pygame.font.Font(None, 36)
    score = font.render(str(scoreValue), 1, (10, 10, 10))
    textPos = score.get_rect(centerx=scoreBoardPos[0] + scoreBoardSize[0] // 2,
                             centery=scoreBoardPos[1] + scoreBoardSize[1] // 2)
    screen.blit(score, textPos)


class Paddle:
    WIDTH = 10
    HEIGHT = 150

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getHitBox(self):
        return pygame.Rect((self.x, self.y), (Paddle.WIDTH, Paddle.HEIGHT))

    def show(self):
        global screen
        pygame.draw.rect(screen, paddleColour, pygame.Rect((self.x, self.y), (Paddle.WIDTH, Paddle.HEIGHT)))

    def update(self):
        upperBound = Paddle.HEIGHT // 2 + BORDER
        lowerBound = HEIGHT - Paddle.HEIGHT // 2 - BORDER
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

    def __init__(self, x, y, vx, vy):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.timeOfLastUpdate = None

    def getHitBox(self):
        return pygame.Rect((int(self.x) - Ball.RADIUS, int(self.y) - Ball.RADIUS), (Ball.RADIUS * 2, Ball.RADIUS * 2))

    def show(self):
        global screen
        pygame.draw.circle(screen, ballColour, (int(self.x), int(self.y)), Ball.RADIUS)

    def destroy(self):
        global ballPlay
        ballPlay = Ball(WIDTH - Ball.RADIUS, HEIGHT // 2, 0, 0)

    def update(self, paddle: Paddle):
        global scoreValue, WIDTH, HEIGHT, velocity
        now = current_time()

        if self.timeOfLastUpdate is None:
            timeSinceLastUpdate = 0.0
        else:
            timeSinceLastUpdate = timeSince(self.timeOfLastUpdate)

        self.timeOfLastUpdate = now

        newX = self.x + timeSinceLastUpdate * self.vx
        newY = self.y + timeSinceLastUpdate * self.vy

        hasCollided = self.getHitBox().colliderect(paddle.getHitBox())
        horizontalOutOfBounds = newX < BORDER + Ball.RADIUS
        offScreen = newX > WIDTH

        if offScreen:
            Ball.destroy(self)

        if horizontalOutOfBounds:
            scoreValue += 1
            self.vx = -self.vx + random.randint(25, 100)
            newX = self.x + timeSinceLastUpdate * self.vx

        if hasCollided:
            self.vx = -abs(self.vx) + random.randint(-25, 25)
            self.vy = -abs(self.vy) + random.randint(-200, 350)

        if newY < BORDER + Ball.RADIUS or newY > HEIGHT - BORDER - Ball.RADIUS:
            scoreValue += 1
            self.vy = -self.vy
            newY = self.y + timeSinceLastUpdate * self.vy

        self.x = newX
        self.y = newY


paddlePlay = Paddle(WIDTH - BORDER * 3 - Paddle.WIDTH, HEIGHT // 2 - Paddle.HEIGHT // 2)
ballPlay = Ball(WIDTH - Ball.RADIUS, HEIGHT // 2, - velocity, 150)

while True:
    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        break

    renderBackground()
    renderScoreBoard()
    renderScore()
    renderWalls()
    paddlePlay.show()
    ballPlay.show()
    pygame.display.flip()
    ballPlay.update(paddlePlay)
    paddlePlay.update()

pygame.quit()
