import bge


class Timer():
    """Medidor de tempo!"""

    def __init__(self, initialTime=0):
        self._timer = 0
        self.reset()

        self._timer -= initialTime

    def reset(self):
        self._timer = bge.logic.getRealTime()

    def getElapsedTime(self):
        return bge.logic.getRealTime() - self._timer

    def get(self):
        return bge.logic.getRealTime() - self._timer
