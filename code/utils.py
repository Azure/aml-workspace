import sys


def required_parameters_provided(parameters, keys, message="Required parameter not found in your parameters file. Please provide a value for the following key: "):
    for key in keys:
        if not parameters.get(key, None):
            print(f"::error::{message}" + key)
            sys.exit()
