import os

import pygame

from src.game_state.pongEntities import Ball, Paddle, GameState, ScoreBoard

# Config Parameters
# screen: pygame.Surface
# screenDimensions = (720, 1080)
# backgroundColour: tuple
# borderColour: tuple
# borderWidth = 25

mainDir = os.getcwd()
backgroundSprites = []


def initialise(config):
    """
    Creates the main Surface for display according to passed in config parameters.
    Parameters are background colour and border colour as RGB tuples, X & Y dimensions, and border thickness.
    """
    global screen, screenDimensions, backgroundColour, borderColour, borderWidth
    borderColour = pygame.Color(config["display"]["colours"]["border"])
    backgroundColour = config["display"]["colours"]["background"]
    screenDimensions = (
        config["display"]["resolution"]["width"],
        config["display"]["resolution"]["height"]
    )
    borderWidth = config["gameplay"]["border"]
    screen = pygame.display.set_mode(screenDimensions)

    # SPRITE INITIALISATION TESTING
    bgSprite = loadImage(config["display"]["sprites"]["background"])
    backgroundSprites.append(bgSprite)


def loadImage(file):
    """
    :param: Name of sprite image to be loaded, including extension.
    :return: Sprite converted for fast display.
    """
    file = os.path.join(mainDir, "assets", file)
    surface = pygame.image.load(file)
    return surface.convert()


def renderBall(ball: Ball):
    # screen.blit(ball.BALLSPRITE, (ball.x, ball.y))

    pygame.draw.circle(screen, ball.colour, (int(ball.x), int(ball.y)), Ball.RADIUS)


def renderPaddle(paddle: Paddle):
    pygame.draw.rect(
        screen,
        paddle.colour,
        pygame.Rect((paddle.x, paddle.y), (paddle.width, paddle.height))
    )


def renderScoreboard(gameState: GameState):
    """
    Displays the final score total and Game Over Message on the score board Surface.
    """
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
    """
    Renders three walls on screen. Top / Bottom / Left.
    Walls are drawn according to screen dimension and border width config parameter.
    """
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


def blitBackground(sprites: list):
    """
    Creates a background surface equivalent to main screen size.
    Converts surface for quick display.
    Fills background with configured colour.
    Blits the background to the background Surface.
    """

    # background = pygame.Surface(screen.get_size())
    # background = background.convert()
    # background.fill(backgroundColour)
    # screen.blit(
    #     background,
    #     (0, 0)
    # )

    screen.fill((0, 0, 0))
    screen.blit(
        sprites[0],
        (0, 0)
    )


def render(gameState: GameState):
    """
    Combines renderer functions to display GameState.
    Call this function once in the main loop to provide display output.
    """
    blitBackground(backgroundSprites)
    renderWalls()
    renderScoreboard(gameState)
    renderGameOnScore(gameState.scoreValue)
    for ball in gameState.liveBalls:
        if ball.x < gameState.width:
            renderBall(ball)
    renderPaddle(gameState.paddle)
    pygame.display.flip()
