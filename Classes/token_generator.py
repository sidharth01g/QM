import utilities
import token
import time


class Token_Generator:

    token_types_list = None
    token_counts_dict = None
    busy = None
    name = None

    def __init__(self, token_types_list=['Default'], logger=None):
        try:
            if type(token_types_list) is not list:
                raise Exception("__init__(..): " +
                                "token_types_list is not of type list")

            self.busy = True
            self.token_types_list = token_types_list
            self.logger = logger

            # Initialize all token counts to 0
            self.token_counts_dict = {}
            for token_type in self.token_types_list:
                self.token_counts_dict[token_type] = 0

            self.busy = False
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def set_name(self, name):
        try:
            if type(name) is not str:
                raise Exception("Class Token_Generator - set_name(..): " +
                                "name is not of type 'str'")
            self.name = name
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def get_name(self):
        try:
            return self.name
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def set_token_types_list(self, token_types_list):
        try:
            if type(token_types_list) is not list:
                raise Exception("set_token_types_list(..): " +
                                "token_types_list is not of type list")
            if any (type(token_type) is not str for
                    token_type in token_types_list):
                raise Exception("set_token_types_list(..): " +
                                "Found one or more token_types that are " +
                                "not strings")
            self.busy = True
            self.token_types_list = token_types_list
            self.busy = False
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def set_token_counts_dict(self, token_counts_dict):
        try:
            if type(token_counts_dict) is not dict:
                raise Exception("set_token_counts_dict(..): " +
                                "token_counts_dict is not of type dict")
            if any (key not in self.token_types_list for
                    key in token_counts_dict.keys()):
                raise Exception("set_token_counts_dict(..): " +
                                "Found one or more invalid token types")
            if any (type(value) is not int for
                    value in token_counts_dict.values()):
                raise Exception("set_token_counts_dict(..): " +
                                "One or more count values is not of type int")
            self.busy = True
            self.token_counts_dict = token_counts_dict
            self.busy = False
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def set_busy(self, busy):
        try:
            if type(busy) is not bool:
                raise Exception("set_busy(..): " +
                                "busy status is not of type bool")
            self.busy = busy
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def get_token_types_list(self):
        try:
            return self.token_types_list
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def get_token_counts_dict(self):
        try:
            return self.token_counts_dict
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def get_new_token(self, token_type):
        try:
            if token_type not in self.token_types_list:
                raise Exception("get_new_token(..): " +
                                "Token type not in list of types for " +
                                "this token generator")
            self.busy = True
            number = self.token_counts_dict[token_type] + 1
            new_token = token.Token(number, token_type)
            self.token_counts_dict[token_type] = number
            self.print_token(new_token)
            self.busy = False
            return new_token
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def is_busy(self):
        try:
            return self.busy
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def print_token(self, current_token):
        try:
            if not isinstance(current_token, token.Token):
                raise Exception("print_token(..): " +
                                "current_token not of type Token")
            # Add printer interfacing/printing commands
            self.logger.info('Printing token: ' + current_token.get_type() +
                             ' - ' + str(current_token.get_number()))
            time.sleep(3)
            self.logger.info("Printed token " + str(current_token.get_number()))
        except Exception as error:
            utilities.show_exception_info(error)
            raise error
