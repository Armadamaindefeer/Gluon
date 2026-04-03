import typing
from library.datafield.type import *

def validate_schema(schema:dict) -> bool:
	if not "type" in schema:
		return False

	if type(schema["type"]) != str:
		return False

	if schema["type"] not in DATAFIELD_TYPE:
		return False

	schema_type = DATAFIELD_TYPE[schema["type"]]

	if schema["type"] == "comment":
		return True

	for key in schema:
		if key not in KEY_BASE:
			return False
	
	if 'selectValue' in schema:
		if type(schema["selectValue"]) != list:
			return False
		for value in schema["selectValue"]:
			if type(value) != schema_type:
				return False

	if 'constraint' in schema:
		constraint = schema["constraint"]
		if type(constraint) != dict:
			return False
		if not "type" in constraint:
			return False
		if type(constraint["type"]) != str:
			return False
		if constraint["type"] not in DATAFIELD_CONSTRAINT_PER_TYPE[schema["type"]]:
			return False

		if not "value" in constraint:
			return False

		if constraint["type"] in CONSTRAINT_BINARY:
			if type(constraint["value"]) not in (int,float):
				return False
		if constraint["type"] in CONSTRAINT_RANGE:
			if type(constraint["value"]) != list:
				return False
			if constraint["type"] == "range" and len(constraint["value"]) != 2:
				return False
			for element in constraint["value"]:
				if constraint["type"] == "range":
					if type(element) not in (int,float):
						return False
				if constraint["type"] == "set":
					if type(element) != schema_type:
						return False

	allowNone = False
	if "allowNone" in schema:
		if type(schema["allowNone"]) != bool:
			return False
		allowNone = schema["allowNone"]

	if "default" in schema :
		if type(schema["default"]) == None:
			if not allowNone:
				return False
		elif type(schema["default"]) != schema_type:
			return False

	return True

def validate_value(value,schema:dict) -> bool:
	schema_type = DATAFIELD_TYPE[schema["type"]]
	allowNone = False
	if "allowNone" in schema:
		allowNone = schema["allowNone"]

	if type(value) == None:
		if not allowNone:
			return False
		else:
			return True
	
	if type(value) != schema_type:
		return False

	if "selectValue" in schema:
		availableValue = set()
		availableValue.update(schema["selectValue"])
		if "default" in schema:
			availableValue.add(schema["default"])

		if value not in availableValue :
			return False

	return True

def default_schema(schema:dict):
	if "default" in schema:
		return schema["default"]
	
	if "allowNone" in schema:
		if schema["allowNone"]:
			return None

	if "selectValue" in schema:
		return schema["selectValue"][0]

	return DATAFIELD_TYPE[schema["type"]]()

def default_list(list:typing.Iterable[dict]):
	return (default_schema(schema) for schema in list)

def default_dict(schema_dict:dict):
	return {name:default_schema(schema) for name,schema in schema_dict.items()}
