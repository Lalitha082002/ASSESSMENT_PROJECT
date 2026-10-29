class Rectangle:
    

    def __init__(self, length: int, width: int):
        if not isinstance(length, int) or isinstance(length, bool):
            raise TypeError("length must be an int")
        if not isinstance(width, int) or isinstance(width, bool):
            raise TypeError("width must be an int")
        self.length = length
        self.width = width

    def __iter__(self):
        yield {"length": self.length}
        yield {"width": self.width}
