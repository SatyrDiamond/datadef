
import argparse
import datadef
import json

parser = argparse.ArgumentParser()
parser.add_argument("-i", default=None)
parser.add_argument("-d", default=None)
args = parser.parse_args()

in_file = args.i
datadef_file = args.d

if in_file == None:
	print('Input File Not Found')
	exit()

if datadef_file == None:
	print('DataDef File Not Found')
	exit()

in_stream = open(in_file, 'rb')

output_data, global_vars, pointers, pointset = datadef.parse(in_stream, datadef_file)


print(json.dumps(output_data, indent=4, sort_keys=True, default=str))






