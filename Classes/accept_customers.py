import token
import super_queue
import token_generator
import utilities


def instantiate(token_types_list, no_of_token_generators):
    try:
        if type(no_of_token_generators) is not int:
            raise Exception("Error in instantiate(..): " +
                            "no_of_token_generators no an integer")
        token_generators_list = []
        for i in range(0, no_of_token_generators):
            token_generators_list.append(
                token_generator.Token_Generator(token_types_list))
        sq = super_queue.Super_Queue(["Type A", "Type B"])
        return token_generators_list, sq
    except Exception as error:
        utilities.show_exception_info(error)
        raise error


def accept_customer(generators_list, sq, toke_type_requested, generator_index):
    """
    Issues a token of the requested type, prints it and inserts it in the queue
    """
    try:
        if type(generator_index) is not int:
            raise Exception("Error in accept_customer(..): " +
                            "generator_index not of type 'int'")
        if generator_index >= len(generators_list):
            raise Exception("Error in accept_customer(..): " +
                            "generator_index exceeds size of generators_list")
        if type(toke_type_requested) is not str:
            raise Exception("Error in accept_customer(..): " +
                            "toke_type_requested is not of type 'str'")

    except Exception as error:
        utilities.show_exception_info(error)
        raise error
