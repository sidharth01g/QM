#!/usr/bin/env python

import token_generator
import utilities
import accept_customers
import super_queue
import accept_customers
import counter
import os
import thread_classes
import configuration
import counter
import threading
import smbus


def getchar():
   # Returns a single character from standard input
   import tty, termios, sys
   fd = sys.stdin.fileno()
   old_settings = termios.tcgetattr(fd)
   try:
      tty.setraw(sys.stdin.fileno())
      ch = sys.stdin.read(1)
   finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
   return ch


def service_counter(counter_x, sq, logger):
    """
    Fetch/release a token at counter_x
    """
    try:
        if not isinstance(counter_x, counter.Counter):
            raise Exception("service_counter(..): 'counter_x' not an " +
                            "instance of 'Counter'")
        if not isinstance(sq, super_queue.Super_Queue):
            raise Exception("service_counter(..): 'sq' not an " +
                            "instance of 'Super_Queue'")
        if counter_x.is_busy() is False:
            logger.info("Fetching token..")
            counter_x.fetch_token_from_super_queue(sq, 10)
        else:
            logger.info("Releasing token..")
            counter_x.release_token()
            counter_x.update_display()
    except Exception as error:
        utilities.show_exception_info(error)
        raise error


def instantiate_super_queue(config_dict, token_types_keyword):
    """
    Instantiate super queue with separate queues each token type specified under
    "Token_Types" in the config file
    """
    try:
        if type(config_dict) is not dict:
            raise Exception("instantiate_super_queue(..): " +
                            "'config_dict' not of type 'dict'")
        if type(token_types_keyword) is not str:
            raise Exception("instantiate_super_queue(..): " +
                            "'token_types_keyword' not of type 'str'")
        token_types_list = config_dict[token_types_keyword]
        sq = super_queue.Super_Queue(token_types_list)
        return sq

    except Exception as error:
        utilities.show_exception_info(error)
        raise error


def instantiate_counters(config_dict, counters_keyword, token_types_keyword,
                         input_keys_keyword, logger):
    """
    Instantiate counters with the repective names and types specified in the
    config file
    """
    try:
        if type(config_dict) is not dict:
            raise Exception("instantiate_counters(..): " +
                            "'config_dict' not of type 'dict'")
        if type(counters_keyword) is not str:
            raise Exception("instantiate_counters(..): " +
                            "'counters_keyword' not of type 'str'")
        if type(token_types_keyword) is not str:
            raise Exception("instantiate_counters(..): " +
                            "'token_types_keyword' not of type 'str'")
        if type(input_keys_keyword) is not str:
            raise Exception("instantiate_counters(..): " +
                            "'input_keys_keyword' not of type 'str'")

        counters_dict = config_dict[counters_keyword]

        counters_list = []
        for counter_name, counter_attributes in counters_dict.iteritems():
            token_types_list = counter_attributes[token_types_keyword]
            new_counter = counter.Counter(counter_name, token_types_list,
                                          logger)
            new_counter_key_config = counter_attributes[input_keys_keyword]
            logger.debug("Counters instance:\n" + str(counter_name) + ': ' +
                         str(counter_attributes))
            counters_list.append((new_counter, new_counter_key_config))
            new_counter = None
        return counters_list
    except Exception as error:
        raise error
        utilities.show_exception_info(error)


def instantiate_token_generators(config_dict, token_generators_keyword, logger):
    """
    Instantiate token generators with the repective names and types specified
    in the config file
    """
    try:
        if type(config_dict) is not dict:
            raise Exception("instantiate_token_generators(..): " +
                            "'config_dict' not of type 'dict'")
        if type(token_generators_keyword) is not str:
            raise Exception("instantiate_counters(..): " +
                            "'token_generators_keyword' not of type 'str'")

        token_generator_dict = config_dict[token_generators_keyword]
        logger.debug("Token generators dictionary:\n" +
                     str(token_generator_dict))

        token_generators_list = []
        for generator_x, generator_x_attrib in token_generator_dict.iteritems():
            new_token_types_dicts_list = generator_x_attrib.values()
            new_token_types_list = []
            for new_token_types_dict in new_token_types_dicts_list:
                new_token_types_list += new_token_types_dict.keys()
            new_generator = token_generator.Token_Generator(
                new_token_types_list, logger)
            new_generator.set_name(generator_x)
            token_generators_list.append(new_generator)
            new_generator = None
        return token_generators_list, token_generator_dict
    except Exception as error:
        raise error
        utilities.show_exception_info(error)


