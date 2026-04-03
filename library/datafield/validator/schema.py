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

	for key,value in schema.items():
		if key not in key_set:
			return False
		
		if key == "default":
			if type(value) != python_type and type(value) != None:
				return False
		elif type(value) != DATAFIELD_KEY_TYPE[key]:
			return False

	allowNone = False
	if "allowNone" in schema:
		allowNone = schema["allowNone"]

	if "default" in schema:
		if type(schema["default"]) == None and not allowNone:
			return False

	if "constraint" in schema:
		for constraint in schema["constraint"]:
			...

	return True	
