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
    'assets/block_layouts/layout1.yml'
]

config = reader.get(configPaths)

# Instantiate GameState and initialise renderer.
gameState: GameState = GameState(config)
renderer.initialise(config)

clock = pygame.time.Clock()

# MAIN LOOP
while gameState.gameOn:
    clock.tick(config["display"]["framerate"]["max"])

    renderer.render(gameState)

    if gameState.gameIsOver:
        renderer.renderScoreboard(gameState)
        time.sleep(2)
        pygame.event.wait()
        gameState.resetGame()

    gameState = engine.updateGameState(gameState)

pygame.quit()
