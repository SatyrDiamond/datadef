
import json
import argparse
import os
import struct
import varint
import datadef
from io import BytesIO

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

def do_switch(input_stream, case_name, data_forcase):
	if case_name in datadef_cases:
		case_data = datadef_cases[case_name]
		for s_case_data in case_data:
			if data_forcase == s_case_data[0]: 
				return decode_part(input_stream, s_case_data[1])
			if s_case_data[0] == None:
				print('[info] cases: else from', bytes.hex(data_forcase), data_forcase)
				return decode_part(input_stream, s_case_data[1])

	else:
		print('[error] '+case_name+' is not found in defined cases.')
		exit()



def decode_part(input_stream, d_valtype):
	global global_vars
	global is_ended

	valuetype = d_valtype[0].split('.')

	## Bytes
	if valuetype[0] == 'skip':             input_stream.read(int(valuetype[1]))

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

	elif valuetype[0] == 'varint':         return varint.decode_stream(input_stream)
	elif valuetype[0] == 'varint_f':       return varint.decode_bytes(input_stream.read(4))

	elif valuetype[0] == 'raw':            return input_stream.read(int(valuetype[1]))
	elif valuetype[0] == 'raw_l':          return input_stream.read(int( decode_part(input_stream, d_valtype[1:]) ))
	elif valuetype[0] == 'raw_e':          return input_stream.read()

	elif valuetype[0] == 'string_n':       return string_fix(input_stream.read(int(valuetype[1])))
	elif valuetype[0] == 'string_l':       return string_fix(input_stream.read( decode_part(input_stream, d_valtype[1:]) ))

	elif valuetype[0] == 's_string_n':     return input_stream.read(int(valuetype[1])).split(b'\x00')[0]
	elif valuetype[0] == 's_string_l':     return input_stream.read( decode_part(input_stream, d_valtype[1:]) ).split(b'\x00')[0]

	elif valuetype[0] == 'string_t':       return readstring(input_stream)

	elif valuetype[0] == 'dstring_n':      return input_stream.read(int(valuetype[1])*2).decode()
	elif valuetype[0] == 'dstring_l':      return input_stream.read( decode_part(input_stream, d_valtype[1:])*2 ).decode()

	elif valuetype[0] == 'string_n':       return string_fix(input_stream.read(int(valuetype[1])))
	elif valuetype[0] == 'list_n':         return [decode_part(input_stream, d_valtype[1:]) for _ in range(int(valuetype[1]))]
	elif valuetype[0] == 'list_l':         return [decode_part(input_stream, d_valtype[2:]) for _ in range(int( decode_part(input_stream, d_valtype[1:]) ))]

	elif valuetype[0] == 'pair':           return [decode_part(input_stream, d_valtype[x+1].split('.')) for x in range(2)]
	elif valuetype[0] == 'mlist':          return [decode_part(input_stream, [p_valtype]) for p_valtype in d_valtype[1:]]

	elif valuetype[0] == 'keyval_n':
		output = {}
		for _ in range(int(valuetype[1])):
			kv_key = decode_part(input_stream, [d_valtype[1]])
			kv_val = decode_part(input_stream, [d_valtype[2]])
			output[kv_key] = kv_val
		return output

	elif valuetype[0] == 'keyval_l':
		output = {}
		for _ in range( decode_part(input_stream, [d_valtype[1]]) ):
			kv_key = decode_part(input_stream, [d_valtype[2]])
			kv_val = decode_part(input_stream, [d_valtype[3]])
			output[kv_key] = kv_val
		return output

	## DataDef
	elif valuetype[0] == 'getvar':         return global_vars[valuetype[1]]
	elif valuetype[0] == 'num':            return struct.unpack('B', input_stream.read(1))[0]
	elif valuetype[0] == 'currentpos':     return input_stream.tell()
	elif valuetype[0] == 'structure':      return decode_data(input_stream, valuetype[1])
	elif valuetype[0] == 'isolate':        
		is_isolated.append(0)
		data_size = decode_part(input_stream, [d_valtype[1]])
		outval = decode_part( BytesIO(input_stream.read(data_size) ), d_valtype[2:])
		is_isolated.remove(0)
		return outval
	elif valuetype[0] == 'end':      is_ended = True

	elif valuetype[0] == 'switch_raw':
		data_forcase = decode_part(input_stream, d_valtype[1:])
		return do_switch(input_stream, valuetype[1], data_forcase)

	else:
		print('unknown cmd:', valuetype[0])
		exit()


global_vars = {}
using_defs = []
pointers = {}
pointset = {}
varlist = {}

is_isolated = []

is_ended = False

