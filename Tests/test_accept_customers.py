import test_utilities
test_utilities.add_folders()
import token_generator
import utilities
import accept_customers


def test_0():
    try:
        permitted_token_types_list = ["Type A", "Type B", "Type C"]
        generators_list, sq = accept_customers.instantiate(
            permitted_token_types_list, 3)
        accept_customers.accept_customer(generators_list, sq, "123", 2)
    except Exception as error:
        utilities.show_exception_info(error)


test_0()
