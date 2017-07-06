import token_generator
import utilities
import accept_customers
import super_queue
import accept_customers
import counter
from multiprocessing import Process
import os
import threading


class Accept_Customer_Thread(threading.Thread):
    def __init__(self, threadID, sq, token_generator, requested_token_type,
                 logger, lock):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.sq = sq
        self.token_generator = token_generator
        self.requested_token_type = requested_token_type
        self.logger = logger
        self.lock = lock


    def run(self):
        self.lock.acquire()
        new_token = self.token_generator.get_new_token(
            self.requested_token_type)
        self.logger.debug("New token: " + str(new_token))
        self.logger.info("Adding token " + str(new_token) + " to queue")
        self.sq.put_in_queue(new_token)
        self.logger.debug("Queue- " + new_token.get_type())
        self.logger.debug(str(
            (self.sq.get_super_queue_dict()[self.requested_token_type])))
        self.lock.release()
