"""Provides an API for talking to HD44780 compatible character LCDs."""
import time


class LcdApi:
    """Implements API for talking with HD44780 compatible character LCDs."""

    LCD_CLR = 0x01
    LCD_HOME = 0x02
    LCD_ENTRY_MODE = 0x04
    LCD_ENTRY_INC = 0x02
    LCD_ENTRY_SHIFT = 0x01
    LCD_ON_CTRL = 0x08
    LCD_ON_DISPLAY = 0x04
    LCD_ON_CURSOR = 0x02
    LCD_ON_BLINK = 0x01
    LCD_MOVE = 0x10
    LCD_MOVE_DISP = 0x08
    LCD_MOVE_RIGHT = 0x04
    LCD_FUNCTION = 0x20
    LCD_FUNCTION_8BIT = 0x10
    LCD_FUNCTION_2LINES = 0x08
    LCD_FUNCTION_10DOTS = 0x04
    LCD_FUNCTION_RESET = 0x30
    LCD_CGRAM = 0x40
    LCD_DDRAM = 0x80
    LCD_RS_CMD = 0
    LCD_RS_DATA = 1
    LCD_RW_WRITE = 0
    LCD_RW_READ = 1

    def __init__(self, num_lines, num_columns):
        """Initiate object's internal state."""
        self.num_lines = num_lines
        if self.num_lines > 4:
            self.num_lines = 4
        self.num_columns = num_columns
        if self.num_columns > 40:
            self.num_columns = 40
        self.cursor_x = 0
        self.cursor_y = 0
        self.implied_newline = False
        self.backlight = True
        self.display_off()
        self.backlight_on()
        self.clear()
        self.hal_write_command(self.LCD_ENTRY_MODE | self.LCD_ENTRY_INC)
        self.hide_cursor()
        self.display_on()

    def clear(self):
        """Clear LCD display and move cursor to top left corner."""
        self.hal_write_command(self.LCD_CLR)
        self.hal_write_command(self.LCD_HOME)
        self.cursor_x = 0
        self.cursor_y = 0

    def show_cursor(self):
        """Make cursor visible."""
        self.hal_write_command(
            self.LCD_ON_CTRL | self.LCD_ON_DISPLAY | self.LCD_ON_CURSOR
        )

    def hide_cursor(self):
        """Make cursor hidden."""
        self.hal_write_command(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY)

    def blink_cursor_on(self):
        """Make cursor blink."""
        self.hal_write_command(
            self.LCD_ON_CTRL
            | self.LCD_ON_DISPLAY
            | self.LCD_ON_CURSOR
            | self.LCD_ON_BLINK
        )

    def blink_cursor_off(self):
        """Make cursor solid (no blinking)."""
        self.hal_write_command(
            self.LCD_ON_CTRL | self.LCD_ON_DISPLAY | self.LCD_ON_CURSOR
        )

    def display_on(self):
        """Turn on LCD display."""
        self.hal_write_command(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY)

    def display_off(self):
        """Turn off LCD display."""
        self.hal_write_command(self.LCD_ON_CTRL)

    def backlight_on(self):
        """Turn the backlight on."""
        self.backlight = True
        self.hal_backlight_on()

    def backlight_off(self):
        """Turn the backlight off."""
        self.backlight = False
        self.hal_backlight_off()

    def move_to(self, cursor_x, cursor_y):
        """Move cursor to indicated position."""
        self.cursor_x = cursor_x
        self.cursor_y = cursor_y
        addr = cursor_x & 0x3F
        if cursor_y & 1:
            addr += 0x40
        if cursor_y & 2:
            addr += self.num_columns
        self.hal_write_command(self.LCD_DDRAM | addr)

    def putchar(self, char):
        """Write character to LCD at current cursor position.

        Advances the cursor by one position.
        """
        if char == "\n":
            if self.implied_newline:
                pass
            else:
                self.cursor_x = self.num_columns
        else:
            self.hal_write_data(ord(char))
            self.cursor_x += 1
        if self.cursor_x >= self.num_columns:
            self.cursor_x = 0
            self.cursor_y += 1
            self.implied_newline = char != "\n"
        if self.cursor_y >= self.num_lines:
            self.cursor_y = 0
        self.move_to(self.cursor_x, self.cursor_y)

    def putstr(self, string):
        """Write string to LCD at current cursor position."""
        for char in string:
            self.putchar(char)

    def custom_char(self, location, charmap):
        """Write character to one of 8 CGRAM locations."""
        location &= 0x7
        self.hal_write_command(self.LCD_CGRAM | (location << 3))
        self.hal_sleep_us(40)
        for i in range(8):
            self.hal_write_data(charmap[i])
            self.hal_sleep_us(40)
        self.move_to(self.cursor_x, self.cursor_y)

    def hal_backlight_on(self):
        """Allow HAL layer to turn the backlight on.

        If desired, a derived HAL class will implement this function.
        """
        pass

    def hal_backlight_off(self):
        """Allow HAL layer to turn backlight off.

        If desired, a derived HAL class will implement this function.
        """
        pass

    def hal_write_command(self, cmd):
        """Write command to LCD.

        It is expected that a derived HAL class will implement this function.
        """
        raise NotImplementedError

    def hal_write_data(self, data):
        """Write data to LCD.

        It is expected that a derived HAL class will implement this function.
        """
        raise NotImplementedError

    def hal_sleep_us(self, usecs):
        """Sleep for some time (given in microseconds)."""
        time.sleep_us(usecs)
