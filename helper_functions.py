import os
import re

def read_file(path_to_file, file_name):
    stream = open(os.path.join(path_to_file, file_name))
    file_contents = stream.read()
    stream.close()
    return file_contents

def write_file(path_to_file, file_name, file_contents):
    stream = open(os.path.join(path_to_file, file_name), "w")
    stream.write(file_contents)
    stream.close()
    return 0

def newlines_to_space(string):
    return_str = string.replace('\n', ' ')
    return_str = return_str.replace('\r\n', ' ')
    return_str = re.sub(r'\s+', ' ', return_str, flags=re.MULTILINE)
    
    return return_str
