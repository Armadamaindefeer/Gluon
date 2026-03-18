from library.model.type import FilledModel, Model, Faulty
from library.object.type import Generic, Storage, Uuid
from copy import copy, deepcopy

def make_object(model:FilledModel) -> Generic:
	__new = None

	match(model.model.type_name):
		case "Storage":
			__new = Storage()

		case "Basic":
			__new = Generic()

		case _:
			__new = Generic()

	__new.count = model.count
	__new.properties = model.properties
	__new.model = model.model
	return __new

def make_filledModel(object:Generic):
	__new = FilledModel()
	__new.count = copy(object.count)
	__new.model = object.model
	__new.properties = copy(object.properties)
	return __new

def make_dict_generic(object:Generic) -> tuple[Uuid,dict]:
	out = {}
	out["properties"] = deepcopy(object.properties)
	out["count"] = copy(object.count)
	if isinstance(object.model,Faulty):
		out["model"] = copy(object.model.target_model)
	else:
		out["model"] = copy(object.model.name)
	out["parent"] = copy(object.parent)
	out["type"] = copy(object.type)
	return object.uuid,out

def make_dict_storage(object:Storage) -> tuple[Uuid,dict]:
	uuid,out = make_dict_generic(object)
	out["child"] = copy(object.childs)
	return uuid,out

def make_dict(object:Generic) -> tuple[Uuid,dict]:
	if isinstance(object,Storage):
		return make_dict_storage(object)
	elif isinstance(object,Generic):
		return make_dict_generic(object)
	else:
		return make_dict_generic(object)
