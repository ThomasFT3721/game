from enum import Enum


class Color(Enum):
    RED = "91"
    ORANGE = "38;5;208"
    GREEN = "92"
    YELLOW = "93"
    BLUE = "94"
    PURPLE = "95"
    CYAN = "96"
    WHITE = "97"
    GREY = "90"
    BLACK = "30"


class BackgroundColor(Enum):
    RED = "101"
    ORANGE = "48;5;208"
    GREEN = "102"
    YELLOW = "103"
    BLUE = "104"
    PURPLE = "105"
    CYAN = "106"
    WHITE = "107"
    GREY = "100"
    BLACK = "40"
    DEFAULT = "49"


class Style:

    def __init__(self, color: Color, background_color: BackgroundColor = None, bold: bool = False,
                 underline: bool = False):
        self.color = color
        self.background_color = background_color
        self.bold = bold
        self.underline = underline

    def __str__(self):
        return "\033[" + self.color.value + (";1" if self.bold else "") + (";4" if self.underline else "") + (
            ";" + self.background_color.value if self.background_color is not None else "") + "m"


class StyledText:
    def __init__(self, text: str, style: Style):
        self.text = text
        self.style = style

    def __str__(self):
        return self.style.__str__() + self.text + "\033[0m"


class Console:
    @staticmethod
    def __print(message, with_type: bool = False, end: str = ""):
        if isinstance(message, str):
            Console.__print_str(message, with_type, end)
        elif isinstance(message, StyledText):
            Console.__print_str(message.__str__(), with_type, end)
        elif isinstance(message, int) or isinstance(message, float):
            Console.__print_number(message, with_type, end)
        elif isinstance(message, bool):
            Console.__print_bool(message, with_type, end)
        elif isinstance(message, list):
            if len(message) == 0:
                Console.__print_list(message, end)
            else:
                if isinstance(message[0], list):
                    Console.__print_list_of_lists(message)
                else:
                    Console.__print_list(message, end)
        else:
            print(message)

    @staticmethod
    def print(message, with_type: bool = False):
        Console.__print(message, with_type)

    @staticmethod
    def println(message="", with_type: bool = False):
        Console.__print(message, with_type, "\n")

    @staticmethod
    def __print_str(message: str, with_type: bool, end: str):
        msg = message
        if with_type:
            msg = f'{type(message).__name__}("{message}")'
        print(msg, end=end)

    @staticmethod
    def __print_number(message: int | float, with_type: bool, end: str):
        msg = message
        if with_type:
            msg = f'{type(message).__name__}({message})'
        print(msg, end=end)

    @staticmethod
    def __print_bool(message: bool, with_type: bool, end: str):
        msg = message
        if with_type:
            msg = f'{type(message).__name__}({message})'
        print(msg, end=end)

    @staticmethod
    def __print_list(message: list, end: str):
        print(message, end=end)

    @staticmethod
    def __print_list_of_lists(message: list[list]):
        for i in range(len(message)):
            Console.print(message[i])

    @staticmethod
    def input(message):
        return input(message)
