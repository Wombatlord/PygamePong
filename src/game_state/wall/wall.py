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

    def getX(self) -> int:
        return int(self.position.x)

    def getY(self) -> int:
        return int(self.position.y)

    def getWidth(self) -> int:
        return int(self.dimensions[0])

    def getHeight(self) -> int:
        return int(self.dimensions[1])

    def getDimensionsVector(self) -> Vector:
        return Vector(self.dimensions[0], self.dimensions[1])

    def getCentre(self) -> Vector:
        return self.position + Vector(self.dimensions[0] // 2, self.dimensions[1] // 2)


def getBlocks(level: dict) -> list:
    initialPointer: Vector = Vector(600, 50)
    blockDimensions: tuple = (25, 100)
    gap: int = 25
    generatorX = Vector(blockDimensions[0] + gap, 0).scale(-1)
    generatorY = Vector(0, blockDimensions[1] + gap)
    blocks: list = []
    print(level["rows"])
    for xIndex, row in enumerate(level["rows"]):
        for yIndex, cell in enumerate(row):
            positionPointer = initialPointer + generatorX.scale(xIndex) + generatorY.scale(yIndex)
            if cell:
                blocks.append(Block(positionPointer, blockDimensions))
                positionPointer = positionPointer + generatorY
                print(positionPointer)

    return blocks
