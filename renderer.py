import pygame

from pongEntities import Ball, Paddle, GameState, ScoreBoard

screen: pygame.Surface
screenDimensions = (720, 1080)
backgroundColour: tuple
borderColour: tuple
borderWidth = 25


def initialise(bkgrndCol, brdrCol, screenDims=None, brdrWidth=None):
    global screen, screenDimensions, backgroundColour, borderColour, borderWidth
    borderColour = brdrCol
    backgroundColour = bkgrndCol
    if screenDims is not None:
        screenDimensions = screenDims
    if brdrWidth is not None:
        borderWidth = brdrWidth
    screen = pygame.display.set_mode(screenDimensions)


def renderBall(ball: Ball):
    pygame.draw.circle(screen, ball.colour, (int(ball.x), int(ball.y)), Ball.RADIUS)


def renderPaddle(paddle: Paddle):
    pygame.draw.rect(
        screen,
        paddle.colour,
        pygame.Rect((paddle.x, paddle.y), (Paddle.WIDTH, Paddle.HEIGHT))
    )


def renderScoreboard(gameState: GameState):
    if gameState.gameIsOver:
        renderGameOnScore(gameState.scoreValue)
        displayGameOver()
        pygame.display.flip()

def displayGameOver():
    """
    Creates the font object for game over message display.
    Passes the game over message to be rendered along with colour as RGB.
    Positions the message within the score board surface.
    Blits the surface to the main screen.
    """
    font = pygame.font.SysFont('comicsansms', 36)
    text = font.render(ScoreBoard.gameOverMessage, 1, (10, 10, 10))
    textPos = text.get_rect(
        centerx=ScoreBoard.POSITION[0] + ScoreBoard.SIZE[0] * 0.5,
        centery=ScoreBoard.POSITION[1] + ScoreBoard.SIZE[1] * 0.5 + 25
    )
    screen.blit(text, textPos)


def renderGameOnScore(scoreValue):
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


def renderWalls():
    global screen, borderColour, borderWidth
    pygame.draw.rect(
        screen,
        borderColour,
        pygame.Rect((0, 0), (screenDimensions[0], borderWidth)),
    )
    pygame.draw.rect(
        screen,
        borderColour,
        pygame.Rect((0, 0), (borderWidth, screenDimensions[1])),
    )
    pygame.draw.rect(
        screen,
        borderColour,
        pygame.Rect((0, screenDimensions[1] - borderWidth), (screenDimensions[0], borderWidth)),
    )


def blitBackground():
    global screen, backgroundColour
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(backgroundColour)
    screen.blit(
        background,
        (0, 0)
    )


def render(gameState: GameState):
    blitBackground()
    renderWalls()
    renderScoreboard(gameState)
    renderGameOnScore(gameState.scoreValue)
    for ball in gameState.liveBalls:
        if ball.x < gameState.width:
            renderBall(ball)
    renderPaddle(gameState.paddle)
    pygame.display.flip()

