#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#made by arma_mainfeer aka Simon Poulet-Alligand

import library.cmdUtils.cmdUtils as cutils
from library.cmdUtils.command import globalCommands, Wrapper
from library.utils.common import CtrlInfo, Version, Version_changelog, Version_history, info, isInteger, warn, error, SOURCE, genUUID
from library.utils.config import RAW_CONFIG, getConfigModel, getConfig, loadConfig
from library.utils.database import RAW_DATABASE, getDatabase, getUUIDsList, loadDatabase
from library.utils.number import convert
from library.utils.modelType import getTypeModel, getTypeModels, getTypeModelsList, loadTypeModels
from library.utils.filter import filtersList

import library.utils.userInput as userInput
import library.utils.object.object as object
import library.utils.object.uuid as uuid
import library.utils.object.getUUID as getUUID

import typing
import json
import sys
import copy

#############################################
#
# System
#
#############################################

class ObjectError:
	def __init__(self,autoRepair:bool):
		self.autoRepair = autoRepair
		return

	def __call__(self):
		return

class StructuralError(ObjectError):
	def __init__(self,autoRepair:bool):
		super().__init__(autoRepair)

class MissingMetaDataKey(StructuralError):
	def __init__(self,objectData:dict,objectUUID:str):
		super().__init__(False)
		self.data = objectData
		self.uuid = objectUUID

class DataError(ObjectError):
	def __init__(self,autoRepair:bool):
		super().__init__(autoRepair)

def sanitizeObjectStructure(targetObject:dict) -> list[StructuralError]:
	errorList = []

	if "MetaData" not in targetObject:
		# Need objet re-creation
		return [MissingMetaDataKey(targetObject,genUUID(getDatabase()))]
	else:
		if "StoredUUID" not in object.MetaData(targetObject):
			...
		elif type(object.getChild(targetObject)) != list:
			...
		elif [type(child) for child in object.getChild(targetObject) if type(child) != str] != []:
			...

		if "ContainerUUID" not in object.MetaData(targetObject):
			...
		elif type(object.getParent(targetObject)) != str:
			...

		if "Count" not in object.MetaData(targetObject):
			...
		elif not type(object.Count(targetObject)) == list and not type(object.Count(targetObject)) == tuple:
			...
		elif len(object.Count(targetObject)) != 3:
			...
		elif (not type(object.Count(targetObject)[0]) == float and not type(object.Count(targetObject)[0]) == int) or type(object.Count(targetObject)[1]) != str or type(object.Count(targetObject)[2]) != str:
			...

		if "ObjectUUID" not in object.MetaData(targetObject):
			...
		elif type(object.getUUID(targetObject)) != str:
			...



	if "Qualifier" not in targetObject:
		...
	elif ...:
		...

	return errorList

def sanitizeObjectData(object:dict,database:dict) -> list[DataError]:
	errorList = []


	return errorList

def sanitizeDatabase(database:dict) -> list[ObjectError]:
	errorList = []
	for objectData,objectUUID in database.items():
		objectErrorList = sanitizeObjectStructure(objectData)
		for objectError in objectErrorList:
			if objectError.autoRepair:
				objectError()
			else:
				errorList += [objectError]

	return errorList

#########################################################
#
# Utils
#
#########################################################

def store(toStore :str,containerUUID :str) -> None:

	if uuid.Count(containerUUID)[0] > 1:

		new_uuid = genUUID(getDatabase())
		object_copy = copy.deepcopy(uuid.getObject(containerUUID))
		object_copy["MetaData"]["ObjectUUID"] = new_uuid
		object_copy["MetaData"]["Count"] = (uuid.Count(containerUUID)[0] -1,"unit",None)
		getDatabase()[new_uuid] = object_copy

		uuid.MetaData(uuid.getParent(containerUUID))["StoredUUID"] += [new_uuid]
		uuid.MetaData(uuid.getParent(containerUUID))["Count"] = (1,"unit",None)

	uuid.MetaData(containerUUID)["StoredUUID"] += [toStore]
	uuid.MetaData(toStore)["ContainerUUID"] = containerUUID

def deleteSubObject(UUID : str):
	for child_uuid in uuid.getChild(UUID):
		deleteSubObject(child_uuid)
		getDatabase().pop(child_uuid)
	uuid.MetaData(UUID)["StoredUUID"] = []
	return

#############################################
#
# Commands
#
#############################################

