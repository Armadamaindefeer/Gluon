from re import M
from library.utils.common import info, jsonWrongType, warn, error, Source
import library.cmdUtils.cmdUtils as cutils
from library.utils.number import unit_system

import os
import typing
import json

DEFAULT_ALLOW_NONE_BY_TYPE = {
	"string" : True,
	"number" : False,
	"boolean" : False,
	"choice" : False,
	"object": False,
	"comment" : True
}

typeModels = dict()

SOURCE = "MODEL_TYPE_SOLVER"

def solveParent(modelsDict : dict,modelName,alreadyParse=[]) -> dict | str:
	current = modelsDict[modelName]
	if "parent" in current and len(current["parent"]) > 0:
		for parent in current["parent"]:
			if parent in alreadyParse:
				return f"Inheritance loop found while solving model"
			elif parent in modelsDict:
				parent = solveParent(modelsDict,parent,alreadyParse+[modelName])
				if type(parent) == str: # if it is STR, it is an error text
					return parent
				elif type(parent) == dict:
					for key,value in parent.items():
						current["args"][key] = value
				else:
					return "Unexpected error"
			else:
				return  f"Unable to find parent {current['parent']} for model : {modelName}"
	return current["args"]

@Source(SOURCE)
def loadTypeModels(path : str= "./model/"):
	out = dict()
	info("Searching models...")
	stat_foundModel = 0
	stat_foundModelFail = 0
	stat_validModel = 0
	stat_aliasModel = 0


	for dirpath, _, files in os.walk(path):
		for filename in files:
			base, ext = os.path.splitext(filename)
			if ext != ".json":
				continue
			else:
				modelName = os.path.join(dirpath.removeprefix(path),base)
				filepath = os.path.join(dirpath, filename)
				temp = None
				potentialError = 1
				stat_foundModel += 1
				try :
					temp = json.load(open(filepath))
				except json.decoder.JSONDecodeError as errorMsg:
					cutils.error(f"in ({filepath}) at [{errorMsg.lineno},{errorMsg.colno}] : {errorMsg.msg}","JSON_DECODER")
					cutils.warn(f"Rejected : {modelName} ({filepath})")
					stat_foundModelFail += 1
					continue
				else :
					info(f"FOUND : {modelName} ({filepath})")
					for key in temp:
						if key not in ["args","alias","version","parent"]:
							warn(f"in ({filepath}) found unknown parameter ({key})")
					if not "args" in temp:
						#error(f"in ({filepath}) : expected \'args\' component")
						potentialError -= 1
						temp["args"] = dict()
					elif type(temp["args"]) != dict:
						jsonWrongType(dict,type(temp['args']),f"{filepath}::args")
					else :
						potentialError -= 1
						for args in temp["args"]:
							potentialError += 1
							if type(temp["args"][args]) != dict:
								jsonWrongType(dict,type(temp["args"][args]),f"{filepath}::args::{args}")

							elif not "type" in temp["args"][args]:
								error(f"in ({filepath}::args::{args}) : expected \'type\' component")

							elif type(temp["args"][args]["type"]) != str:
								jsonWrongType(str,type(temp['args'][args]['type']),f"{filepath}::args::{args}::type")

							elif temp["args"][args]["type"] not in ["comment","string","number","boolean","choice","object"]:
								error(f"in ({filepath}::args::{args}::type) : expected value to be in : {['comment','string','number','boolean','choice','object']}, got \'{temp['args'][args]['type']}\'")

							################################################################
							#Choice type error

							elif temp["args"][args]["type"] == "choice" and "available" not in temp["args"][args]:
								error(f"in ({filepath}::args::{args}) : key \"available\" not found (required because \'type\' component value is \"choice\"")

							elif temp["args"][args]["type"] == "choice" and type(temp["args"][args]["available"]) != list:
								jsonWrongType(list,type(temp['args'][args]['available']),f"{filepath}::args::{args}::available")

							elif temp["args"][args]["type"] == "choice" and len(temp["args"][args]["available"]) < 1:
								error(f"in ({filepath}::args::{args}::available) : expected one ore more value")

							elif temp["args"][args]["type"] == "choice" and len([ type(a) for a in temp["args"][args]["available"] if type(a) != str]) > 0:
								jsonWrongType(list[str],"list" + str([type(a) for a in temp['args'][args]['available']]),f"{filepath}::args::{args}::available")

							################################################################
							#Object type error

							elif temp["args"][args]["type"] == "object" and "objectType" not in temp["args"][args]:
								error(f"in ({filepath}::args::{args}) : key \"objectType\" not found (required because \'type\' component value is \"object\"")

							elif temp["args"][args]["type"] == "object" and type(temp["args"][args]["objectType"]) != str:
								jsonWrongType(str,type(temp['args'][args]['type']),f"{filepath}::args::{args}::objectType")

							elif temp["args"][args]["type"] == "object" and temp["args"][args]["objectType"] not in ["uuid","name","type","any"]:
								error(f"in ({filepath}::args::{args}::objectType) : expected value to be in : {['exact','filter','any']}, got \'{temp['args'][args]['objectType']}\'")

							################################################################
							#Number type error

							elif temp["args"][args]["type"] == "number" and "unitSystem" in temp["args"][args] and type(temp["args"][args]["unitSystem"]) != str:
								jsonWrongType(str,type(temp['args'][args]['unitSystem']),f"{filepath}::args::{args}::unitSystem")

							elif temp["args"][args]["type"] == "number" and  "unitSuffix" in temp["args"][args] and type(temp["args"][args]["unitSuffix"]) != str:
								jsonWrongType(str,type(temp['args'][args]['unitSuffix']),f"{filepath}::args::{args}::unitSuffix")

							elif temp["args"][args]["type"] == "number" and "unitSystem" not in temp["args"][args] and "unitSuffix" in temp["args"][args]:
								error(f"in ({filepath}::args::{args}) : key \"unitSystem\" not found (required by key \"unitSuffix\"")

							elif temp["args"][args]["type"] == "number" and "unitSystem" in temp["args"][args] and temp["args"][args]["unitSystem"] not in unit_system:
								error(f"in ({filepath}::args::{args}::unitSystem) : unrecognised unit system \'{temp['args'][args]['unitSystem']}\', (available unit system : {list(unit_system.keys())})")

							elif temp["args"][args]["type"] == "number" and "unitSuffix" in temp["args"][args] and temp["args"][args]["unitSuffix"] not in unit_system[temp["args"][args]["unitSystem"]]["unitSuffix"]:
								error(f"in ({filepath}::args::{args}::unitSuffix) : unrecognised unit \'{temp['args'][args]['unitSuffix']}\', (available unit : {unit_system[temp['args'][args]['unitSystem']]['unitSuffix']})")

							################################################################


							elif "allowNone" in temp["args"][args] and type(temp["args"][args]["allowNone"]) != bool:
								jsonWrongType(bool,type(temp['args'][args]['allowNone']),f"{filepath}::args::{args}::allowNone")

							else:
								for key in temp["args"][args]:
									if key not in ["type","objectType","allowNone","objectType","value","available","unitSystem","unitSuffix"]:
										warn(f"in ({filepath}::args) : found unknown parameter ({key})")
								potentialError -= 1

							if potentialError == 0 and "allowNone" not in temp["args"][args]:
								temp["args"][args]["allowNone"] = DEFAULT_ALLOW_NONE_BY_TYPE[temp["args"][args]["type"]]
					if potentialError > 0:
						cutils.warn(f"Rejected : {modelName} ({filepath})")
						stat_foundModelFail += 1
					else:
						out[modelName] = temp
						out[modelName]["filepath"] = filepath
						if "parent" not in temp:
							out[modelName]["parent"] = []


	final = dict()

	for modelName,modelData in out.items():
		result = solveParent(out,modelName)
		if type(result) == str:
			cutils.error(f"In {modelName} : {result}","MODEL_SOLVER")
			cutils.warn(f"Rejected : {modelName} ({modelData['filepath']})")
			stat_foundModelFail += 1
		else:
			final[modelName] = {"args" : result}
			final[modelName]["parent"] = out[modelName]["parent"]
			final[modelName]["filepath"] = out[modelName]["filepath"] 
			if "alias" in out[modelName]:
				final[modelName]["alias"] = out[modelName]["alias"]
			stat_validModel += 1

	for modelName,modelData in list(final.items()):
		if "alias" in modelData:

			if type(modelData["alias"]) != str:
				error(f"in ({modelData['filepath']}::alias) : expected value to be {str} instead it is {type(modelData['alias'])}")
				cutils.warn(f"Rejected : {modelName} ({modelData['filepath']})")
				final.pop(modelName)
				stat_validModel -= 1
				stat_foundModelFail += 1

			elif modelData["alias"].strip() == "":
				continue

			elif not modelData["alias"] in final:
				error(f"in ({modelData['filepath']}::alias) : unable to find model specified ({modelData['alias']})")
				cutils.warn(f"Rejected : {modelName} ({modelData['filepath']})")
				final.pop(modelName)
				stat_validModel -= 1
				stat_foundModelFail += 1

			else:
				if ("parent" in modelData and len(modelData["parent"]) > 0) or ("args" in modelData and len(modelData["args"])>0):
					cutils.warn(f"Usage of \'alias\' parameter in an object erase existing data {modelData['filepath']})")
				final[modelName] = final[modelData["alias"]]
				info(f"{modelName} is now an alias for {modelData['alias']}")
				stat_aliasModel += 1

	final["Universe"] = {'args': {'name': {'type': 'string', 'allowNone': False}}, 'filepath': None, "parent": []}
	final["Base"] = {'args' : {}, 'filepath': None, "parent": []}

	info(f'Found {stat_foundModel} model : ({stat_foundModelFail} FAIL/{stat_validModel} SUCESS)')
	info(f'Alias : {stat_aliasModel}')

	info("Done !")
	global typeModels
	typeModels =  final

def getTypeModels() -> dict:
	return typeModels

def getTypeModelsList() -> list[str]:
	return list(getTypeModels().keys())

def getTypeModel(modelName:str) -> dict:
	return typeModels[modelName]

def isSubOf(modelName, searchParent) -> bool:
	if getTypeModel(modelName)["parent"] == []:
		return False
	else:
		for parent in getTypeModel(modelName)["parent"]:
			if parent == searchParent or isSubOf(parent,searchParent):
				return True
	return False
