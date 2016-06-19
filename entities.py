from imports import *

token_generator = None
super_queue = None


class Token:

    number = None
    token_type = None
    busy = None

    def __init__(self, number, token_type):
        try:
            self.busy = True
            self.number = number
            self.token_type = token_type
            self.busy = False
        except Exception as e:
            show_exception_info(e)

    def set_number(self, n):
        self.busy = True
        self.number = n
        self.busy = False

    def set_type(self, type):
        self.busy = True
        self.type = type
        self.busy = False

    def set_busy(self, busy):
        self.busy = busy

    def is_busy(self):
        return self.busy

    def get_number(self):
        return self.number

    def get_type(self):
        return self.token_type


class Counter:

    number = None
    token_types = None
    current_token = None
    busy = None  # True or False

    def __init__(self, number, token_types):
        try:
            self.busy = True
            self.number = number
            self.token_types = token_types
            self.busy = False
        except Exception as e:
            show_exception_info(e)

    def set_number(self, number):
        self.busy = True
        self.number = number
        self.busy = False

    def set_types(self, types):
        self.busy = True
        self.types = types
        self.busy = False

    def set_current_token(self, current_token):
        self.busy = True
        self.current_token = current_token

    def set_busy(self, busy):
        self.busy = busy

    def get_number(self):
        return self.number

    def get_types(self):
        return self.token_types

    def get_current_token(self):
        return self.current_token

    def is_busy(self):
        return self.busy

    def release_token(self):
        self.current_token = None
        self.set_busy(False)

    def simulate_serve_token(self, current_token, service_time):
        try:
            self.set_current_token(current_token)
            time.sleep(service_time)
            self.release_token()
        except Exception as e:
            show_exception_info(e)


class Token_Generator:

    global super_queue

    token_types_list = None
    token_counts_dict = None
    busy = None

    def __init__(self, token_types_list):
        try:
            global token_generator
            self.busy = True
            if token_types_list is not None:
                self.token_types_list = token_types_list
            else:
                self.token_types_list = ['Default']

            # Initialize all token counts to 0
            self.token_counts_dict = {}
            for token_type in self.token_types_list:
                self.token_counts_dict[token_type] = 0
            token_generator = self
            self.busy = False
        except Exception as e:
            show_exception_info(e)

    def set_token_types_list(self, token_types_list):
        self.busy = True
        self.token_types_list = token_types_list
        self.busy = False

    def set_token_counts_dict(self, token_counts_dict):
        self.busy = True
        self.token_counts_dict = token_counts_dict
        self.busy = False

    def set_busy(self, busy):
        self.busy = busy

    def get_token_types_list(self):
        return self.token_types_list

    def get_token_counts_dict(self):
        return self.token_counts_dict

    def get_new_token(self, token_type):
        try:
            self.busy = True
            number = self.token_counts_dict[token_type] + 1
            self.token_counts_dict[
                token_type] = self.token_counts_dict[token_type] + 1
            new_token = Token(number, token_type)
            self.busy = False
            return new_token
        except Exception as e:
            show_exception_info(e)

    def is_busy(self):
        return self.busy


class Super_Queue:

    super_queue_dict = None
    queue_busy_dict = None
    max_size = 10000
    system_busy = None

    def __init__(self, token_types_list):
        try:
            self.system_busy = True
            global super_queue
            self.super_queue_dict = {}
            self.queue_busy_dict = {}
            # Initialize queue lengths to 0
            for token_type in token_types_list:
                self.super_queue_dict[token_type] = deque()
                self.queue_busy_dict[token_type] = False
            # Assuming a single Super_Queue instance is present in the project
            super_queue = self
            self.system_busy = False
        except Exception as e:
            show_exception_info(e)

    def get_token_types_list(self):
        return self.super_queue_dict.keys()

    def get_super_queue_dict(self):
        return self.super_queue_dict

    def get_queue_busy_dict(self):
        return self.queue_busy_dict

    def put_in_queue(self, token):
        try:
            token_type = token.get_type()
            while self.queue_busy_dict[token_type] is True:
                time.sleep(0.1)
                print('Waiting for queue (' + token_type + ') to be free..')
            if token_type in self.get_token_types_list():
                self.queue_busy_dict[token_type] = True
                self.super_queue_dict[token_type].appendleft(token)
                self.queue_busy_dict[token_type] = False
            else:
                print(
                    'Token type ' +
                    token_type +
                    ' not allowed in any of the queues')
        except Exception as e:
            show_exception_info(e)

    def remove_from_queue(self, token_type):
        try:
            self.queue_busy_dict[token_type] = True
            print('$'*5+token_type)
            if token_type in self.get_token_types_list():
                popped_token = self.super_queue_dict[token_type].pop()
            else:
                print(
                    'Token type ' +
                    token_type +
                    ' not valid in any of the queues')
            self.queue_busy_dict[token_type] = False
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

    def send_token_to_counter_and_service(self):
        global counters_list, super_queue
        try:
            while(True):
                for counter in counters_list:
                    if counter.is_busy() is True:
                        continue
                    super_queue_dict = super_queue.get_super_queue_dict()
                    for queue_type, queue in super_queue_dict.items():
                        if (queue_type in counter.get_types() and
                                len(queue) > 0):
                            self.show_queue_status()
                            if super_queue.get_queue_busy_dict()[queue_type] is True:
                                continue
                            popped_token = super_queue.remove_from_queue(
                                queue_type)
                            if popped_token is None:
                                # Potentially terminate program?? Verify
                                return
                            print('\n\nPopped token no: ' + str(popped_token.get_number()) + '-' + popped_token.get_type() + str(popped_token) + '. Sending it to counter.' + str(counter.get_number()) + ': ' + str(counter.get_types()))
                            self.show_queue_status()
                            service_time = 5 
                            counter.simulate_serve_token(popped_token, service_time)
        except Exception as e:
            show_exception_info(e)

    def issue_token(self, token_type):
        try:
            global token_generator, super_queue
            new_token = token_generator.get_new_token(token_type)
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
                counters_list.append(Counter(counter_number, supported_tokens_list))
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

    def show_queue_status(self):
        try:
            global super_queue
            super_queue_dict = super_queue.get_super_queue_dict()
            msg = "Queues status:"
            print('\n' + msg + '\n' + '-'*len(msg))
            for queue_type, queue in super_queue_dict.items():
                print(queue_type + ":" + str(queue))

        except Exception as e:
            show_exception_info(e)

    def all_counters_busy(self):
        try:
            global counters_list
            for counter in counters_list:
                if counter.is_busy() is False:
                    return False
            return True
        except Exception as e:
            show_exception_info(e)
