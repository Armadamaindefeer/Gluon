from library.common import Source, error, info
import library.cmdUtils.cmdUtils as cutils
from library.dataField import default_schema


def getNumber(type,text):
	number = 0
	valid = False
	while not valid:
		try:
			number = type(cutils.Input(text,"OBJECT_CREATOR"))
		except ValueError:
			error("Invalid litteral, try again...")
		else:
			valid = True
	return number

@Source("OBJECT_CREATOR")
def getCount():
	return getNumber(int,"How many of that object should be created")

@Source("OBJECT_CREATOR")
def getProperty(name,datafield:dict):
	allowNone = False
	selectValue_list = []
	default = default_schema(datafield)

	if "allowNone" in datafield:
		allowNone = datafield["allowNone"]

	if "selectValue" in datafield:
		selectValue_list = datafield["selectValue"]
		value =  cutils.Choice(f"Choose a value for {name}","OBJECT_CREATOR",selectValue_list,allowNone)
		return selectValue_list[value]

	match datafield["type"]:

		case "string":
			return cutils.Input(f"Enter a value for {name}","OBJECT_CREATOR")
		case "bool" : 
			return cutils.Validate(f"Enter a value for {name}","OBJECT_CREATOR",False)
		case "int":
			return getNumber(int,f"Enter an integral value for {name}")
		case "float":
			return getNumber(float,f"Enter a float value for {name}")
		case "comment":
			error("Comment SHOULD NOT be used as valid datafield")
			return default
