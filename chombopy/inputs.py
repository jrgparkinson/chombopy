import re
import math


def read_inputs(inputs_file):
    """ Load up an inputs file and parse it into a dictionary """

    params = {}

    # Read in the file
    with open(inputs_file, "r") as f:
        file_data = f.readlines()

    for line in file_data:
        # print(line)
        # Ignore lines that are commented out
        if line.startswith("#"):
            continue

        # Remove anything after a #
        line = re.sub(r"#[^\n]*[\n]", "", line)

        parts = re.findall(r"^([^=]*)=(.*)$", line)

        # parts = line.split('=')
        # if len(parts) > 1:
        if parts:
            match = parts[0]
            key = match[0].strip()
            val = match[1].strip()

            # Convert to float/int as appropriate
            if isint(val):
                val = int(val)
            elif isfloat(val):
                val = float(val)

            params[key] = val

    # print(params)
    return params


def write_inputs(location, params, ignore_list=None, do_sort=True):
    """
     Write out a set of parameters to an inputs file
    """
    output_file = ""

    key_list = list(params.keys())
    if do_sort:
        key_list.sort()

    for key in key_list:
        if not ignore_list or key not in ignore_list:

            if isinstance(params[key], list):
                key_val = " ".join([str(a) for a in params[key]])

            else:
                key_val = str(params[key])

            output_file += "\n" + key + "=" + key_val

    with open(location, "w") as f:
        f.write(output_file)


def isfloat(value):
    """
    Determine if value is a float
    """
    try:
        float_val = float(value)
        if float_val == value or str(float_val) == value:
            return True
        else:
            return False
    except ValueError:
        return False


def isint(value):
    """
    Determines if value is an integer
    """

    try:
        int_val = int(value)

        if int_val == value or str(int_val) == value:
            return True
        else:
            return False
    except ValueError:
        return False


def string_to_array(string, conversion=None):
    """ Convert a string separated by spaces to an array, i.e.
    a b c -> [a,b,c]
     """

    if isinstance(string, list):
        return string

    # Default: convert to list of ints
    if not conversion:
        conversion = int

    parts = string.split(" ")
    array = [conversion(i) for i in parts]
    return array


def array_to_string(array):
    """ Convert an array to a string with the elements separated by spaces i.e.
    [a,b,c] -> a b c
    """
    str_array = [str(a) for a in array]
    string = " ".join(str_array)
    return string


def is_power_of_two(n):
    """ Determine if a number if a power of 2 """
    test = math.log(n) / math.log(2)

    if round(test) == test:
        return True
    else:
        return False


def add_params(default_params, extra_params):
    """ Add params from extra_params to defaultParams """

    for k, v in extra_params.items():
        default_params[k] = v

    return default_params