def getAvailableToken(values:list[str],buffer:str):
	token_set = {token[:len(buffer)+1] for token in values if token.startswith(buffer)}
	if len(token_set) > 1 or len(token_set) == 0:
		return buffer
	else:
		returnToken = token_set.pop()
		available_value = [value for value in values if value.startswith(returnToken)]
		if len(available_value) == 1:
			return available_value[0] + " "
		else:
			return getAvailableToken(values,returnToken)

def autoComplete(char_buffer:str,values:list[str],alwaysShow=False) ->str:
	if not alwaysShow:
		display_token = [token for token in values if token.startswith(char_buffer)]
	else:
		display_token = values
	if len(display_token) > 1 and len(display_token) <= 60:
		print("\r",end="")
		for i,value in enumerate(display_token,1):
			terminator = "\n" if i % 6 == 0 else "\t"
			print(value,end=terminator)
		print()
	return getAvailableToken(values,char_buffer)

def autoCompleteFromToken(tokens:list[str],completionList:list[str],alwaysShow=False) -> str:
	if len(tokens) == 3 or (len(tokens) == 2 and tokens[1].count(" ") > 0):
		if len(tokens) == 2:
			result = autoComplete(tokens[-1],completionList,alwaysShow)
		else:
			result = autoComplete(tokens[-2],completionList,alwaysShow)
		if result.strip() == "":
			return "".join(tokens)
		else:
			return "".join([*tokens[:-2]," ",result])
	else:
		return "".join(tokens)

# Ajouter une commande un commande qui permet de convertir un objet en container et vice-versa
def autoCompleteFromList(completionList:list[str],alwaysShow=False) -> typing.Callable:
	def wrapped_autoComplete(tokens:list[str]):
		return autoCompleteFromToken(tokens,completionList,alwaysShow)
	return wrapped_autoComplete

def autoCompleteFromGen(completionGenFunc:typing.Callable,alwaysShow=False) -> typing.Callable:
	def wrapped_autoComplete(tokens:list[str]):
		return autoCompleteFromToken(tokens,completionGenFunc(),alwaysShow)
	return wrapped_autoComplete

def autoCompleteObjectUUID() -> typing.Callable:
	def wrapped_autoComplete(tokens:list[str]):
		result = autoCompleteFromToken(tokens,getUUIDsList(),alwaysShow=False)
		if result.split(" ")[-2].strip() in getUUIDsList():
			uuid.prettyPrintName(result.split(" ")[-2])
		return result
	return wrapped_autoComplete

@Wrapper("exit","exit exitCode","Exit application on use",maxQuantity=1) #TEXT
def _exit(input : cutils.InputParameter) -> None:
	exitCode:str = input[0] if len(input.input) > 0 else ""
	if cutils.Validate("Voulez vous quitter ?",SOURCE,enterIsYes=True): #TEXT
		sys.exit(exitCode)

@Wrapper("reload", "reload","Reload model type from computer storage",maxQuantity=1)
def _reload(input : cutils.InputParameter) -> None:
	modelTypePath:str = input[0] if len(input.input) == 1 else "./model/"
	info("Reloading object types models") #TEXT
	loadTypeModels(modelTypePath)

