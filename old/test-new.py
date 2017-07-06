#!/usr/bin/python3
from entities import *
"""Insert functions for customer_entry and customer_service and make them
threads
"""


def show_counters_status(counters_list):
    for counter in counters_list:
        print(
            'Counter: ' + counter.get_number() +
            'Status: ' + str(counter.is_busy()) +
            'Token number: ' + str(counter.get_current_token().get_number()) +
            'Token type: ' + counter.get_current_token().get_type())


def accept_customer():
    try:
        global token_generator, super_queue, counters_list, queue_manager
        while(True):
            time.sleep(10)
            queue_manager.issue_token('Electricity Bills')
            queue_manager.show_queue_status()
    except Exception as e:
        show_exception_info(e)

def service_queue():
    try:
        global token_generator, super_queue, counters_list, queue_manager
        while(True):
            time.sleep(0.5)
            queue_manager.send_token_to_counter_and_service()
            # queue_manager.show_queue_status()
    except Exception as e:
        show_exception_info(e)

def timer(name, delay, repeat):
    try:
        print("Timer " + name + " started")
        while repeat > 0:
                time.sleep(delay)
                print(name + ": " + time.ctime(time.time()))
                repeat = repeat - 1
        print("Timer " + name + " completed")
    except Exception as e:
        show_exception_info(e)

def test():
    try:
        global token_generator, super_queue, counters_list, queue_manager

        queue_manager = Queue_Manager()
        queue_manager.initialize_token_generator(
            ['Phone Bills', 'Electricity Bills'])

        counters_dict = {'A1': ['Phone Bills'],
                         'B1': ['Electricity Bills'],
                         'C1': ['Phone Bills', 'Electricity Bills']}
        """
        counters_dict = {'A1': ['Phone Bills'],
                         'C1': ['Phone Bills', 'Electricity Bills']}
        """
        queue_manager.initialize_counters_list(counters_dict)

        token_types_list = ['Phone Bills', 'Electricity Bills']
        queue_manager.initialize_super_queue(token_types_list)
        queue_manager.issue_token('Phone Bills')
        queue_manager.issue_token('Phone Bills')
        queue_manager.issue_token('Phone Bills')
        queue_manager.issue_token('Phone Bills')
        queue_manager.issue_token('Phone Bills')
        queue_manager.issue_token('Phone Bills')
        queue_manager.issue_token('Phone Bills')
        queue_manager.issue_token('Phone Bills')
        queue_manager.issue_token('Electricity Bills')
        queue_manager.issue_token('Electricity Bills')
        queue_manager.issue_token('Electricity Bills')
        queue_manager.show_queue_status()

        thread_accept_customer = Thread(target=accept_customer)
        thread_accept_customer.start()

        thread_service_customer = Thread(target=service_queue)
        thread_service_customer.start()

    except Exception as e:
        show_exception_info(e)

if __name__ == '__main__':
    test()
