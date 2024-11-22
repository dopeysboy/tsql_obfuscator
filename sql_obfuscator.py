import os
import re
from helper_functions import *

def generate_set_vars(var_dict):
    return_str = ''
    
    for key in var_dict.keys():
        if key == ' ' or key == "'" or key == ";":
            return_str += f':setvar {var_dict[key]} "{key}"\n'
        elif key == '"':
            return_str += f":setvar {var_dict[key]} '{key}'\n"
        else:
            return_str += f':setvar {var_dict[key]} {key}\n'

    return return_str

def remove_empty_vals(list):
    return_list = list
    return_list.remove("")

    return return_list

def increment_letter_by_one(letter_seq):
    # A is 65 Z is 90
    # a is 97 z is 122
    return_str = letter_seq

    last_letter_ord = ord(letter_seq[-1])

    if (last_letter_ord < 90 and last_letter_ord >=65) or (last_letter_ord < 122 and last_letter_ord >= 97):
        last_letter_ord += 1
        return_str = return_str[0:-1] + chr(last_letter_ord)
    elif last_letter_ord == 90:
        return_str = return_str[0:-1] + 'a'
    elif last_letter_ord == 122:
        return_str = increment_letter_by_one(return_str[0:-1]) + 'A'

    return return_str

def get_next_var_name(dictionary):
    var_names = list(dictionary.values())
    var_names.sort()
    last_var_name = var_names[-1]

    next_var_name = increment_letter_by_one(last_var_name)
    return next_var_name

def token_list_to_var_dict(var_dict, token_list):
    return_dict = var_dict
    for token in token_list:
        if token not in return_dict.keys():
            next_var_name = get_next_var_name(return_dict)
            return_dict[token] = next_var_name

    return return_dict

def divvy_list(input_str, delim):
    pattern = re.compile(f'({re.escape(delim)})')
    return_list = re.split(pattern, input_str)
    return return_list

def split_str(str, split_dict):
    str_split_list = [str]
    return_list = []

    # ' ', 'i'
    # ['this is a string']
    # ['this', ' ', 'is', ' ', 'a', ' ', 'string']
    # ['th', 'i', 's', ' ', 'i', 's', ' ', 'a', ' ', 'str', 'i', 'ng']
    for char in split_dict.keys():
        for str in str_split_list:
            split_list = divvy_list(str, char)
            return_list += (split_list)

        str_split_list = return_list
        return_list = []
    
    return_list = str_split_list

    return return_list

def remove_comments(input_str):
    return re.sub(r'\s*--.*$', '', input_str, flags=re.MULTILINE)

def initialize_obf_dict():
    # TODO randomize values
    obf_dict = {
        " ": "A",
        ".": "B",
        ",": "C",
        ";": "D",
        "(": "E",
        ")": "F",
        "'": "G",
        "\"": "H",
        "_": "I"
    }
    return obf_dict

def main():
    working_dir = os.path.dirname(__file__)

    original_script = read_file(working_dir, "sample_sql.sql")
    var_dict = initialize_obf_dict()

    modified_script = remove_comments(original_script)
    modified_script = newlines_to_space(modified_script)

    script_token_list = split_str(modified_script, var_dict)
    script_token_list = remove_empty_vals(script_token_list)

    var_dict = token_list_to_var_dict(var_dict, script_token_list)

    output_str = generate_set_vars(var_dict)

    for token in script_token_list:
        output_str += f'$({var_dict[token]})'
    
    write_file(working_dir, "output_sql.sql", output_str)
    return 0

if __name__ == "__main__":
    main()
