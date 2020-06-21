from src.lib.spaces.vector import Vector


class OrientedPlane:
    def __init__(self, normal: Vector) -> None:
        self.normal = normal.normalise()

    def reflect(self, initialVector: Vector):
        normalComponent: float = initialVector.dot(self.normal)
        if normalComponent < 0:
            normalComponentVector = self.normal.scale(normalComponent)
            reflector = normalComponentVector.scale(-2)
        else:
            reflector = Vector(0, 0)

        return initialVector + reflector
