from src.lib.spaces.vector import Vector


class Movable:
    def getPosition(self) -> Vector:
        """
        Gets the current position of a movable
        :return: Vector
        """
        pass

    def getVelocity(self) -> Vector:
        """
        Gets the current velocity
        :return:
        """
        pass

    def setPosition(self, position: Vector) -> None:
        """
        Sets the current position of a movable
        :return: None
        """
        pass

    def setVelocity(self, velocity: Vector) -> Vector:
        """
        Sets the current velocity
        :return:
        """
        pass
