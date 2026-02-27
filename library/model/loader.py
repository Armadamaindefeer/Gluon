import json
import os
import copy
from library.dataField import validate_schema

KEY_PROPERTY = "properties"
KEY_PARENT = "parent"
KEY_TYPE = "type"
KEY_ALIAS = "alias"
KEY_VERSI0N = "version"
KEY_IS_CATEGORY = "isCategory"
CURRENT_VERSION = 0
FILE_EXT_MODEL = ".json"

def update(modelA:dict,modelB:dict):
	if KEY_PROPERTY not in modelB:
		pass
	elif KEY_PROPERTY not in modelA:
		modelA[KEY_PROPERTY] = modelB[KEY_PROPERTY].copy()
	else:
		modelA[KEY_PROPERTY].update(modelB[KEY_PROPERTY])

	if KEY_PARENT not in modelB:
		pass
	elif KEY_PARENT not in modelA:
		modelA[KEY_PARENT] = modelB[KEY_PARENT].copy()
	else:
		modelA[KEY_PARENT] = modelA[KEY_PARENT] + modelB[KEY_PARENT]

	if KEY_TYPE in modelA:
		pass
	elif KEY_TYPE not in modelB:
		pass
	else:
		modelA[KEY_TYPE] = copy.copy(modelB[KEY_TYPE])

def resolveParent(model:str,model_database:dict[str,dict],already_parsed:set[str]=set()):
	already_parsed.add(model)
	model_object = model_database[model]

	if KEY_PARENT not in model_object:
		return model_object

	if type(model_object[KEY_PARENT]) != list:
		return model_object
	
	for parent in model_object[KEY_PARENT]:
		if type(parent) != str:
			continue
		if parent not in model_database:
			continue
		if parent in already_parsed:
			continue

		model_parent = model_database[parent]
		if model_parent == model:
			continue

		update(model_object,resolveParent(parent,model_database,already_parsed))

	return model_object

def loadModels(path:str) -> dict:
	
	model_json:dict[str,dict] = dict()

	for dirpath, _, files in os.walk(path):
		dirpath = dirpath.removeprefix(path).replace("\\","/") + "/"
		for file in files:
			base, ext = os.path.splitext(file)
			with open(path + "\\"+ dirpath + file) as f:
				content = json.load(f)

				if KEY_VERSI0N not in content:
					continue
				if content[KEY_VERSI0N] != CURRENT_VERSION:
					continue

				model_json[dirpath + base] = content
				if KEY_ALIAS not in content:
					continue
				if type(content[KEY_ALIAS]) != list:
					continue
				
				for alias in content[KEY_ALIAS]:
					if type(alias) != str:
						continue
					if dirpath + alias in model_json:
						continue
					model_json[dirpath + alias] = content
	
	category_model = set()

	for model_name,model_data in model_json.items():
		model_json[model_name] = resolveParent(model_name,model_json,already_parsed=set())

		if KEY_IS_CATEGORY not in model_data:
			continue
		if type(model_data[KEY_IS_CATEGORY]) != bool:
			continue
		if model_data[KEY_IS_CATEGORY] == True:
			category_model.add(model_name)

	for model_name in model_json:

		for category_name in category_model:
			if category_name == model_name:
				continue
			if model_name.startswith(category_name):
				update(model_json[model_name],model_json[category_name])

	for model_name,model_data in model_json.items():
		print(model_name)
		if not KEY_PROPERTY in model_data:
			continue
		if type(model_data[KEY_PROPERTY]) != dict:
			continue
		for name,metadata in model_data[KEY_PROPERTY].items():
			print(name,metadata,validate_schema(metadata))
		
	return model_json

#print(findModels("C:\\Users\\armad\\Documents\\Projet\\Gluon\\env\\model\\example"))
