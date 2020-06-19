from pongEntities import GameState


def updateGameState(gameState: GameState) -> GameState:
    """
    Tracks position and collision of each ball. Updates total score value based on return value from each ball.
    Tracks paddle and collision with walls.
    """
    for gameState.ball in gameState.liveBalls:
        gameState.scoreValue = gameState.ball.update(gameState.paddle, gameState.height, gameState.border, gameState.scoreValue)
    gameState.paddle.update(gameState.border, gameState.height)

    return gameState
