import pygame
import time
import renderer

import engine
from configReader import reader
from pongEntities import GameState

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
gameState: GameState = GameState(config)
renderer.initialise(config)

# MAIN LOOP
while gameState.gameOn:
    renderer.render(gameState)

    if gameState.gameIsOver:
        renderer.renderScoreboard(gameState)
        time.sleep(2)
        pygame.event.wait()
        gameState.resetGame()

    gameState = engine.updateGameState(gameState)

pygame.quit()
