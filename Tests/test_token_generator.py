import test_utilities
test_utilities.add_folders()
import token_generator
import utilities


def test_0():
    utilities.show_heading("Creating token generator objects...")
    try:
        generator0 = token_generator.Token_Generator()
    except Exception as error:
        utilities.show_exception_info(error)
    try:
        generator1 = token_generator.Token_Generator(["Type A", "Type B"])
    except Exception as error:
        utilities.show_exception_info(error)
    try:
        generator2 = token_generator.Token_Generator(True)
    except Exception as error:
        utilities.show_exception_info(error)


def test_1():
    try:
        generator0 = token_generator.Token_Generator()
    except Exception as error:
        utilities.show_exception_info(error)
    try:
        generator0.set_token_types_list(token_types_list=["A", "B"])
        print generator0.get_token_types_list()
    except Exception as error:
        utilities.show_exception_info(error)
    try:
        generator0.set_token_counts_dict(token_counts_dict={"A": 45, "B": 1})
    except Exception as error:
        utilities.show_exception_info(error)
    try:
        generator0.set_busy(busy=False)
    except Exception as error:
        utilities.show_exception_info(error)
    try:
        test_token = generator0.get_new_token(token_type="A")
    except Exception as error:
        utilities.show_exception_info(error)

    try:
        test_token = generator0.get_new_token(token_type="B")
    except Exception as error:
        utilities.show_exception_info(error)
    try:
        print generator0.is_busy()
    except Exception as error:
        utilities.show_exception_info(error)

    try:
        generator0.print_token("test_token")
    except Exception as error:
        utilities.show_exception_info(error)

    generator0.print_token(test_token)
    generator0.print_token(test_token)


test_1()
