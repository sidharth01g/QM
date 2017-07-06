import utilities

class Token:

    number = None  # allowed to be of any type
    token_type = None
    busy = None

    def __init__(self, number, token_type="Default", busy=False):
        try:
            if type(number) is not int:
                raise Exception("__init__(..): " +
                                "Token number not of type integer")
            if type(token_type) is not str:
                raise Exception("__init__(..): " +
                                "Token type not string")
            if type(busy) is not bool:
                raise Exception("__init__(..): " +
                                "Token busy status not boolean")
            if number < 0:
                raise Exception("__init__(..): " +
                                "Token number cannot be negative")
            self.number = number
            self.token_type = token_type
            self.busy = busy

        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def set_number(self, n):
        try:
            if type(n) is not int:
                raise Exception("set_number(..): " +
                                "Token number not of type integer")
            if n < 0:
                raise Exception("set_number(..): " +
                                "Token number cannot be negative")
            self.busy = True
            self.number = n
            self.busy = False

        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def set_type(self, token_type):
        try:
            if type(token_type) is not str:
                raise Exception("set_type(..): " +
                                "Token type not string")
            self.busy = True
            self.type = token_type
            self.busy = False
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def set_busy(self, busy):
        try:
            if type(busy) is not bool:
                raise Exception("set_busy(..): " +
                                "Token busy status not boolean")
            self.busy = busy
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def is_busy(self):
        try:
            return self.busy
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def get_number(self):
        try:
            return self.number
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def get_type(self):
        try:
            return self.token_type
        except Exception as error:
            utilities.show_exception_info(error)
            raise error
