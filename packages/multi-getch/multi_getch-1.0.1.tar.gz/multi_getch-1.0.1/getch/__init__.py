"""
Multiplatform Getch
"""

import sys

__all__ = ['getch']

if sys.platform == 'win32':
    import msvcrt

    def getch():
        """
        Read a keypress and return the resulting character as a byte string.

        This function is compatible on Windows with getch() function from the MSVCRT library.
        """

        return msvcrt.getch()

else:
    import termios
    import tty

    def getch():
        """
        Read a keypress and return the resulting character as a byte string.

        This function is compatible on Unix Systems and is designed to be as similar as possible to
        getch() on Windows.
        """

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1).encode()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return ch