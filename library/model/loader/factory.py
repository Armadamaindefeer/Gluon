import copy

from library.model.type import Model
from library.model.loader.type import *


def makeModelDict(models:list[tuple[dict,str,str]]) -> dict[str,dict]:
	out = {}
	for model,dirpath,name in models:
		key = dirpath
		if dirpath != "":
			key += "/"
		key += name
		out[key] = model
		out[key][KEY_DIRPATH] = dirpath
		out[key][KEY_FILENAME] = name
	return out

def resolveAlias(model_dict:dict) -> dict:
	out = {}
	for model_name,model_data in model_dict.items():
		out[model_name] = model_data
		if KEY_ALIAS not in model_data:
			continue

		for alias in model_data[KEY_ALIAS]:
			alias_name = model_data[KEY_DIRPATH]
			if model_data[KEY_DIRPATH] != "":
				alias_name += "/"
			alias_name += alias
			if alias_name in model_dict:
				continue
			if alias_name in out:
				continue
			out[alias_name] = model_data
	return out

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

def resolveParent(model:str,model_database:dict[str,dict],already_parsed:set[str]=set()) -> dict:
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

def getCategory(model_dict:dict) -> set[str]:
	category_list = set()
	for model_name,model_data in model_dict.items():
		if not KEY_IS_CATEGORY in model_data:
			continue		
		if model_data[KEY_IS_CATEGORY] == True:
			category_list.add(model_name)
	return category_list

def resolveCategory(category_list:set, model_dict:dict):
	for model_name in model_dict:
		for category_name in category_list:
			if category_name == model_name:
				continue
			if model_name.startswith(category_name):
				update(model_dict[model_name],model_dict[category_name])

def resolveModel(model_dict):
	model_dict = resolveAlias(model_dict)
	model_dict = {
	model_name:resolveParent(model_name,model_dict,already_parsed=set())
	for model_name in model_dict
	}
	category_list = getCategory(model_dict)
	resolveCategory(category_list,model_dict)
	return model_dict

def makeModel(model_name,model_dict:dict) -> Model:
	__new_model = Model()
	if KEY_ALIAS in model_dict:
		__new_model.alias = model_dict[KEY_ALIAS]
	if KEY_IS_CATEGORY in model_dict:
		__new_model.isCategory = model_dict[KEY_IS_CATEGORY]
	if KEY_PARENT in model_dict:
		__new_model.parent = model_dict[KEY_PARENT]
	if KEY_PROPERTY in model_dict:
		__new_model.properties = model_dict[KEY_PROPERTY]
	if KEY_TYPE in model_dict:
		__new_model.type_name = model_dict[KEY_TYPE]

	filepath = model_dict[KEY_DIRPATH]
	if model_dict[KEY_DIRPATH] != "":
		filepath += "/"
	filepath += model_dict[KEY_FILENAME] + FILE_EXT_MODEL
	__new_model.filepath = filepath
	__new_model.name = model_name

	return __new_model

def makeModels(model_dict):
	return{
		model_name:makeModel(model_name,model_data)
		for model_name,model_data in model_dict.items()
 	}
