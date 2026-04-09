import numbers

from library.datafield.type import *

def validate(schema:dict) -> bool:
	if not "type" in schema:
		return False

	if type(schema["type"]) != str:
		return False

	if schema["type"] not in DATAFIELD_TYPE:
		return False
	
	if schema["type"] == "comment":
		return True

	field_type= schema["type"]
	python_type = DATAFIELD_TYPE[field_type]
	key_set = DATAFIELD_KEY[field_type]
	constraint_set = DATAFIELD_CONSTRAINT_PER_TYPE.get(field_type,set())

	for key,value in schema.items():
		if key not in key_set:
			return False
		
		if key == "default":
			if type(value) != python_type and value != None:
				return False
		elif type(value) != DATAFIELD_KEY_TYPE[key]:
			return False

	allowNone = schema.get("allowNone",True)
	default = schema.get("default")

	if not allowNone and default == None:
		return False

	if "constraint" in schema:
		constraint = schema["constraint"]
		if "type" not in constraint:
			return False
		if type(constraint["type"]) != str:
			return False
		if constraint["type"] not in constraint_set:
			return False 
		if constraint["type"] in CONSTRAINT_BINARY:
			if "value" not in constraint:
				return False
			if not isinstance(constraint["value"],numbers.Number):
				return False
			
		if constraint["type"] in CONSTRAINT_RANGE:
			if "value" not in constraint:
				return False
			if type(constraint["value"]) != list:
				return False
			if len(constraint["value"]) != 2:
				return False
			for value in constraint["value"]:
				if not isinstance(value,numbers.Number):
					return False
			if constraint["value"][0] > constraint["value"][1]:
				return False

		if constraint["type"] in CONSTRAINT_SET:
			if "value" not in constraint:
				return False
			if type(constraint["value"]) != list:
				return False
			for value in constraint["value"]:
				if not isinstance(value,python_type):
					return False


	return True	
