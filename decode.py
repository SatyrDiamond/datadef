
import argparse
import datadef

parser = argparse.ArgumentParser()
parser.add_argument("-i", default=None)
parser.add_argument("-d", default=None)
args = parser.parse_args()

in_file = args.i
datadef_file = args.d

in_stream = open(in_file, 'rb')

output_data, global_vars, pointers, pointset = datadef.parse(in_stream, datadef_file)

print(output_data)
#print(global_vars)
#print(pointers)
#print(pointset)












