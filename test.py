from entities import *
"""Insert functions for customer_entry and customer_service and make them
threads
"""

def test():
    global token_generator, super_queue, counters_list, queue_manager

    queue_manager = Queue_Manager()
    queue_manager.initialize_token_generator(
        ['Phone Bills', 'Electricity Bills'])

    counters_dict = {'A1': ['Phone Bills'],
                     'B1': ['Electricity Bills'],
                     'C1': ['Phone Bills', 'Electricity Bills']}
    queue_manager.initialize_counters_list(counters_dict)

    token_types_list = ['Phone Bills', 'Electricity Bills']
    queue_manager.initialize_super_queue(token_types_list)
    queue_manager.issue_token('Phone Bills')
    queue_manager.issue_token('Phone Bills')
    queue_manager.issue_token('Electricity Bills')
    queue_manager.show_queue_status()


if __name__ == '__main__':
    test()
