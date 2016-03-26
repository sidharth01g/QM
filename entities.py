from imports import *

token_generator = None
super_queue = None


class Token:

    number = None
    type = None

    def __init__(self, number, type):
        try:
            self.set_number(number)
            self.set_type(type)
        except Exception as e:
            show_exception_info(e)

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
    busy = None  # True or False

    def __init__(self, number, types):
        try:
            self.set_number(number)
            self.set_types(types)
        except Exception as e:
            show_exception_info(e)

    def set_number(self, number):
        self.number = number

    def set_types(self, types):
        self.types = types

    def set_current_token(self, current_token):
        self.busy = True
        self.current_token = current_token

    def set_busy(self, busy):
        self.busy = busy

    def get_number(self):
        return self.number

    def get_types(self):
        return self.types

    def get_current_token(self):
        return self.current_token

    def is_busy(self):
        return self.busy

    def release_token(self):
        self.current_token = None
        self.busy = False


class Token_Generator:

    global super_queue

    token_types_list = None
    token_counts_dict = None

    def __init__(self, token_types_list):
        try:
            global token_generator
            if token_types_list:
                self.token_types_list = token_types_list
            else:
                self.token_types_list = ['Default']

            # Initialize all token counts to 0
            self.token_counts_dict = {}
            for token_type in self.token_types_list:
                self.token_counts_dict[token_type] = 0

            token_generator = self
        except Exception as e:
            show_exception_info(e)

    def set_token_types_list(self, token_types_list):
        self.token_types_list = token_types_list

    def set_token_counts_dict(self, token_counts_dict):
        self.token_counts_dict = token_counts_dict

    def get_token_types_list(self):
        return self.token_types_list

    def get_token_counts_dict(self):
        return self.token_counts_dict

    def get_new_token(self, token_type):
        try:
            number = self.token_counts_dict[token_type] + 1
            self.token_counts_dict[
                token_type] = self.token_counts_dict[token_type] + 1
            new_token = Token(number, token_type)
            return new_token
        except Exception as e:
            show_exception_info(e)


class Super_Queue:

    super_queue_dict = None
    max_size = 10000

    def __init__(self, token_types_list):
        try:
            global super_queue
            self.super_queue_dict = {}
            # Initialize queue lengths to 0
            for token_type in token_types_list:
                self.super_queue_dict[token_type] = deque()
            # Assuming a single Super_Queue instance is present in the project
            super_queue = self
        except Exception as e:
            show_exception_info(e)

    def get_token_types_list(self):
        return self.super_queue_dict.keys()

    def get_super_queue_dict(self):
        return self.super_queue_dict

    def put_in_queue(self, token):
        try:
            token_type = token.get_type()
            if token_type in self.get_token_types_list():
                self.super_queue_dict[token_type].appendleft(token)
            else:
                print(
                    'Token type ' +
                    token_type +
                    ' not allowed in any of the queues')
        except Exception as e:
            show_exception_info(e)

    def remove_from_queue(self, token_type):
        try:
            if token_type in self.get_token_types_list():
                popped_token = self.super_queue_dict[token_type].pop()
            else:
                print(
                    'Token type ' +
                    token_type +
                    ' not valid in any of the queues')
            return popped_token
        except Exception as e:
            show_exception_info(e)


class Queue_Manager:

    def __init__(self):
        try:
            global queue_manager, counters_list
            queue_manager = self
        except Exception as e:
            show_exception_info(e)

    def send_token_to_counter():
        global counters_list, super_queue
        try:
            while (True):
                for counter in counters_list:
                    if counter.is_busy() is False:
                        super_queue_dict = super_queue.get_super_queue_dict()
                        for queue_type, queue in super_queue_dict.items():
                            if (queue_type in counter.get_types() and
                                    len(queue) > 0):
                                popped_token = super_queue.remove_from_queue(
                                    remove_from_queue)
                                counter.set_current_token(popped_token)

        except Exception as e:
            show_exception_info(e)

    def issue_token(self, token_type):
        try:
            global token_generator, super_queue
            new_token = get_new_token(token_type)
            super_queue.put_in_queue(new_token)
        except Exception as e:
            show_exception_info(e)

    def initialize_token_generator(self, token_types_list):
        try:
            global token_generator
            token_generator = Token_Generator(token_types_list)
            return token_generator
        except Exception as e:
            show_exception_info(e)

    def initialize_counters_list(self, counters_dict):
        try:
            global counters_list
            counters_list = []
            for counter_number, supported_tokens_list in counters_dict.items():
                counters_list.append(Counter(counter_number, counter_number))
            return counters_list
        except Exception as e:
            show_exception_info(e)

    def initialize_super_queue(self, token_types_list):
        try:
            global super_queue
            super_queue = Super_Queue(token_types_list)
            return super_queue
        except Exception as e:
            show_exception_info(e)
