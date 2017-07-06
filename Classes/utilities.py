import os
import sys
import logging
import coloredlogs


def show_exception_info(e):
    msg = "\nException info"
    print(msg + "\n" + "=" * len(msg))
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print("Exception: " + str(e))
    print("Exception class: " + str(exc_type))
    print("Exception in: " + fname)
    print("Line: " + str(exc_tb.tb_lineno) + "\n")


def show_heading(message, character="="):
    """
    Shows message with underline
    """
    if type(message) is not str or type(character) is not str:
        raise Exception("Invalid argument types to show_heading(..)")
    print("\n" + message + "\n" + character * len(message))


# Create a logger object.
def get_logger(log_filepath='default.log'):
    """
    Returns logger object set to log to "log_filepath"
    """
    if type(log_filepath) is not str:
        raise Exception('utilities.py - get_logger(..): ' +
                        "'log_filepath' not of type 'str'")

    logging.basicConfig(filename=log_filepath)
    logger = logging.getLogger('QM Logger')
    # Initialize coloredlogs.
    coloredlogs.install(level='DEBUG')
    return logger
