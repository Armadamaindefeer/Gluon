from library.utils.common import genUUID
from library.utils.database import getDatabase
import copy

def getObject(uuid : str) -> dict:
	return getDatabase()[uuid]

def MetaData(uuid:str):
	return getObject(uuid)["MetaData"]

def Qualifier(uuid:str):
	return getObject(uuid)["Qualifier"]

def isContainer(uuid : str) -> bool:
	return MetaData(uuid)["IsContainer"]

def isCountUnit(uuid : str) -> bool:
	return MetaData(uuid)["IsCountUnit"]

def Count(uuid : str) -> tuple[int|float,str,str]:
	return MetaData(uuid)["Count"]

def getChild(uuid : str) -> list[str] :
	return MetaData(uuid)["StoredUUID"]

def getParent(uuid : str) -> str :
	return MetaData(uuid)["ContainerUUID"]

def getUUID(uuid : str) -> str :
	return MetaData(uuid)["ObjectUUID"]

def getType(uuid : str) -> str :
	return MetaData(uuid)["Type"]

#############################################
#
# Object Data test
#
#############################################

def isEmpty(uuid : str) -> bool:
	return len(MetaData(uuid)["StoredUUID"]) == 0

def isStackable(uuid : str) -> bool:
	return isEmpty(uuid)


def getPrettyName(targetObjectUUID : str) -> str:
	text = f"{getType(targetObjectUUID)}< {targetObjectUUID} >"
	return (f"{text}{(' : '+ Qualifier(targetObjectUUID)['name']) if 'name' in Qualifier(targetObjectUUID) and Qualifier(targetObjectUUID)['name'] != '' else ''}")

def prettyPrintName(targetObject : str):
	print(getPrettyName(targetObject))

def getPrettyChild(targetObjectUUID: str) -> str:
	text = ""
	if len(getChild(targetObjectUUID)) > 0:
		text = "Child	: \n"
		for i,child_uuid in enumerate(getChild(targetObjectUUID)):
			text += f"[{i}] : {getPrettyName(child_uuid)}\n"
	return text

def prettyPrintChild(targetObject : str):
	print(getPrettyChild(targetObject))

def prettyPrint(toPrintUUID : str):

	prettyPrintName(toPrintUUID)
	print("MetaData	: ")

	print(f"\t- IsContainer : {isContainer(toPrintUUID)}")
	print(f"\t- IsCountUnit : {isCountUnit(toPrintUUID)}")
	print(f"\t- Count : {Count(toPrintUUID)[0]} {Count(toPrintUUID)[2] if Count(toPrintUUID)[2] != None else ''}")

	prettyPrintChild(toPrintUUID)

	print("Qualifier	: ")
	for name, value in Qualifier(toPrintUUID).items():
		if type(value) == str:
			print(f"\t- {name} : \"{value}\"")
		elif (type(value) == list or type(value) == tuple )and len(value) == 3 and (type(value[0]) == int or type(value[0]) == float):
			print(f"\t- {name} : {value[0]} {value[2]}")
		else:
			print(f"\t- {name} : {value}")

def copyObject(objectUUID :str,modification:dict) -> dict:
	newObject = copy.deepcopy(getObject(objectUUID))
	newObject["MetaData"]["ObjectUUID"] = genUUID(getDatabase())
	for namespace,data in modification.items():
		for key, keyData in data.items():
			newObject[namespace][key] = keyData
	return newObject