@Wrapper("new", "new (TYPE)","Create a new object in the database",auto_completion_func=autoCompleteFromGen(getTypeModelsList),maxQuantity=1) #TEXT
def _new(input : cutils.InputParameter) -> None:
	modelTypeName:str = input[0] if len(input) == 1 else userInput.getType()[0]
	if modelTypeName not in getTypeModels():
		error("Invalid type :"+ modelTypeName) #TEXT
		info("Enter : \"list TYPE\" to view available types") #TEXT
		return

	newObject = object.getNewObject()

	object.MetaData(newObject)["Type"] = modelTypeName

	info("Where the object should be stored ?") #TEXT
	container_uuid = ""

	inputMethod = getConfig("defaultInputMethod")
	if inputMethod == "Ask": 
		available_method = [method for method in getConfigModel()["defaultInputMethod"]["available"] if method != "Ask"] 
		inputMethod = available_method[cutils.Choice("Select input method",SOURCE,available_method)] #TEXT

	match inputMethod:
		case "ByName":
			containerName = cutils.Input("Enter container Name (leave empty to select default container)",SOURCE) #TEXT
			available_container = getUUID.fromName_isContainer(containerName)
			if len(available_container) > 1:
				info("Multiple container with the same name are available") #TEXT
				choice:int = cutils.Choice("Please choose one (leave empty to skip)",SOURCE,[uuid.getPrettyName(objectUUID) for objectUUID in available_container],enterIsNone=True) #TEXT 
				if choice == -1:
					info(f"Skipped storing step (defaulted to {uuid.getPrettyName(getConfig('defaultContainerUUID'))})") #TEXT
					container_uuid = getConfig("defaultContainerUUID")
				else:
					container_uuid = available_container[choice]
			elif len(available_container) == 1 :
				container_uuid = available_container[0]
			else:
				warn(f"No available container with specified name (defaulted to {uuid.getPrettyName(getConfig('defaultContainerUUID'))})") #TEXT
				container_uuid = getConfig("defaultContainerUUID")

		case "ByUUID":
			while not container_uuid in getUUID.isContainer():
				container_uuid = userInput.getUUID("Enter container UUID") #TEXT
				if not uuid.isContainer(container_uuid):
					error("Invalid container ,please try again...") #TEXT

		case "ByType":
			containerName = cutils.Input("Enter container type (leave empty to select default container)",SOURCE) #TEXT
			available_container = getUUID.fromName_isContainer(containerName)
			if len(available_container) > 1:
				info("Multiple container with the same name are available") #TEXT
				choice:int = cutils.Choice("Please choose one (leave empty to skip)",SOURCE,[uuid.getPrettyName(objectUUID) for objectUUID in available_container],enterIsNone=True) #TEXT
				if choice == -1:
					info(f"Skipped storing step (defaulted to {uuid.getPrettyName(getConfig('defaultContainerUUID'))})") #TEXT
					container_uuid = getConfig("defaultContainerUUID")
				else:
					container_uuid = available_container[choice]
			elif len(available_container) == 1 :
				container_uuid = available_container[0]
			else:
				warn(f"No available container with specified name (defaulted to {uuid.getPrettyName(getConfig('defaultContainerUUID'))})") #TEXT
				container_uuid = getConfig("defaultContainerUUID")

		case "ByFilter":
			filters,tolerance = userInput.getFilter()
			filter["MetaData" : {"isCont"}]
			available_container = getUUID.fromFilter_isContainer(filters,tolerance)
			if len(available_container) > 1:
				info("Multiple container match with selected filter") #TEXT
				choice:int = cutils.Choice("Please choose one (leave empty to skip)",SOURCE,[uuid.getPrettyName(objectUUID) for objectUUID in available_container],enterIsNone=True) #TEXT
				if choice == -1:
					info(f"Skipped storing step (defaulted to {uuid.getPrettyName(getConfig('defaultContainerUUID'))})") #TEXT
					container_uuid = getConfig("defaultContainerUUID")
				else:
					container_uuid = available_container[choice]
			elif len(available_container) == 1 :
				container_uuid = available_container[0]
			else:
				cutils.warn(f"No available container match with selected filter (defaulted to {uuid.getPrettyName(getConfig('defaultContainerUUID'))})") #TEXT
				container_uuid = getConfig("defaultContainerUUID")
	info(f"Selected container {uuid.getPrettyName(container_uuid)}") #TEXT


	object.MetaData(newObject)["IsContainer"] = cutils.Validate("Is object a container ? (ENTER = YES)",SOURCE,enterIsYes=True) #TEXT


	if object.isContainer(newObject):
		object.MetaData(newObject)["IsCountUnit"] = True
	else:
		object.MetaData(newObject)["IsCountUnit"] = cutils.Validate("Is object's count unit ? (ENTER = YES)",SOURCE,enterIsYes=True) #TEXT


	if object.isCountUnit(newObject):
		object.MetaData(newObject)["Count"] = userInput.getNumber("Enter item quantity", chooseUnitSystem=False,selectedUnitSystem="unit") #TEXT
	else:
		object.MetaData(newObject)["Count"] = userInput.getNumber("Enter item quantity",chooseUnitSystem=True) #TEXT


	for parameterName,parameterData in getTypeModel(modelTypeName)["args"].items():
		if parameterData["type"] == "comment":
			continue
		object.Qualifier(newObject)[parameterName] = userInput.getValue(parameterData,parameterName)


	getDatabase()[object.getUUID(newObject)] = newObject
	store(object.getUUID(newObject),container_uuid)

