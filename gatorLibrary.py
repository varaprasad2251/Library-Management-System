import sys
import os
from red_black_tree import *


def is_file_exist(file_name):
    # To check if given file exists in the current working directory
    try:
        file_path = os.path.join(os.getcwd(), file_name)
        return os.path.exists(file_path)
    except FileNotFoundError as f:
        raise Exception(f)


def read_functions_from_file(file_path):
    # To read contents of a file(with path as file_path) and return all lines as a list
    with open(file_path, 'r') as f:
        return f.readlines()


def write_output_to_file(file_path, output):
    # To write output content to file(with path as file_path)
    with open(file_path, 'w') as file:
        file.write(output)


if __name__ == "__main__":
    input_filename = sys.argv[1]   # Read input_file name from command-line argument
    output_filename = input_filename + "_" + "output_file.txt"

    # Read operations from the input file and execute each operation in input file.
    if is_file_exist(input_filename):
        functions = read_functions_from_file(input_filename)
        rbtree = RedBlackTree()
        results = []
        for x in functions:
            # class instance name appended to all operations before executing.
            # ';' is not expected at end of operation being called since python does not expect a ';' after method call.
            # using rstrip() to trim trailing ; if any. (Did not work properly in some cases)
            results.append(eval("rbtree." + x.rstrip(";")))
            if "Quit()" in x:
                break

    # Write results to the output file
        output_stream = ""
        for result in results:
            if result is not None:
                output_stream += (result + "\n")
        write_output_to_file(output_filename, output_stream)
