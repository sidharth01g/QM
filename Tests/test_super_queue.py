import test_utilities
test_utilities.add_folders()
import super_queue
import utilities
import token


def test_0():
    try:
        sq0 = super_queue.Super_Queue(["Type A", "Type B"])
    except Exception as error:
        utilities.show_exception_info(error)
    try:
        print sq0.get_token_types_list()
    except Exception as error:
        utilities.show_exception_info(error)
    try:
        print sq0.get_super_queue_dict()
    except Exception as error:
        utilities.show_exception_info(error)
    try:
        print sq0.get_queue_busy_dict()
    except Exception as error:
        utilities.show_exception_info(error)
    try:
        token0 = token.Token(200, "Type A")
        sq0.put_in_queue(token0)
    except Exception as error:
        utilities.show_exception_info(error)
    try:
        print("Popping..")
        popped_token = sq0.pop_token_type("Type A")
        print popped_token
        print sq0.get_super_queue_dict()
        popped_token = sq0.pop_token_type("Type A")
        print popped_token
        print sq0.get_super_queue_dict()
        popped_token = sq0.pop_token_type("Type A")
        print popped_token
        print sq0.get_super_queue_dict()
    except Exception as error:
        utilities.show_exception_info(error)


test_0()
