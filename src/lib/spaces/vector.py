from __future__ import annotations

import math


class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @staticmethod
    def fromPolarCoOrds(magnitude: float, angle: float) -> Vector:
        x = magnitude * math.cos(angle)
        y = magnitude * math.sin(angle)

        return Vector(x, y)

    def getMagnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def scale(self, scaleFactor: float) -> Vector:
        newX = self.x * scaleFactor
        newY = self.y * scaleFactor

        return Vector(newX, newY)

    def add(self, vector: Vector) -> Vector:
        newX = self.x + vector.x
        newY = self.y + vector.y
        newVector = Vector(newX, newY)

        return newVector

    def invert(self) -> Vector:
        return Vector(-self.x, -self.y)

    def invertX(self) -> Vector:
        return Vector(-self.x, self.y)

    def invertY(self) -> Vector:
        return Vector(self.x, -self.y)