@Wrapper("remove", "remove (UUID)","Delete an object from the database",auto_completion_func=autoCompleteObjectUUID(),maxQuantity=1) #TEXT
def _remove(input : cutils.InputParameter) -> None:
	targetUUID:str = input[0] if len(input) > 0 else userInput.getObject()
	
	if targetUUID == "0":
		return error("Cannot remove Universe container") #TEXT
	elif targetUUID == getConfig("defaultContainerUUID"): #TEXT
		return error("Cannot remove default container") #TEXT
	elif targetUUID not in getDatabase():
		return error(f"Unable to find object with UUID {targetUUID}") #TEXT

	targetObject = uuid.getObject(targetUUID)

	if uuid.isContainer(targetUUID) and not uuid.isEmpty(targetUUID):
		warn(f"The object ({uuid.getPrettyName(targetUUID)}) contain other objects") #TEXT
		available_choice = ["Delete stored object", "Move stored object inside parent container", "Cancel"] #TEXT
		choice = cutils.Choice("What should be done ?",SOURCE,available_choice) #TEXT
		match choice:
			case 0:
				deleteSubObject(targetUUID)			
			case 1:
				for child_uuid in uuid.getChild(targetUUID):
					uuid.MetaData(child_uuid)["ContainerUUID"] = uuid.getParent(targetUUID)				
			case 2:
				return info("Cancelling!") #TEXT

	uuid.MetaData(uuid.getParent(targetUUID))["StoredUUID"].remove(targetUUID)
	getDatabase().pop(targetUUID)

	info(f"Successfully removed object : {object.getPrettyName(targetObject)}") #TEXT

@Wrapper("move", "move UUID TO_UUID", "Move an object to specified container",maxQuantity=2) #TEXT
def _move(input : cutils.InputParameter) -> None:
	targetUUID:str = input[0] if len(input) > 0 else userInput.getObject()

	targetContainerUUID:str = input[1] if len(input) > 1 else userInput.getObject()


	if targetUUID == "0":
		error("Universe container cannot be moved") #TEXT
		return
	elif targetUUID not in getDatabase():
		error(f"Unable to find object with UUID : {targetUUID}") #TEXT
		return
	elif targetContainerUUID not in getDatabase():
		error(f"Unable to find object with UUID : {targetContainerUUID}") #TEXT
		return
	elif not uuid.isContainer(targetContainerUUID):
		error(f"Target object isn't a container ({uuid.getPrettyName(targetContainerUUID)})") #TEXT
		return 

	uuid.MetaData(uuid.getParent(targetUUID))["StoredUUID"].remove(targetUUID)
	store(targetUUID,targetContainerUUID)

@Wrapper("get", "get UUID (CHILD_NUMBER) ... ","Display data about selected object",auto_completion_func=autoCompleteObjectUUID(), minQuantity=0) #TEXT
def _get(input:cutils.InputParameter) -> None:
	targetUUID:str = input[0] if len(input) > 0 else userInput.getObject()


	if targetUUID not in getDatabase():
		error(f"No object found with UUID : {targetUUID}") #TEXT
		return

	if len(input) <= 1:
		uuid.prettyPrint(targetUUID)
	elif len(input) > 1:
		for i in range(len(input) -1):
			try:
				int(input[i+1])
			except ValueError:
				error(f"Invalid argument for command \'get\', need integer, got {input[i+1]}") #TEXT
				return
			if int(input[i+1]) < len(uuid.getChild(targetUUID)) and int(input[i+1]) >=0:
				print(f"\nChild [{int(input[i+1])+1} out of {len(uuid.getChild(targetUUID))}] of object : {uuid.getPrettyName(targetUUID)}") #TEXT
				uuid.prettyPrint(uuid.getChild(targetUUID)[int(input[i+1])])

@Wrapper("list","list","Display available container", needQuantity=0)
def _list(input:cutils.InputParameter) -> None:
	container_list = getUUID.isContainer()
	info("TYPE<UUID> : NAME") #TEXT
	for containerUUID in container_list:
		print(uuid.getPrettyName(containerUUID))

@Wrapper("type", "type (RELOAD|LIST|INFO) (TYPE)","Allow to reload and get info about model type",minQuantity=1,maxQuantity=2) #TEXT
def _type(input:cutils.InputParameter) -> None:
	parameter = input[0]
	modelTypeName = input[1] if len(input) > 1 else ""

	if parameter.casefold() not in ["RELOAD".casefold(),"LIST".casefold(),"INFO".casefold()]:
		error(f"Invalid argument for command 'type', expected [\"RELOAD\",\"LIST\",\"INFO\"] got \'{input[0]}\'") #TEXT
	elif parameter.casefold() == "RELOAD".casefold(): #TEXT
		_reload(cutils.InputParameter({},[]))
	elif parameter.casefold() == "LIST".casefold(): #TEXT
		info("Available types : ")
		for typeName in getTypeModels().keys():
			print(typeName)
	elif parameter.casefold() == "INFO".casefold(): #TEXT
		if len(input) < 2:
			error("Expected another argument after \'INFO\'") #TEXT
		elif modelTypeName not in getTypeModels():
			error("Invalid typeName")  #TEXT
		else:
			print(json.dumps(getTypeModel(modelTypeName),indent="\t",ensure_ascii=False))

