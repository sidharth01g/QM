#!/usr/bin/env python
import test_utilities
test_utilities.add_folders()
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
    def __init__(self, threadID, sq, token_generator, requested_token_type):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.sq = sq
        self.token_generator = token_generator
        self.requested_token_type = requested_token_type

    def run(self):
        new_token = self.token_generator.get_new_token(
            self.requested_token_type)
        print("New token: ", new_token)
        self.sq.put_in_queue(new_token)
        print("Queue- " + new_token.get_type())
        print(self.sq.get_super_queue_dict()[self.requested_token_type])


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


def main():
    generators_list, sq = accept_customers.instantiate(["Type A", "Type B"], 3)
    counter_a = counter.Counter(number="Counter X",
                                token_types_list=["Type A"])
    counter_b = counter.Counter(number="Counter Y",
                                token_types_list=["Type A", "Type B"])

    thread_id = -1
    accept_threads_list = []
    while 1:
        ch = getchar()
        if ch == 'q':
            exit()
        process_list = []
        print '\nYou pressed: ', ch

        if ch == 'a':
            thread_id += 1
            type_requested = "Type A"
            accept_threads_list.append(
                Accept_Customer_Thread(threadID=thread_id, sq=sq,
                                       token_generator=generators_list[0],
                                       requested_token_type=type_requested))
            accept_threads_list[len(accept_threads_list) -1].start()

        if ch == 's':
            thread_id += 1
            type_requested = "Type B"
            accept_threads_list.append(
                Accept_Customer_Thread(threadID=thread_id, sq=sq,
                                       token_generator=generators_list[1],
                                       requested_token_type=type_requested))
            accept_threads_list[len(accept_threads_list) -1].start()

        if ch == 'k':
            if counter_a.is_busy() is False:
                print("Fetching token..")
                counter_a.fetch_token_from_super_queue(sq, 10)
            else:
                print("Releasing token..")
                counter_a.release_token()
                counter_a.update_display()

        if ch == 'l':
            if counter_b.is_busy() is False:
                print("Fetching token..")
                counter_b.fetch_token_from_super_queue(sq, 10)
            else:
                print("Releasing token..")
                counter_b.release_token()
                counter_b.update_display()


    for process in process_list:
        process.join()
    for accept_thread in accept_threads_list:
        accept_thread.join()

main()
