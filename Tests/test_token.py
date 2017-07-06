import test_utilities

test_utilities.add_folders()

import token


def test_token_0():
    test_token = token.Token(10, "asdf")
    test_token.set_number(12)
    
    #test_token.set_type(12)

    #test_token.set_busy("jbkj")

    print test_token.is_busy()
    print test_token.get_number()
    print test_token.get_type()

test_token_0()
