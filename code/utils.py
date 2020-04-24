import os
import json
import jsonschema


class AMLConfigurationException(Exception):
    pass


def mask_parameter(parameter):
    print(f"::add-mask::{parameter}")


def load_json(path):
    paths = []
    for root, dirs, files in os.walk(os.path.split(path)[-1]):
        for filename in files:
            if ".parquet" in filename:
                path = os.path.join(root, filename)
                paths.append(path)
    print(f"Path List: {paths}")

    with open(path) as f:
        json_object = json.load(f)
    return json_object


def validate_json(data, schema, input_name):
    validator = jsonschema.Draft7Validator(schema)
    errors = validator.iter_errors(data)
    if len(errors) > 0:
        for error in errors:
            print(f"::error::JSON validation error: {error}")
        raise AMLConfigurationException(f"JSON validation error for '{input_name}'. Provided object does not match schema. Please check the output for more details.")
    else:
        print(f"::debug::JSON validation passed for '{input_name}'. Provided object does match schema.")
