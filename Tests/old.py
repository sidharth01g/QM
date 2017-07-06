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
                    thread_classes.Accept_Customer_Thread(
                        threadID=thread_id, sq=sq,
                        token_generator=generators_list[0],
                        requested_token_type=type_requested))
                accept_threads_list[len(accept_threads_list) -1].start()

            if ch == 's':
                thread_id += 1
                type_requested = "Type B"
                accept_threads_list.append(
                    thread_classes.Accept_Customer_Thread(
                        threadID=thread_id, sq=sq,
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
