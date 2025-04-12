def add_Numbers(number: int, number2: int) -> int:
    """
    This Function will add up the numbers you provide.

    ## Args:
        - number (int): the first integer to add.
        - number2 (int): the second integer to add.

    ## Returns:
        - int: the result of addition.
    """
    return number + number2


def subtract_Numbers(number: int, number2: int) -> int:
    """
    This Function will subtract the second number from the first.

    ## Args:
        - number (int): the number to subtract from.
        - number2 (int): the number to subtract.

    ## Returns:
        - int: the result of subtraction.
    """
    return number - number2


def multiply_Numbers(number: int, number2: int) -> int:
    """
    This Function will multiply the numbers you provide.

    ## Args:
        - number (int): the first number to multiply.
        - number2 (int): the second number to multiply.

    ## Returns:
        - int: the result of multiplication.
    """
    return number * number2


def divide_Numbers(number: int, number2: int) -> float:
    """
    This Function will divide the first number by the second.

    ## Args:
        - number (int): the dividend.
        - number2 (int): the divisor.

    ## Returns:
        - float: the result of division.
    """
    return number / number2


def modulo_Numbers(number: int, number2: int) -> int:
    """
    This Function will return the remainder when the first number is divided by the second.

    ## Args:
        - number (int): the dividend.
        - number2 (int): the divisor.

    ## Returns:
        - int: the remainder of the division.
    """
    return number % number2


def power_Numbers(number: int, number2: int) -> int:
    """
    This Function will raise the first number to the power of the second.

    ## Args:
        - number (int): the base number.
        - number2 (int): the exponent.

    ## Returns:
        - int: the result of exponentiation.
    """
    return number**number2


__all__ = [
    "power_Numbers",
    "add_Numbers",
    "subtract_Numbers",
    "multiply_Numbers",
    "modulo_Numbers",
]
