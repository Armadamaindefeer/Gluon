import json
import os
from library.common import ERROR
from library.model.loader.type import *
from library.datafield.datafield import validate_schema

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
	if jsonData[KEY_VERSI0N] < VERSION.version:
		return ERROR.VERSION_OUTDATED
	if jsonData[KEY_VERSI0N] > VERSION.version:
		return ERROR.UNKNOWN_VERSION
	return 0

def validateProperties(jsonData:dict) -> int:
	if KEY_PROPERTY not in jsonData:
		return 0
	if type(jsonData[KEY_PROPERTY]) != dict:
		return ERROR.MALFORMED_PROPERTY
	for key,datafield in jsonData[KEY_PROPERTY].items():
		if type(datafield) != dict:
			return ERROR.MALFORMED_PROPERTY
		if not validate_schema(datafield):
			return ERROR.MALFORMED_PROPERTY
	return 0

def validateParent(jsonData:dict) -> int:
	if KEY_PARENT not in jsonData:
		return 0
	if type(jsonData[KEY_PARENT]) != list:
		return ERROR.MALFORMED_PARENT
	for parent in jsonData[KEY_PARENT]:
		if type(parent) != str:
			return ERROR.MALFORMED_PARENT
	return 0

def validateType(jsonData:dict) -> int:
	if KEY_TYPE not in jsonData:
		return 0
	if type(jsonData[KEY_TYPE]) != str:
		return ERROR.MALFORMED_TYPE
	return 0

def validateAlias(jsonData:dict) -> int:
	if KEY_ALIAS not in jsonData:
		return 0
	if type(jsonData[KEY_ALIAS]) != list:
		return ERROR.MALFORMED_ALIAS
	for alias in jsonData[KEY_ALIAS]:
		if type(alias) != str:
			return ERROR.MALFORMED_ALIAS
	return 0

def validateCategory(jsonData:dict) -> int:
	if KEY_IS_CATEGORY not in jsonData:
		return 0
	if type(jsonData[KEY_IS_CATEGORY]) != bool:
		return ERROR.MALFORMED_ISCATEGORY
	return 0

def validateModel(filepath) -> tuple[int,dict]:
	content = {}
	result = 0
	with open(filepath,"rt",encoding="utf-8") as f:
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
		result,data = validateModel(model_path)
		if result != 0:
			continue
		validated.append((data,dirpath,name))
	return validated
