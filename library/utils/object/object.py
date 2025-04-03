# Gluon , a terminal-based inventory manager
# Copyright (C) 2022-2025 Simon Alligand | Arma_mainfeer
# contact : simon.alligand@gmail.com

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from library.utils.common import genUUID
from library.utils.database import getDatabase
from library.utils.modelType import getTypeModel
from library.utils.number import Number
from library.utils.modelType import isSubOf
import copy

class Object:
	def __init__(self,value:dict[str,str]):
		self.objectType = value["objectType"]
		match value["objectType"]:
			case "uuid":
				self.uuid = value["uuid"]
			case "name":
				self.name = value["name"]
			case "type":
				self.type = value["type"]

	def __repr__(self):
		out = None
		match self.objectType:
			case "uuid":
				out = self.uuid
			case "name":
				out = self.name
			case "type":
				out = self.type
		return {"objectType" : self.objectType, self.objectType : out }

	def __str__(self):
		return self.__repr__()

class ObjectName:
	def __init__(self,value:dict[str,str]):
		if value["objectType"] == "name":
			self.name = value["name"]
		return 

	def __repr__(self):
		return  {"objectType" : "name", "name" : self.name }

	def __str__(self):
		return self.__repr__()

class ObjectUUID:
	def __init__(self,value:dict[str,str]):
		if value["objectType"] == "uuid":
			self.uuid = value["uuid"]
		return 

	def __repr__(self):
		return  {"objectType" : "uuid", "uuid" : self.uuid }

	def __str__(self):
		return self.__repr__()

class ObjectType:
	def __init__(self,value:dict[str,str]|str):
		if type(value) == dict:
			self.value = value["type"]
		else:
			self.value = value
		return

	def __repr__(self):
		return  {"objectType" : "type", "type" : self.value}

	def __str__(self) -> str:
		return str(self.__repr__())

	def __eq__(self, value: "ObjectType") -> bool:
		return self.value == value.value

	def __ne__(self, value: "ObjectType") -> bool:
		return self.value != value.value
	
	def __contains__(self, parent:"ObjectType") -> bool:
		return isSubOf(self.value,parent.value)

#############################################
#
# Object Data fast access
#
#############################################

def getObject(uuid : str) -> dict:
	return getDatabase()[uuid]

def MetaData(object:dict):
	return object["MetaData"]

def Qualifier(object:dict):
	return object["Qualifier"]

def isContainer(object : dict) -> bool:
	return MetaData(object)["IsContainer"]

def isCountUnit(object : dict) -> bool:
	return MetaData(object)["IsCountUnit"]

def Count(object : dict) -> tuple[int|float,str,str]:
	return MetaData(object)["Count"]

def getChild(object : dict) -> list[str] :
	return MetaData(object)["StoredUUID"]

def getParent(object : dict) -> str :
	return MetaData(object)["ContainerUUID"]

def getUUID(object : dict) -> str :
	return MetaData(object)["ObjectUUID"]

def getType(object : dict) -> str :
	return MetaData(object)["Type"]

#############################################
#
# Object Data test
#
#############################################

def isEmpty(object : dict) -> bool:
	return len(MetaData(object)["StoredUUID"]) == 0

def isStackable(object :dict) -> bool:
	return isEmpty(object)

def objectMatch(filter : dict, objectData:dict, tolerance: float= 0) -> bool:
	map_type_str ={"string" : str,"bool": bool,"number": Number, "type" : ObjectType, "choice" :str,"name" : ObjectName,"uuid" : ObjectUUID, "any" :Object, "list" : list}
	map_metadata_type = {"Count": "number", "StoredUUID" : "list", "IsContainer" : "bool", "IsCountUnit" : "bool", "ObjectUUID" : "uuid", "Type" : "type"}

	differenceCounter = 0
	testedParameter = 0

	if "MetaData" in filter:
		for parameter,test in filter["MetaData"].items():
			testedParameter += 1
			value = map_type_str[map_metadata_type[parameter]](MetaData(objectData)[parameter]) if map_metadata_type[parameter] != "list" else MetaData(objectData)[parameter]
			if not(test(value)):
				differenceCounter += 1
			

	if "Qualifier" in filter:
		model = getTypeModel(getType(objectData))
		for parameter,test in filter["Qualifier"].items():
			testedParameter += 1
			if parameter not in objectData["Qualifier"]:
				differenceCounter +=1
			else:
				valueType = 'string'
				if model["args"][parameter]["type"] == "object":
					valueType = model["args"][parameter]["objectType"]
				else:
					valueType = model["args"][parameter]["type"]

				value = map_type_str[valueType](Qualifier(objectData)[parameter])
				if not(test(value)) :
					differenceCounter +=1

	return (differenceCounter == 0) or (differenceCounter/testedParameter <= (tolerance/100))

def getNewObject() -> dict:
	return {
		"MetaData" : {
			"ContainerUUID" : "0",
			"ObjectUUID" : genUUID(getDatabase()),
			"StoredUUID" : [],
			"Count" : (0,"unit",""),
			"IsContainer" : False,
			"IsCountUnit" : True,
			"Type" : "Base"
		},
		"Qualifier": {}
	}

def copyObject(object :dict,modification:dict) -> dict:
	newObject = copy.deepcopy(object)
	newObject["MetaData"]["ObjectUUID"] = genUUID(getDatabase())
	for namespace,data in modification.items():
		for key, keyData in data.items():
			newObject[namespace][key] = keyData
	return newObject


def getPrettyName(targetObject : dict) -> str:
	text = f"{getType(targetObject)}< {getUUID(targetObject)} >"
	return (f"{text}{(' : '+ Qualifier(targetObject)['name']) if 'name' in Qualifier(targetObject) and Qualifier(targetObject)['name'] != '' else ''}")

def prettyPrintName(targetObject : dict):
	print(getPrettyName(targetObject))

def getPrettyChild(targetObjectUUID: dict) -> str:
	text = ""
	if len(getChild(targetObjectUUID)) > 0:
		text = "Child	: \n"
		for i,child_uuid in enumerate(getChild(targetObjectUUID)):
			text += f"[{i}] : {getPrettyName(getObject(child_uuid))}\n"
	return text

def prettyPrintChild(targetObject : dict):
	print(getPrettyChild(targetObject))

def prettyPrint(toPrint : dict):

	prettyPrintName(toPrint)
	print("MetaData	: ")

	print(f"\t- IsContainer : {isContainer(toPrint)}")
	print(f"\t- IsCountUnit : {isCountUnit(toPrint)}")
	print(f"\t- Count : {Count(toPrint)[0]} {Count(toPrint)[2]}")

	prettyPrintChild(toPrint)

	print("Qualifier	: ")
	for name, value in Qualifier(toPrint).items():
		if type(value) == str:
			print(f"\t- {name} : \"{value}\"")
		elif (type(value) == list or type(value) == tuple )and len(value) == 3 and (type(value[0]) == int or type(value[0]) == float):
			print(f"\t- {name} : {value[0]} {value[2]}")
		else:
			print(f"\t- {name} : {value}")
