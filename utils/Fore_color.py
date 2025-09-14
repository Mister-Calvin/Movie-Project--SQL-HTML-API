from colorama import Fore


def fore_color_text(text, fore_color):
    """
    :param text: the text to be colored
    :param fore_color: the color of the text
    :return: reset the original color
    """
    return (f"{fore_color}{text}{Fore.RESET}")