def decode_data(input_stream, current_defname):
	global datadef_structs
	global using_defs
	global global_vars
	global is_isolated
	global is_ended

	if current_defname not in datadef_structs:
		exit('[error] '+current_defname+' is not defined')
	current_def = datadef_structs[current_defname]

	output_data = {}
	if current_defname not in using_defs:
		using_defs.append(current_defname)
		for def_part in current_def:

			if is_ended == True: break

			if len(def_part) == 3: 
				d_command, d_valtype, d_name = def_part

				print('[debug]', 
					'ISO' if is_isolated != [] else '   ', 
					str(input_stream.tell()).ljust(10), 
					current_defname.ljust(20), 
					d_command.ljust(13), 
					d_name.ljust(20), 
					' > '.join(d_valtype) )

				if d_command == 'magic': 
					hexdata = bytes.hex(decode_part(input_stream, d_valtype))
					if hexdata != d_name: 
						print('[datadef] magic not match', hexdata, d_name)
						exit()

				if d_command == 'magic_end': 
					hexdata = bytes.hex(decode_part(input_stream, d_valtype))
					if hexdata != d_name: 
						is_ended = True

				if d_command == 'part': 
					outval = decode_part(input_stream, d_valtype)
					if d_name != '': output_data[d_name] = outval

				if d_command == 'part_loop': 
					outval = []
					while is_ended == False and input_stream.tell() < input_stream.__sizeof__():
						outpart = decode_part(input_stream, d_valtype)
						outval.append(outpart)
					is_ended = False
					output_data[d_name] = outval

				if d_command == 'setvar': 
					outval = decode_part(input_stream, d_valtype)
					if d_name != '': global_vars[d_name] = outval

				if d_command == 'part_setvar':
					outval = decode_part(input_stream, d_valtype)
					
					if d_name != '': 
						output_data[d_name] = outval
						global_vars[d_name] = outval

				if d_command == 'pointer': pointers[d_name] = decode_part(input_stream, d_valtype)
				if d_command == 'pointset': pointset[d_name] = decode_part(input_stream, d_valtype)
				if d_command == 'varlist': varlist[d_name] = decode_part(input_stream, d_valtype)
				if d_command == 'part_varlist': 
					outval = decode_part(input_stream, d_valtype)
					if d_name != '': 
						output_data[d_name] = outval
						varlist[d_name] = outval

				if d_command == 'dataset_len': 
					datasetlen[d_name] = decode_part(input_stream, d_valtype)

				if def_part[0] == 'act_pointset': 
					t_structure, t_pointset = d_valtype[0].split('.')
					dataset = []
					oldpos = input_stream.tell()
					for pointer in pointset[t_pointset]:
						if pointer != 0:
							input_stream.seek(pointer)
							dataset.append(  decode_part(input_stream, ['structure.'+t_structure])  )
						else: dataset.append(None)

					output_data[d_name] = dataset
					input_stream.seek(oldpos)

				if def_part[0] == 'act_pointer': 
					t_structure, t_pointername = d_valtype[0].split('.')
					oldpos = input_stream.tell()
					input_stream.seek(pointers[t_pointername])
					output_data[d_name] = decode_part(input_stream, ['structure.'+t_structure])
					input_stream.seek(oldpos)

				if def_part[0] == 'act_varlist_rep':
					t_varlistname = d_valtype[0].split('.')
					dataset = []
					for vardata in varlist[t_varlistname[0]]:
						partdata = []
						for num in range(vardata):
							partdata.append(decode_part(input_stream, d_valtype[1:]))
						dataset.append(partdata)
					output_data[d_name] = dataset

				if def_part[0] == 'act_varlist_swi':
					t_caseset, t_varlistname = d_valtype[0].split('.')

					dataset = []
					for casedata in varlist[t_varlistname]:
						dataset.append(do_switch(input_stream, t_caseset, casedata))
					output_data[d_name] = dataset




			#if def_part[0] == 'math_pointset': 
			#	splitted_string = def_part[1].split('.')
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
	global datadef_structs
	global datadef_cases
	global is_ended

	datadef_stream = open(datadef_file, 'r')
	datadef_lines = datadef_stream.readlines()

	datadef_structs = {}
	current_struct = None

	datadef_cases = {}
	current_case = None

	for datadef_line in datadef_lines:
		splittedtext = [x.strip() for x in datadef_line.split('#')[0].strip().split('|')]

		if splittedtext != ['']:
			if splittedtext[0] == 'area_struct':
				print('[datadef] structure found: '+splittedtext[1])
				current_struct = splittedtext[1]
				datadef_structs[current_struct] = []
			elif splittedtext[0] == 'area_end':
				current_struct = None
				current_case = None


			elif splittedtext[0] == 'area_cases_raw':
				print('[datadef] cases (raw) found: '+splittedtext[1])
				current_case = splittedtext[1]
				datadef_cases[current_case] = []

			elif splittedtext[0] == 'case_issame': 
				if len(splittedtext) != 3: exit('[error] length in case_issame is not 3')
				datadef_cases[current_case].append([bytes.fromhex(splittedtext[2]), splittedtext[1].split('/')])

			elif splittedtext[0] == 'case_else': 
				datadef_cases[current_case].append([None, [splittedtext[1]]])

			else:
				if len(splittedtext) == 3:
					txttxt = splittedtext[0], splittedtext[1].split('/'), splittedtext[2]
					datadef_structs[current_struct].append(txttxt)
				else:
					print('[error] unknown cmd or length of Line is not 3')
					exit()

	output_data = decode_data(in_stream, 'main')
	return output_data, global_vars, pointers, pointset
