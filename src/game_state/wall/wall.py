import pygame

from src.lib.spaces.vector import Vector


class Block:
    def __init__(self, position: Vector, dimensions: tuple) -> None:
        self.position = position
        self.dimensions = dimensions

    def getHitBox(self):
        """
        Returns a hit-box for collision detection which corresponds to paddle location and size.
        """
        return pygame.Rect(
            (self.position.x, self.position.y),
            (self.dimensions[0], self.dimensions[1])
        )


def getBlocks():
    return [
        Block(
            Vector(300, 300),
            (25, 100)
        )
    ]
