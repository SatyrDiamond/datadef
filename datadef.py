
import json
import argparse
import os
import struct
import datadef

def readstring(data):
	output = b''
	terminated = 0
	while terminated == 0:
		char = data.read(1)
		if char != b'\x00' and char != b'': output += char
		else: terminated = 1
	return output.decode('ascii')

def string_fix(inputtxt):
	return inputtxt.split(b'\x00')[0].decode().translate(dict.fromkeys(range(32)))



def decode_part(input_stream, d_valtype):
	global global_vars

	valuetype = d_valtype[0].split(',')

	if valuetype[0] == 'skip':             input_stream.read(int(valuetype[1]))

	elif valuetype[0] == 'num':            return struct.unpack('B', input_stream.read(1))[0]

	elif valuetype[0] == 'byte':           return struct.unpack('B', input_stream.read(1))[0]
	elif valuetype[0] == 's_byte':         return struct.unpack('b', input_stream.read(1))[0]

	elif valuetype[0] == 'short':          return struct.unpack('H', input_stream.read(2))[0]
	elif valuetype[0] == 'short_b':        return struct.unpack('>H', input_stream.read(2))[0]
	elif valuetype[0] == 's_short':        return struct.unpack('h', input_stream.read(2))[0]
	elif valuetype[0] == 's_short_b':      return struct.unpack('>h', input_stream.read(2))[0]

	elif valuetype[0] == 'int':            return struct.unpack('I', input_stream.read(4))[0]
	elif valuetype[0] == 'int_b':          return struct.unpack('>I', input_stream.read(4))[0]
	elif valuetype[0] == 's_int':          return struct.unpack('i', input_stream.read(4))[0]
	elif valuetype[0] == 's_int_b':        return struct.unpack('>i', input_stream.read(4))[0]

	elif valuetype[0] == 'float':          return struct.unpack('f', input_stream.read(4))[0]
	elif valuetype[0] == 'float_b':        return struct.unpack('>f', input_stream.read(4))[0]
	elif valuetype[0] == 'double':         return struct.unpack('d', input_stream.read(8))[0]
	elif valuetype[0] == 'double_b':       return struct.unpack('>d', input_stream.read(8))[0]

	elif valuetype[0] == 'raw':
		return input_stream.read(int(valuetype[1]))

	elif valuetype[0] == 'raw_l':
		val_len = decode_part(input_stream, d_valtype[1:])
		return input_stream.read(int(val_len))

	elif valuetype[0] == 'string_n':   
		return string_fix(input_stream.read(int(valuetype[1])))

	elif valuetype[0] == 'string_l':
		string_len = decode_part(input_stream, d_valtype[1:])
		return string_fix(input_stream.read(string_len))

	elif valuetype[0] == 'string_t':
		return readstring(input_stream)

	elif valuetype[0] == 'subdefine':
		return decode_data(input_stream, valuetype[1])

	elif valuetype[0] == 'list_n':
		return [decode_part(input_stream, d_valtype[1:]) for _ in range(int(valuetype[1]))]

	elif valuetype[0] == 'list_l':
		list_len = decode_part(input_stream, d_valtype[1:])
		return [decode_part(input_stream, d_valtype[2:]) for _ in range(int(list_len))]

	elif valuetype[0] == 'pair':
		first = decode_part(input_stream, d_valtype[1].split(','))
		second = decode_part(input_stream, d_valtype[2].split(','))
		return [first, second]

	elif valuetype[0] == 'getvar': return global_vars[valuetype[1]]

	else:
		print('unknown cmd:', valuetype[0])


global_vars = {}
using_defs = []
pointers = {}
pointset = {}

def decode_data(input_stream, current_defname):
	global datadef_defs
	global using_defs
	global global_vars
	current_def = datadef_defs[current_defname]

	output_data = {}
	if current_defname not in using_defs:
		using_defs.append(current_defname)
		for def_part in current_def:

			#print(input_stream.tell(), current_defname, def_part)

			if len(def_part) == 3: 
				d_command, d_valtype, d_name = def_part

				print(d_command, d_valtype, d_name)

				if d_command == 'header': 
					hexdata = bytes.hex(decode_part(input_stream, d_valtype))

					if hexdata != d_name:
						print('[datadef] header not match')
						exit()

				if d_command == 'part': 
					outval = decode_part(input_stream, d_valtype)
					if outval != None: output_data[d_name] = outval
				if d_command == 'setvar': global_vars[d_name] = decode_part(input_stream, d_valtype)
				if d_command == 'pointer': pointers[d_name] = decode_part(input_stream, d_valtype)
				if d_command == 'pointset': pointset[d_name] = decode_part(input_stream, d_valtype)

				if def_part[0] == 'act_pointset': 
					print(d_valtype[0].split(','))
					t_subdefine, t_pointset = d_valtype[0].split(',')

					dataset = []
					oldpos = input_stream.tell()
					for pointer in pointset[t_pointset]:
						if pointer != 0:
							input_stream.seek(pointer)
							dataset.append(  decode_part(input_stream, ['subdefine,'+t_subdefine])  )
						else:
							dataset.append(None)


					output_data[d_name] = dataset
					input_stream.seek(oldpos)


			#if def_part[0] == 'math_pointset': 
			#	splitted_string = def_part[1].split(',')
			#	vmathval = int(splitted_string[1])
			#	if splitted_string[0] == 'add': pointset[def_part[2]] = [x+vmathval for x in pointset[def_part[2]]]
			#	if splitted_string[0] == 'sub': pointset[def_part[2]] = [x-vmathval for x in pointset[def_part[2]]]
			#	if splitted_string[0] == 'div': pointset[def_part[2]] = [x/vmathval for x in pointset[def_part[2]]]
			#	if splitted_string[0] == 'mul': pointset[def_part[2]] = [x*vmathval for x in pointset[def_part[2]]]


	else: 
		print('no recurse')
		exit()

	using_defs.remove(current_defname)

	return output_data



def parse(in_stream, datadef_file):
	global datadef_defs

	datadef_stream = open(datadef_file, 'r')
	datadef_lines = datadef_stream.readlines()

	datadef_defs = {}

	current_subdef = None
	for datadef_line in datadef_lines:
		splittedtext = [x.strip() for x in datadef_line.split('#')[0].strip().split('|')]

		if splittedtext != ['']:
			if splittedtext[0] == 'def_start':
				current_subdef = splittedtext[1]
				datadef_defs[current_subdef] = []
			elif splittedtext[0] == 'def_end':
				current_subdef = None
			else:
				txttxt = splittedtext[0], splittedtext[1].split(':'), splittedtext[2]
				datadef_defs[current_subdef].append(txttxt)

	output_data = decode_data(in_stream, 'main')
	return output_data, global_vars, pointers, pointset