@Wrapper("find", "find","Search database for object which match filters",needQuantity=0) #TEXT
def _find(input:cutils.InputParameter) -> None:
	found = getUUID.fromFilter(*userInput.getFilter())
	info(f"Found {len(found)} match : ") #TEXT
	for objectUUID in found:
		print(uuid.getPrettyName(objectUUID))

@Wrapper("save", "save", "Save database to computer storage",needQuantity=0) #TEXT
def _save(input:cutils.InputParameter) -> None:
	with open("database.json","wt") as o:
		json.dump(RAW_DATABASE(),o,indent="\t",ensure_ascii=False)

@Wrapper("input", f"input {getConfigModel()['defaultInputMethod']['available']}","Edit default input method for selecting object",auto_completion_func=autoCompleteFromList(getConfigModel()['defaultInputMethod']['available'],alwaysShow=True),needQuantity=1) #TEXT
def _inputMethod(input:cutils.InputParameter) -> None:
	valid_value = getConfigModel()["defaultInputMethod"]["available"]
	inputMethod = input[0]

	if inputMethod not in valid_value:
		error(f"Invalid input for command \'input\' (allowed value : {getConfigModel()['defaultInputMethod']['available']})") #TEXT
	else:
		RAW_CONFIG()["defaultInputMethod"] = inputMethod
		json.dump(RAW_CONFIG(),open("./config.json","wt"),indent="\t",ensure_ascii=False)
	
@Wrapper("config", "config","Allow to easily configure application",needQuantity=0) #TEXT
def _config(input:cutils.InputParameter) -> None:
	available_target = [key for key in RAW_CONFIG().keys() if not ("canUserEdit" in getConfigModel()[key] and getConfigModel()[key]["canUserEdit"] == False)]
	target = available_target[cutils.Choice("Select config target",SOURCE,available_target)] #TEXT 
	RAW_CONFIG()[target] = userInput.getValue(getConfigModel()[target],target)
	json.dump(RAW_CONFIG(),open("./config.json","wt"),indent="\t",ensure_ascii=False)

@Wrapper("split", "split (UUID)","Split selected object into two object with specified quantity",auto_completion_func=autoCompleteObjectUUID(),maxQuantity=1) #TEXT
def _split(input:cutils.InputParameter) -> None:
	#targetObject = input[0] if len(input) > 0 else userInput.getUUID("Enter object to split") #TEXT
	targetObject:str = input[0] if len(input) > 0 else userInput.getObject() #TEXT


	if targetObject == "0":
		error("Cannot split Universe") #TEXT
		return
	elif targetObject not in getDatabase():
		error(f"Invalid objectUUID ({targetObject})") #TEXT
		return
	elif not uuid.isEmpty(targetObject):
		error(f"Cannot split non-empty object") #TEXT
	elif uuid.Count(targetObject)[0] == 1 and uuid.isCountUnit(targetObject):
		error(f"Cannot split object of quantity one and value IsCountUnit = True") #TEXT

	oldCount = uuid.Count(targetObject)
	number = userInput.getNumber("Enter percentage split",selectedUnitSystem="percentage",chooseUnit=False,selectedUnit="%") #TEXT
	info(f"Selected ratio : {number[0]}% /{100 - number[0]}%") #TEXT
	number = convert("percentage","",number[2],number[0]) #TEXT
	if uuid.isCountUnit(targetObject):
		FirstHalfCount = round(oldCount[0] * (1-number[0]))
	else:
		FirstHalfCount = oldCount[0]  * (1-number[0])

	SecondHalfCount = oldCount[0] - FirstHalfCount

	info(f"Effective ratio : {(FirstHalfCount* 100)/ (FirstHalfCount + SecondHalfCount)}% /{(SecondHalfCount* 100)/ (FirstHalfCount + SecondHalfCount)}%") #TEXT

	if FirstHalfCount <= 0 or SecondHalfCount <= 0:
		return error(f"One of the quantity is zero of negative {FirstHalfCount}% /{SecondHalfCount}%") #TEXT

	newObject = uuid.copyObject(targetObject,{"MetaData" : {"Count" : (SecondHalfCount ,oldCount[1], oldCount[2])}})

	getDatabase()[object.getUUID(newObject)] = newObject

	store(object.getUUID(newObject),uuid.getParent(targetObject))

	uuid.getObject(targetObject)["MetaData"]["Count"] = (FirstHalfCount ,oldCount[1], oldCount[2])

