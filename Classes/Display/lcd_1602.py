import smbus
import time
import logging
i2c_bus_busy = None


class LCD_1602_Default_Settings:
    def __init__(self, device_address):

        # Define some device parameters
        self.I2C_ADDR  = device_address # I2C device address
        self.LCD_WIDTH = 16   # Maximum characters per line

        # Define some device constants
        self.LCD_CHR = 1 # Mode - Sending data
        self.LCD_CMD = 0 # Mode - Sending command

        self.LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
        self.LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
        self.LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
        self.LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

        self.LCD_BACKLIGHT  = 0x08  # On
        #LCD_BACKLIGHT = 0x00  # Off

        self.ENABLE = 0b00000100 # Enable bit

        # Timing constants
        # self.E_PULSE = 0.0005
        # self.E_DELAY = 0.0005
        self.E_PULSE = 0.0005
        self.E_DELAY = 0.00001


class LCD_1602:
    def __init__(self, display_settings, bus):
        self.settings = display_settings
        self.bus = bus

    def lcd_init(self):
    # Initialise display
        self.lcd_byte(0x33, self.settings.LCD_CMD)  # 110011 Initialise
        self.lcd_byte(0x32, self.settings.LCD_CMD)  # 110010 Initialise
        self.lcd_byte(0x06, self.settings.LCD_CMD)  # 000110 Cursor move direction
        self.lcd_byte(0x0C, self.settings.LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
        self.lcd_byte(0x28, self.settings.LCD_CMD)  # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01, self.settings.LCD_CMD)  # 000001 Clear display
        time.sleep(self.settings.E_DELAY)

    def lcd_byte(self, bits, mode):
        # Send byte to data pins
        # bits = the data
        # mode = 1 for data
        #        0 for command

        bits_high = mode | (bits & 0xF0) | self.settings.LCD_BACKLIGHT
        bits_low = mode | ((bits<<4) & 0xF0) | self.settings.LCD_BACKLIGHT

        # High bits
        print '**********', type(self.settings.I2C_ADDR), type(bits_high)
        self.bus.write_byte(self.settings.I2C_ADDR, bits_high)
        self.lcd_toggle_enable(bits_high)

        # Low bits
        self.bus.write_byte(self.settings.I2C_ADDR, bits_low)
        self.lcd_toggle_enable(bits_low)

    def lcd_toggle_enable(self, bits):
        # Toggle enable
        time.sleep(self.settings.E_DELAY)
        self.bus.write_byte(self.settings.I2C_ADDR,
                            (bits | self.settings.ENABLE))
        time.sleep(self.settings.E_PULSE)
        self.bus.write_byte(self.settings.I2C_ADDR,
                            (bits & ~self.settings.ENABLE))
        time.sleep(self.settings.E_DELAY)

    def lcd_string(self, message, line):
        # Send string to display

        message = message.ljust(self.settings.LCD_WIDTH," ")

        self.lcd_byte(line, self.settings.LCD_CMD)

        for i in range(self.settings.LCD_WIDTH):
            self.lcd_byte(ord(message[i]), self.settings.LCD_CHR)


def show_message(logger, lcd_address, line_number, text, bus=None,
                 initialize=False):
    global i2c_bus_busy
    max_lines = 2
    try:
        if bus is None:
            bus = smbus.SMBus(1)
        line_addresses = [0x80, 0xC0, 0x94, 0xD4]
        line_address = line_addresses[line_number - 1]
        if type(line_number) is not int:
            message = ("Line number not of type 'int'")
            logger.exception(message)
            raise Exception(message)
        if line_number not in range(1, max_lines + 1):
            message = ("Invalid line number")
            logger.exception(message)
            raise Exception(message)
        if type(text) is not str:
            message = ("text is not of type 'str'")
            logger.exception(message)
            raise Exception(message)
        if not isinstance(bus, smbus.SMBus):
            message = ("'bus' not instance of 'smbus.SMBus'")
            logger.exception(message)
            raise Exception(message)

        settings0 = lcd_1602.LCD_1602_Default_Settings(lcd_address)
        i2c_manager = lcd_1602.LCD_1602(settings0, bus)

        max_attempts = 20
        interval = 0.1
        for i in range(0, max_attempts):
            if i2c_bus_busy is True:
                time.sleep(interval)
            else:
                i2c_bus_busy = True
                if initialize is True:
                    i2c_manager.lcd_init()
                i2c_manager.lcd_string(text, line_address)
                i2c_bus_busy = False
                break

    except Exception as error:
        print(str(error))
        raise error
