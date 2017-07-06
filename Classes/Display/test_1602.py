import lcd_1602
import time
import smbus
import logging
i2c_bus_busy = None

def test_0():
    try:
        LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
        LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
        LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
        LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

        bus = smbus.SMBus(1) # Rev 2 Pi uses 1
        settings0 = lcd_1602.LCD_1602_Default_Settings(0x3f)
        i2c_manager = lcd_1602.LCD_1602(settings0, bus)
        i2c_manager.lcd_init()
        i2c_manager.lcd_string("RPiSpy         <",LCD_LINE_1)
        i2c_manager.lcd_string("asdsa          <",LCD_LINE_2)
        time.sleep(20)
    except KeyboardInterrupt:
      pass
    finally:
        # Clears display in interrupt (^C)
        i2c_manager.lcd_byte(0x01, settings0.LCD_CMD)


def show_message(logger, lcd_address, line_number, text, bus, initialize=False):
    global i2c_bus_busy
    max_lines = 2
    try:
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

bus = smbus.SMBus(1)
logger = logging.getLogger(__name__)
show_message(logger=logger, lcd_address=0x3f, line_number=1,
             text="Hello, world!", bus=bus, initialize=True)