#Add inline option
@Wrapper("refill", "refill (UUID)","Add a quantity of an existing object",auto_completion_func=autoCompleteObjectUUID(),maxQuantity=1) #TEXT
def _refill(input:cutils.InputParameter) -> None:
	#targetObject = input[0] if len(input) > 0 else userInput.getUUID("Enter object to refill") #TEXT
	targetObject:str = input[0] if len(input) > 0 else userInput.getObject() #TEXT


	if targetObject == "0":
		return error("Cannot edit Universe Container") #TEXT
	elif targetObject not in getDatabase():
		return error(f"Invalid objectUUID ({targetObject})") #TEXT
	elif uuid.isContainer(targetObject) and not uuid.isEmpty(targetObject):
		return error(f"Cannot edit Count of non-empty container") #TEXT
	
	new_value = uuid.Count(targetObject)[0]

	if uuid.isCountUnit(targetObject):
		new_value = uuid.Count(targetObject)[0] + userInput.getNumber("Enter quantity to refill",chooseUnitSystem=False,chooseUnit=False)[0] #TEXT
	else:
		user_value = userInput.getNumber("Enter quantity to refill",chooseUnitSystem=False,selectedUnitSystem=uuid.Count(targetObject)[1]) #TEXT
		new_value = uuid.Count(targetObject)[0] + convert(uuid.Count(targetObject)[1],uuid.Count(targetObject)[2],user_value[2],user_value[0])[0]

	uuid.MetaData(targetObject)["Count"] = (new_value,uuid.Count(targetObject)[1],uuid.Count(targetObject)[2])

#Add inline option
@Wrapper("consume", "consume (UUID)","Substract quantity from an existing object",auto_completion_func=autoCompleteObjectUUID(),maxQuantity=1) #TEXT
def _consume(input:cutils.InputParameter) -> None:
	#targetObject = input[0] if len(input) > 0 else userInput.getUUID("Enter object to consume") #TEXT
	targetObject:str = input[0] if len(input) > 0 else userInput.getObject() #TEXT

	if targetObject == "0":
		return error("Cannot edit Universe Container") #TEXT
	elif targetObject not in getDatabase():
		return error(f"Invalid objectUUID ({targetObject})") #TEXT
	elif uuid.isContainer(targetObject) and not uuid.isEmpty(targetObject):
		return error(f"Cannot edit Count of non-empty container") #TEXT

	new_value = uuid.Count(targetObject)[0]

	if uuid.isCountUnit(targetObject):
		new_value = uuid.Count(targetObject)[0] - userInput.getNumber("Enter quantity to refill",chooseUnitSystem=False)[0] #TEXT
	else:
		user_value = userInput.getNumber("Enter quantity to refill",chooseUnitSystem=False,selectedUnitSystem=uuid.Count(targetObject)[1]) #TEXT
		new_value = uuid.Count(targetObject)[0] - convert(uuid.Count(targetObject)[1],uuid.Count(targetObject)[2],user_value[2],user_value[0])[0]

	uuid.MetaData(targetObject)["Count"] = (new_value,uuid.Count(targetObject)[1],uuid.Count(targetObject)[2])

@Wrapper("empty","empty (UUID)","Remove all the child of selected object",auto_completion_func=autoCompleteObjectUUID(),maxQuantity=1) #TEXT
def _empty(input:cutils.InputParameter) -> None:
	targetObjectUUID:str = input[0] if len(input) > 0 else userInput.getObject()


	available_choice = ["Delete all child object"] #TEXT
	if targetObjectUUID != "0" : 
		available_choice += ["Move child in parent container", "Move child elsewhere"] #TEXT
	available_choice += ["Cancel"] #TEXT

	CtrlInfo()
	choice:int = cutils.Choice("What should be done with the child object ?",SOURCE,available_choice) #TEXT
	if not cutils.Validate(available_choice[choice],SOURCE):
		return info("Cancelling !") #TEXT
	match available_choice[choice]:

		case "Delete all child object": #TEXT
			deleteSubObject(targetObjectUUID)
		case "Move child in parent container": #TEXT
			for childUUID in uuid.getChild(targetObjectUUID):
				uuid.MetaData(targetObjectUUID)["StoredUUID"].remove(childUUID)
				uuid.MetaData(childUUID)["ContainerUUID"] = uuid.getParent(targetObjectUUID)
				uuid.MetaData(uuid.getParent(targetObjectUUID))["StoredUUID"] += childUUID

		case "Move child elsewhere": #TEXT
			containerUUID = userInput.getUUID("Select container")
			if containerUUID == targetObjectUUID:
				error(f"Cannot move child : already stored in {uuid.getPrettyName(containerUUID)}") #TEXT
			else:
				for childUUID in uuid.getChild(targetObjectUUID):
					uuid.MetaData(targetObjectUUID)["StoredUUID"].remove(childUUID)
					store(childUUID,containerUUID)

		case "Cancel": #TEXT
			return info("Cancelling !") #TEXT

	info("Done !") #TEXT

