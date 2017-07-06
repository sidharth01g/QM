import os
import sys


def add_folders():
    this_file = os.path.realpath(__file__)
    this_dir = os.path.dirname(this_file)
    parent_dir = os.path.abspath(os.path.join(this_dir, os.pardir))

    directories_list = ['Classes']
    for dirname in directories_list:
        classes_dir_path = os.path.abspath(parent_dir + '/' + dirname)

        if not os.path.exists(classes_dir_path):
            raise Exception("Path '%s' does not exists " %classes_dir_path)

        if classes_dir_path not in sys.path:
            try:
                sys.path.insert(0, classes_dir_path)
                # print sys.path
            except Exception as error:
                print("ERROR: " + str(error))
