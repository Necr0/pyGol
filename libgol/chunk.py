import scipy as _sci

from .common import Position


class Chunk:
    def __init__(self, width: int, height: int):
        self.__occupied_cells = 0
        self.width = width
        self.height = height
        self.__array: _sci.ndarray = _sci.full((width, height), 0)

    def __getitem__(self, key: Position) -> int:
        return self.__array[key]

    def __setitem__(self, key: Position, value: int) -> None:
        if self.__array[key] == value:
            return
        self.__array[key] = value
        self.__occupied_cells += 1 if value else -1

    def empty(self) -> bool:
        return not self.__occupied_cells

    def __iter__(self):
        return _sci.ndenumerate(self.__array)