@Wrapper("edit", "edit (UUID)", "Allow editing of object's value",auto_completion_func=autoCompleteObjectUUID(),maxQuantity=1) #TEXT
def _edit(input:cutils.InputParameter) -> None:
	targetObject:str = input[0] if len(input) > 0 else userInput.getObject()


	if targetObject == "0":
		return error("Cannot edit Universe Container") #TEXT
	elif targetObject not in getDatabase():
		return error(f"Invalid objectUUID ({targetObject})") #TEXT

	info(f"Editing object : {uuid.getPrettyName(targetObject)}") #TEXT

	available_namespace = ["MetaData","Qualifier"]
	choice:int = cutils.Choice("Select namespace",SOURCE,available_namespace) #TEXT
	namespace = available_namespace[choice]

	if namespace == "MetaData":
		# Add type modification -> can create trouble
		available_target = ["IsContainer","IsCountUnit","Count"]
		choice:int = cutils.Choice("Select target",SOURCE,available_target) #TEXT
		parameterName = available_target[choice]

		match parameterName:

			case "IsContainer":

				if uuid.isContainer(targetObject) and not uuid.isEmpty(targetObject):
					return error("Cannot edit \"IsContainer\" while object contain other objects") #TEXT
				elif not uuid.isContainer(targetObject) and not uuid.isCountUnit(targetObject):
					return error("Cannot set \"IsContainer\" to True while \"IsCountUnit\" is set to False") #TEXT
				else:
					uuid.MetaData(targetObject)["IsContainer"] = bool(cutils.Choice("Select value for <IsContainer>",SOURCE,["False","True"])) #TEXT

			case "IsCountUnit":
				if uuid.isCountUnit(targetObject) and uuid.isContainer(targetObject):
					return error("Cannot set \"IsCountUnit\" to False while \"IsContainer\" is set to True") #TEXT
				elif not uuid.isCountUnit(targetObject) and not isInteger(uuid.Count(targetObject)[0]):
					return error(f"Cannot set \"IsCountUnit\" to True while \"Count\" value is a decimal {uuid.Count(targetObject)}")	#TEXT

				elif (uuid.isCountUnit(targetObject) and not uuid.isContainer(targetObject) )or (not uuid.isCountUnit(targetObject) and isInteger(uuid.Count(targetObject)[0])):
					uuid.MetaData(targetObject)["IsCountUnit"] = bool(cutils.Choice("Select value for <IsCountUnit>",SOURCE,["False","True"])) #TEXT

			case "Count":
				if uuid.isContainer(targetObject) and not uuid.isEmpty(targetObject):
					return error("Cannot edit count while object contain other objects") #TEXT
				
				elif (uuid.isContainer(targetObject) and uuid.isEmpty(targetObject) )or uuid.isCountUnit(targetObject):
					uuid.MetaData(targetObject)["Count"] = userInput.getNumber("Enter value for <Count>") #TEXT

				else:
					uuid.MetaData(targetObject)["Count"] = userInput.getNumber("Enter value for <Count>",chooseUnitSystem=True,chooseUnit=True) #TEXT


	elif namespace == "Qualifier":
		modelName = uuid.getType(targetObject)
		modelType = getTypeModel(modelName)
		available_parameter = list(modelType["args"].keys())
		available_parameter_str = [f"\'{parameterName}\' = {parameterValue}" for parameterName,parameterValue in uuid.Qualifier(input[0]).items()]
		choice = cutils.Choice("Enter parameter to edit",SOURCE,available_parameter_str) #TEXT
		parameterName = available_parameter[choice]
		parameterData = modelType["args"][parameterName]

		CtrlInfo()
		try:
			value = userInput.getValue(parameterData,parameterName)
		except KeyboardInterrupt:
			warn("Cancelling...") #TEXT
		else:
			uuid.getObject(targetObject)[namespace][parameterName] = value
			info("Done !") #TEXT

