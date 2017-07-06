import token
import utilities
import time
from multiprocessing import Process
import os
import lcd_1602
import settings
import sys
sys.modules["lcd_1602"] = lcd_1602



class Counter:

    number = None
    token_types_list = None
    current_token = None
    busy = None  # True or False

    def __init__(self, number="DefaultCounter", token_types_list=["Default"],
                 logger=None):
        try:
            if type(token_types_list) is not list:
                raise Exception("Class: Counter - __init__(..): " +
                                "token_types_list is not a list")
            if number is None:
                raise Exception("Class: Counter - __init__(..): " +
                                "number is 'None'")
            self.busy = True
            self.number = str(number)
            self.token_types_list = token_types_list
            self.busy = False
            self.logger = logger
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def set_number(self, number):
        try:
            self.busy = True
            self.number = str(number)
            self.busy = False
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def set_types(self, token_types_list):
        try:
            if type(token_types_list) is not list:
                raise Exception("Class: Counter - set_types(..): " +
                                "token_types_list is not a list")
            if any(type(token_type) is not str for
                   token_type in token_types_list):
                raise Exception("Class: Counter - set_types(..): " +
                                "token_types_list contains at least one " +
                                "element that is not of type 'str'")
            self.busy = True
            self.token_types_list = token_types_list
            self.busy = False
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def set_busy(self, busy):
        try:
            if type(busy) is not bool:
                raise Exception("Class: Counter - set_busy(..): " +
                                "'busy' is not of type 'bool'")
            self.busy = busy
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def get_number(self):
        try:
            return self.number
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def get_types(self):
        try:
            return self.token_types_list
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def get_current_token(self):
        try:
            return self.current_token
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def is_busy(self):
        try:
            return self.busy
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def set_current_token(self, current_token):
        try:
            if not isinstance(current_token, token.Token):
                raise Exception("Class: Counter - set_busy(..): " +
                                "'current_token' not instance of 'Token'")
            if self.busy is True:
                self.logger.warn("Counter busy. Cannot accept token")
                return
            self.busy = True
            self.current_token = current_token
            self.logger.debug(self.number + " - Servicing token: " +
                              str(self.current_token))
            self.update_display()
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def release_token(self):
        try:
            self.logger.debug(self.number + " - Releasing token: " +
                              str(self.current_token))
            self.current_token = None
            self.busy = False
            return self.current_token
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def update_display(self):
        # Interfacing commands to be added
        try:
            self.logger.info('Counter status:')
            all_settings = settings.Settings()
            # display_module_name = all_settings.display_module
            # display_module = getattr(Display, display_module_name)
            # display_module = lcd_1602

            print "#####################################", lcd_1602
            if self.current_token is None:
                self.logger.warn("No token at this counter to display!")
                lcd_1602.show_message(
                    logger=self.logger, lcd_address=0x3f, line_number=1,
                    text="NO token!", initialize=True)
            else:
                self.logger.info(str(self.number) + " - " +
                                 str(self.current_token.get_number()) + " - " +
                                 str(self.current_token.get_type()))

                line_1_text = str(self.current_token.get_type())
                line_2_text = str(self.current_token.get_number())
                lcd_1602.show_message(
                    logger=self.logger, lcd_address=0x3f, line_number=1,
                    text=line_1_text, initialize=True)
                lcd_1602.show_message(
                    logger=self.logger, lcd_address=0x3f, line_number=2,
                    text=line_2_text, initialize=True)
            print('\n')
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def fetch_token_from_super_queue(self, sq, polling_duration=0):
        """
        # Threading features not yet implemented !!!!!!!!!!!!!!!!
        Scans super_queue for 'polling_duration' and attempts to get a token
        whose type is supported by the current counter

        Arguments:
        sq: super_queue instance
        polling_duration: time (in seconds). Super_queue will be
            scanned over and over for this duration if it happens to return
            None for popped_token
        """
        try:
            if self.busy is True:
                self.logger.warn("Counter busy. Cannot accept token")
                return
            start_time = time.time()
            popped_token = None
            def scan_and_pop():
                time_now = time.time()
                while (time_now < (start_time + polling_duration)):
                    for token_type in self.token_types_list:
                       popped_token = sq.pop_token_type(token_type)
                       if popped_token is not None:
                           self.set_current_token(current_token=popped_token)
                           return
            def scan_and_pop_no_threading():
                for token_type in self.token_types_list:
                   popped_token = sq.pop_token_type(token_type)
                   if popped_token is not None:
                       self.set_current_token(current_token=popped_token)
                       return
                if popped_token is None:
                    self.logger.warn("No tokens in super queue for " +
                                     "this counter")
            # scan_and_pop()
            scan_and_pop_no_threading()

        except Exception as error:
            utilities.show_exception_info(error)
            raise error
