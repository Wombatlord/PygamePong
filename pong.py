import pygame
import time
from src.renderer import renderer
from src.engine import engine
from configReader import reader
from src.game_state.pongEntities import GameState

pygame.init()
pygame.display.set_caption("PONGO!")
pygame.mouse.set_visible(0)

# Get config
configPaths = [
    'config/config.yml',
    'config/config.local.yml',
]
config = reader.get(configPaths)

# Instantiate GameState and initialise renderer.
renderer.initialise(config)
gameState: GameState = GameState(config, renderer.ballSprite)

clock = pygame.time.Clock()
FPS = 120
frameCount = 0

# MAIN LOOP
while gameState.gameOn:
    clock.tick(FPS)
    frameCount += 1
    print(frameCount)

    renderer.render(gameState)

    if gameState.gameIsOver:
        renderer.renderScoreboard(gameState)
        time.sleep(2)
        pygame.event.wait()
        gameState.resetGame()

    gameState = engine.updateGameState(gameState)

pygame.quit()
