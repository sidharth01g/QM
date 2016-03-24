from imports import *

token_generator = None
super_queue = None

class Token:
    
    number = None
    type = None

    def __init__(self, number, type):
        self.set_number(number)
        self.set_type(type)

    def set_number(self, n):
        self.number = n

    def set_type(self, type):
        self.type = type

    def get_number(self):
        return self.number

    def get_type(self):
        return self.type


class Counter:
    
    number = None
    types = None
    current_token = None

    def __init__(self, number, types, current_token):
        self.set_number(number)
        self.set_types(types)
        self.set_current_token(current_token)

    def set_number(self, number):
        self.number = number

    def set_types(self, types):
        self.types = types

    def set_current_token(self):
        self.current_token = current_token

    def get_number(self):
        return self.number

    def get_types(self):
        return self.types

    def get_current_token(self):
        return self.current_token

    def get_queue_status(queue):
        """To be written
        """

    def get_token_from_queue(queue):
        """To be written
        """


class Token_Generator:
    

    token_types_list = None
    token_counts_dict = None

    def __init__(self, token_types_list):
        
        global token_generator
        if token_types_list:
            self.token_types_list = token_types_list
        else:
            self.token_types_list = ['Default']

        # Initialize all token counts to 0
        for token_type in self.token_types_list:
            token_counts_dict[token_type] = 0
        
        token_generator = self

    def set_token_types_list(self, token_types_list):
        self.token_types_list = token_types_list

    def set_token_counts_dict(self, token_counts_dict)
        self.token_counts_dict = token_counts_dict

    def get_token_types_list(self):
        return self.token_types_list

    def get_token_counts_dict(self, token_counts_list)
        return self.token_counts_dict

    def issue_token(self, token_type):
        number = token_counts_dict[token_type]
        new_token = Token(number, token_type)
        return new_token


class Super_Queue:

    queues_length_dict = None
    token_types_list = None

    def __init__(self, token_types_list):
        global super_queue
        set_token_types_list(token_types_list)
        queues_length_dict = {}
        # Initialize queue lengths to
        for token_type in token_types_list:
            queues_length_dict[token_type] = 0
        super_queue = self

    def set_queues_length_dict(self, queues_length_dict):
        self.queues_length_dict = queues_length_list

    def set_token_types_list(self, token_types_list):
        self.token_types_list = token_types_list
    
    def get_queues_length_dict(self):
        return self.queues_length_dict

    def get_token_types_list(self):
        return self.token_types_list
