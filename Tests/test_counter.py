import test_utilities
test_utilities.add_folders()
import super_queue
import utilities
import token
import counter


def test_0():
    try:
        # To do: check if token_types list has values permitted in settings file
        counter_a = counter.Counter("Counter A", ["Type A"])
        counter_b = counter.Counter("Counter B", ["Type B"])
    except Exception as error:
        utilities.show_exception_info(error)
    try:
        counter_a.set_number("First Counter")
    except Exception as error:
        utilities.show_exception_info(error)
    try:
        counter_a. set_types(token_types_list=["Type A"])
    except Exception as error:
        utilities.show_exception_info(error)
    try:
        counter_a.set_busy(busy=True)
    except Exception as error:
        utilities.show_exception_info(error)
    try:
        print counter_a.get_number()
    except Exception as error:
        utilities.show_exception_info(error)
    try:
        print counter_a.get_types()
    except Exception as error:
        utilities.show_exception_info(error)
    try:
        new_token = token.Token(25, "Fried chicken")
        counter_a.set_current_token(new_token)
    except Exception as error:
        utilities.show_exception_info(error)
    try:
        print "Current token: ", counter_a.get_current_token()
    except Exception as error:
        utilities.show_exception_info(error)
    try:
        print "Releasing current token"
        counter_a.release_token()
        print counter_a.get_current_token()
        counter_a.update_display()
    except Exception as error:
        utilities.show_exception_info(error)




test_0()
