import json
import os
from library.common import ERROR
from library.model.loader.type import *

def findModel(path:str) -> set[tuple[str,str]]:
	maybe = set()
	for dirpath, _, files in os.walk(path):	
		dirpath = dirpath.removeprefix(path).replace("\\","/").removeprefix("/")
		for file in files:
			base, ext = os.path.splitext(file)
			if ext != ".json":
				continue
			maybe.add((dirpath,base))
	return maybe


def validateVersion(jsonData:dict) -> int:
	if not KEY_VERSI0N in jsonData:
		return ERROR.UNKNOWN_VERSION
	if jsonData[KEY_VERSI0N] < CURRENT_VERSION:
		return ERROR.VERSION_OUTDATED
	if jsonData[KEY_VERSI0N] > CURRENT_VERSION:
		return ERROR.UNKNOWN_VERSION
	return 0

def validateProperties(jsonData:dict) -> int:
	return 0

def validateParent(jsonData:dict) -> int:
	return 0

def validateType(jsonData:dict) -> int:
	return 0

def validateAlias(jsonData:dict) -> int:
	return 0

def validateCategory(jsonData:dict) -> int:
	return 0

def validateModel(filepath) -> tuple[int,dict]:
	content = {}
	result = 0
	with open(filepath,"rt") as f:
		try : 
			content = json.load(f)
		except json.JSONDecodeError:
			return ERROR.JSON_DECODER_ERROR, content

		if (result := validateVersion(jsonData=content)) != 0:
			return result,content
		
		result |= validateProperties(content)
		result |= validateCategory(content)
		result |= validateParent(content)
		result |= validateAlias(content)
		result |= validateType(content)
	return result, content

def validateModels(root_path:str,models:set[tuple[str,str]])-> list[tuple[dict,str,str]]:
	validated = []
	for dirpath,name in models:
		model_path = "/".join((root_path,dirpath,name)) + FILE_EXT_MODEL
		result = validateModel(model_path)
		if result[0] != 0:
			continue
		validated.append((result[1],dirpath,name))
	return validated
