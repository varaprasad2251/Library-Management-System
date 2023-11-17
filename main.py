import sys
import os
from red_black_tree import *

def is_file_exist(file_name):
    try:
        file_path = os.path.join(os.getcwd(), file_name)
        return os.path.exists(file_path)
    except FileNotFoundError as f:
        raise Exception(f)


def read_functions_from_file(file_path):
    with open(file_path, 'r') as f:
        # code = compile(file.read(), file_path, 'exec')
        # globals_dict = {}
        # exec(code, globals_dict)
        return f.readlines()


def write_output_to_file(file_path, output):
    with open(file_path, 'w') as file:
        file.write(output)


if __name__ == "__main__":

    input_filename = sys.argv[1]
    output_filename = input_filename + "_" + "output_file.txt"

    # Read functions from the input file
    if is_file_exist(input_filename):
        functions = read_functions_from_file(input_filename)
        rbtree = RedBlackTree()
        # Execute functions and collect results
        results = []
        for x in functions:
            results.append(eval("rbtree." + x))
            results.append(eval("print(rbtree.flip_count)"))
            if "Quit()" in x:
                print("exiting the loop")
                break

        # results = [eval("rbtree."+x), eval("rbtree."+x)  for x in functions]
    # for func_name, func in functions_dict.items():
    #     if callable(func):
    #         try:
    #             result = func(2, 3)  # Example input for each function
    #             results.append(f"{func_name}: {result}")
    #         except Exception as e:
    #             results.append(f"{func_name}: Error - {str(e)}")

    # Write results to the output file

        output_stream = ""
        for result in results:
            if result is not None:
                output_stream += (result + "\n")
        # results = "".join(results)
        write_output_to_file(output_filename, output_stream)