def get_types_dict(generator_x, token_generator_dict, token_types_keyword):
    try:
        # print "*" * 20, token_generator_dict, generator_x
        for gen_name, gen_attrib in token_generator_dict.iteritems():
            if generator_x.get_name() == gen_name:
                return gen_attrib[token_types_keyword]
        return None
    except Exception as error:
        raise error
        utilities.show_exception_info(error)


def main():
    try:
        # Configuration parameters:
        token_types_keyword = "Token_Types"
        token_generators_keyword = "Token_Generators"
        counters_keyword = "Counters"
        input_keys_keyword = "Input_Keys"
        process_keyword = "Process"

        # Get logger object
        logger = utilities.get_logger()
        logger.info("Starting objects instatiation")
        # Config file complete path
        # config_file_path = (
        #     "/home/sidharth/Dropbox/QM-Redesign/Configuration/config-0.yaml")
        config_file_path = (
            "/home/pi/Documents/QM-Redesign/Configuration/config-0.yaml")
        cm = configuration.Config_Manager(config_file_path)
        config_dict = cm.read_config()
        logger.debug("Configuration Dictionary:\n" + str(config_dict))

        # Instantiate Super_Queue
        sq = instantiate_super_queue(config_dict, token_types_keyword)
        logger.debug("Super_Queue instance:\n" + str(sq))

        # Instantiate counters and store them in a list
        counters_list = instantiate_counters(config_dict, counters_keyword,
                                             token_types_keyword,
                                             input_keys_keyword, logger)
        logger.debug("Counters list:\n" + str(counters_list))

        # Instantiate token generators
        token_generators_list, token_generator_dict = (
            instantiate_token_generators(
                config_dict, token_generators_keyword, logger))
        logger.debug("Token generators list:\n" + str(counters_list))

        logger.debug("Initializing bus..")
        bus = smbus.SMBus(1)


        logger.info("Starting main loop")

        thread_id = -1
        accept_threads_list = []
        # Thread lock
        lock = threading.Lock()
        while True:
            ch = getchar()
            logger.debug("Pressed key: " + ch)
            if ch == 'q':
                exit()

            # Token generators: issue tokens upon press of assigned keys
            for generator_x in token_generators_list:
                name_x = generator_x.get_name()
                types_dict_x = get_types_dict(generator_x, token_generator_dict,
                                              token_types_keyword)
                for key, value in types_dict_x.iteritems():
                    if value == ch:
                        type_requested = key
                        logger.debug("Requested type: " + type_requested)
                        thread_id += 1
                        logger.debug("Creating thread for token type: " +
                                     type_requested)
                        logger.debug("Supported types: " +
                                     str(generator_x.get_token_types_list()))
                        accept_threads_list.append(
                            thread_classes.Accept_Customer_Thread(
                                threadID=thread_id, sq=sq,
                                token_generator=generator_x,
                                requested_token_type=type_requested,
                                logger=logger, lock=lock))
                        logger.debug("Thread: " + str(thread_id))
                        accept_threads_list[len(accept_threads_list) -1].start()
                        logger.debug("Threads (issue token) list: " +
                                     str(accept_threads_list))

            # Scan counters to check if key pressed is that for processing
            # tokens at any of the counters
            for counter_x in counters_list:
                counter_instance = counter_x[0]
                counter_process_key = counter_x[1][process_keyword]
                if ch == counter_process_key:
                    service_counter(counter_instance, sq, logger)
                    break

        for accept_thread in accept_threads_list:
            accept_thread.join()

    except Exception as error:
        utilities.show_exception_info(error)
        exit(1)


if __name__ == "__main__":
    main()
