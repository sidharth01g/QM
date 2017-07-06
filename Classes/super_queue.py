import utilities
import token
from collections import deque


class Super_Queue:

    super_queue_dict = None
    queue_busy_dict = None
    max_size = 10000
    system_busy = None

    def __init__(self, token_types_list=["Default"]):

        try:
            if type(token_types_list) is not list:
                raise Exception("Class Super_Queue - __init__(..): " +
                                "'token_types_list' not of type 'list'")
            self.system_busy = True
            self.super_queue_dict = {}
            self.queue_busy_dict = {}
            # Initialize queue lengths to 0
            for token_type in token_types_list:
                self.super_queue_dict[token_type] = deque()
                self.queue_busy_dict[token_type] = False
            self.system_busy = False
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def get_token_types_list(self):
        try:
            return self.super_queue_dict.keys()
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def get_super_queue_dict(self):
        try:
            return self.super_queue_dict
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def get_queue_busy_dict(self):
        try:
            return self.queue_busy_dict
        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def put_in_queue(self, current_token):
        try:
            if not isinstance(current_token, token.Token):
                raise Exception("Class Super_Queue -put_in_queue(..): " +
                "current_token not instance of Token class")

            token_type = current_token.get_type()
            # Raise exception if current_token type is not a permissible one
            if token_type not in self.super_queue_dict.keys():
                raise Exception("Class Super_Queue -put_in_queue(..): " +
                                "current_token's type does not match any " +
                                "permissible type in Super Queue")

            while self.queue_busy_dict[token_type] is True:
                time.sleep(0.1)
                print('Waiting for queue (' + token_type + ') to be ' +
                      "available for insertion..")

            self.queue_busy_dict[token_type] = True
            self.super_queue_dict[token_type].appendleft(current_token)
            self.queue_busy_dict[token_type] = False

        except Exception as error:
            utilities.show_exception_info(error)
            raise error

    def pop_token_type(self, token_type):
        try:
            if type(token_type) is not str:
                raise Exception("Class Super_Queue -pop_token_type(..): " +
                                "token_type is not of type 'str'")

            self.queue_busy_dict[token_type] = True
            if token_type in self.get_token_types_list():
                try:
                    popped_token = (self.super_queue_dict[token_type]).pop()
                except Exception as pop_error:
                    # Set popped_token to None if deque is empty
                    pop_error_string = "pop from an empty deque" # empty deque
                    if pop_error_string.lower() in (str(pop_error)).lower():
                        popped_token = None
                    else:
                        raise pop_error
            else:
                raise Exception('Token type "' + token_type +
                                '" not valid in any of the queues')
            self.queue_busy_dict[token_type] = False
            return popped_token
        except Exception as error:
            utilities.show_exception_info(error)
            raise error
