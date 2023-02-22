import json
import os
import yaml
import argparse
from pykwalify.core import Core

########## Usage ##########
# usage: Convert-ParameterFile.py [-h] --parameter-file PARAMETER_FILE --schema-file SCHEMA_FILE [--output-file OUTPUT_FILE]
#
# required parameters:
#   --parameter-file PARAMETER_FILE
#                         file location of the input yaml parameter file
#   --schema-file SCHEMA_FILE
#                         file location of the schema yaml file
#
# optional arguments:
#   -h, --help            show this help message and exit
#   --output-file OUTPUT_FILE
#                         name of output file to generate

########## Argument check ##########
parser = argparse.ArgumentParser()
parser.add_argument("--parameter-file",type=str, help="file location of the input yaml parameter file",required=True)
parser.add_argument("--schema-file",type=str, help="file location of the schema yaml file",required=True)
parser.add_argument("--output-file",type=str, help="file location and name of the output file",required=False)
args = parser.parse_args()

parameter_file = args.parameter_file
schema_file = args.schema_file

if args.output_file is not None:
    output_file = args.output_file
else:
    output_file = parameter_file.replace('.yml','.json')
    
########## Validate existance of input files ##########
print(f"Input parameter file is: {parameter_file}. Checking if it exists...")
try:
    parameters_check = os.path.exists(parameter_file)
    if not parameters_check:
        raise Exception('Parameter file not found.')
except Exception as e:
    print(f"The parameter file [{parameter_file}] could not be found. Make sure to include the path in the file name.")
    print(e)
    exit(1)

print(f"Input schema file is: {schema_file}. Checking if it exists...")
try:
    schema_check = os.path.exists(schema_file)
    if not schema_check:
        raise Exception('Schema file not found.')
except Exception as e:
    print(f"The schema file [{schema_file}] could not be found. Make sure to include the path in the file name.")
    print(e)
    exit(1)

########## Validate parameter file with the schema file ##########
print('Validating the parameter file using the schema file...')
c = Core(source_file=parameter_file, schema_files=[schema_file])
try:
    c.validate(raise_exception=True)
except Exception as e:
    print("An error occured during the schema validation of the parameter file:")
    print(e)
    exit(1)

########## Transform parameter file to json file ##########
print('Transforming the yaml parameter file to a json file...')
with open(parameter_file) as f:
    parameters = yaml.safe_load(f)
    output_parameters = {}
    for k, v in parameters.items():
        output_parameters[k] = {"value": v}

    output_JSON = {
        "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
        "contentVersion": "1.0.0.0",
        "parameters": output_parameters
    }

with open(output_file, 'w') as outputFile:
    json.dump(output_JSON, outputFile, indent=4)
