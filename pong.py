import pygame
import time

# Variables
HEIGHT = 600
WIDTH = 1200
BORDER = 20
bgColour = pygame.Color("black")
fgColour = pygame.Color("red")
ballColour = pygame.Color("white")
paddleColour = pygame.Color("blue")
velocity = 300

pygame.init()


def current_time():
    return time.time()


def timeSince(when):
    return current_time() - when


def renderBackGround():
    global screen, bgColour, fgColour, WIDTH, BORDER, HEIGHT

    pygame.draw.rect(screen, bgColour, pygame.Rect((0, 0), (WIDTH, HEIGHT)))
    pygame.draw.rect(screen, fgColour, pygame.Rect((0, 0), (WIDTH, BORDER)))
    pygame.draw.rect(screen, fgColour, pygame.Rect((0, 0), (BORDER, HEIGHT)))
    pygame.draw.rect(screen, fgColour, pygame.Rect((0, HEIGHT - BORDER), (WIDTH, BORDER)))


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
        upperBound = Paddle.HEIGHT//2 + BORDER
        lowerBound = HEIGHT - Paddle.HEIGHT//2 - BORDER
        outOfBoundsAbove = pygame.mouse.get_pos()[1] < upperBound
        outOfBoundsBelow = pygame.mouse.get_pos()[1] > lowerBound

        if not outOfBoundsAbove and not outOfBoundsBelow:
            self.y = pygame.mouse.get_pos()[1] - Paddle.HEIGHT//2

        elif outOfBoundsAbove:
            self.y = upperBound - Paddle.HEIGHT//2

        elif outOfBoundsBelow:
            self.y = lowerBound - Paddle.HEIGHT//2

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

    def update(self, paddle: Paddle):
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

        if horizontalOutOfBounds:
            self.vx = -self.vx
            newX = self.x + timeSinceLastUpdate * self.vx

        if hasCollided:
            self.vx = -abs(self.vx)

        if newY < BORDER + Ball.RADIUS or newY > HEIGHT - BORDER - Ball.RADIUS:
            self.vy = -self.vy
            newY = self.y + timeSinceLastUpdate * self.vy

        self.x = newX
        self.y = newY


paddlePlay = Paddle(WIDTH - BORDER * 3 - Paddle.WIDTH, HEIGHT // 2 - Paddle.HEIGHT // 2)
ballPlay = Ball(WIDTH - Ball.RADIUS, HEIGHT // 2, - velocity, 150)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

while True:
    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        break

    paddlePlay.show()
    ballPlay.show()
    pygame.display.flip()
    renderBackGround()
    ballPlay.update(paddlePlay)
    paddlePlay.update()

pygame.quit()
