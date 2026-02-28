from library.model.type import Model
from library.model.loader.validator import findModel, validateModels
from library.model.loader.factory import makeModelDict, resolveModel, makeModels

def constructModels(model_dir_path:str) -> dict[str,Model]:
	model_path = findModel(model_dir_path)
	model_list = validateModels(model_dir_path,model_path)
	model_dict = makeModelDict(model_list)
	model_dict = resolveModel(model_dict)
	return makeModels(model_dict)
