import typing

DATAFIELD_TYPE = {
	"string" : str,
	"bool" : bool,
	"int" : int,
	"float" : float,
	"comment" : str
}

DATAFIELD_ARGUMENT = {
	"type",
	"allowNone",
	"default",
	"selectValue"
}

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
		if key not in DATAFIELD_ARGUMENT:
			return False
	
	if 'selectValue' in schema:
		if type(schema["selectValue"]) != list:
			return False
		for value in schema["selectValue"]:
			if type(value) != schema_type:
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