@Wrapper("backup", "backup (LOAD|LIST|SAVE) PATH","Create a backup of the database",minQuantity=1,maxQuantity=2) #TEXT
def _backup(input:cutils.InputParameter) -> None:
	return error("NYI")

	parameter = input[0]
	if parameter.casefold() not in ["load".casefold(),"list".casefold(),"save".casefold]:
		error(f"Unknown parameter \"{parameter}\" for command \"backup\" (valid : [\"load\",\"list\",\"save\"])")
		return
	elif len(input.input) > 1 and parameter.casefold() in ["list".casefold()]:
		error(f'Unexpected parameter {input[1]}for command \"backup\"') 

	if parameter.casefold() == "list".casefold():
		...		
	elif parameter.casefold() == "load".casefold():
		...
	elif parameter.casefold() == "save".casefold():
		if len(input.input) == 1:
			path = "./backup/"

@Wrapper("help","help (TOPIC ENTRY)","Show help", maxQuantity=2) #TEXT
def _help(input:cutils.InputParameter) -> None:
	topicData = {
		"Command": {
			"desc" : "Show all available commands", #TEXT
			"entry" : {command.call_name:(command.desc,command.usage) for command in globalCommands},
		},
		"Filter":{
			"desc" : "Show information about filters", #TEXT
			"entry" : {filterName:(f"symbol : \"{filterData['symbol']}\"","Can test the following type : " + str(filterData["validType"])) for filterName,filterData in filtersList.items()} #TEXT
		}
	}

	if len(input) == 0:
		info("List of available topic, type \'help <topic>\'")
		for topicName,topicData in topicData.items():
			info(f"{topicName} : {topicData['desc']}")

	elif len(input) > 0:
		if input[0] not in list(topicData.keys()):

			return error(f"Unknown topic \"{input[0]}\"")
	
		if len(input) == 1:
			info(f"Available entry for {input[0]}")
			for topicEntryName,topicEntry in topicData[input[0]]["entry"].items():
				info(f"{topicEntryName} : {topicEntry[0]}")

		elif len(input) == 2:
			if input[1] not in topicData[input[0]]["entry"]:
				print(topicData[input[0]])
				return error(f"Unknown entry \"{input[1]}\" for topic \"{input[0]}\"")
			info(f'{input[0]}: {input[1]}')
			info(f"{topicData[input[0]]['entry'][input[1]][0]}")
			info("")
			info(f"{topicData[input[0]]['entry'][input[1]][1]}")

@Wrapper("changelog", "changelog","Get changelog for selected version",needQuantity=0) #TEXT
def _changelog(input:cutils.InputParameter) -> None:
	available_version = Version_history
	choice:int = cutils.Choice("Select version (sorted from earliest to latest)",SOURCE,available_version) #TEXT

	info(f"Changelog for version {available_version[choice]} :") #TEXT
	if len(Version_changelog[available_version[choice]]) > 0:
		for entry in Version_changelog[available_version[choice]]:
			info(f"- {entry}")
	else:
		info("- No Changelog") #TEXT

def main() -> None:	
	cutils.toggleInternalDebug()
	cmd = cutils.CmdHandler(SOURCE)

	info(f"Running Virgil {Version}") #TEXT

	loadTypeModels("./model/")
	loadDatabase("./database.json")
	loadConfig("./config.json")

	latestVersion = getConfig("latestVersion")
	latestVersionIndex = Version_history.index(latestVersion)
	for i,version in enumerate(Version_history[latestVersionIndex+1::]):
			info(f"Changelog for version {version} :")
			if len(Version_changelog[version]) > 0:
				for entry in Version_changelog[version]:
					info(f"- {entry}")
			else:
				info("- No Changelog")

	RAW_CONFIG()["latestVersion"] = Version
	json.dump(RAW_CONFIG(),open("./config.json","wt"),indent="\t",ensure_ascii=False)

	info("Virgil launch has succeed") #TEXT
	print("Gluon  Copyright (C) 2022-2023  Simon Poulet-Alligand | Arma_mainfeer")
	#print("This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.")
	print("This program comes with ABSOLUTELY NO WARRANTY.")
	print("This is free software, and you are welcome to redistribute it")
	#print("under certain conditions; type `show c' for details.")

	info(f"Welcome {getConfig('username')}") #TEXT

	running = True
	while running:
		try :
			cmd.handle_input()
		except KeyboardInterrupt:
			if cutils.Validate("Voulez vous quitter ?",SOURCE,enterIsYes=True): #TEXT
				if getConfig("saveOnExit"):
					_save(cutils.InputParameter({},[]))
				sys.exit()

if __name__ == "__main__":
	main()
