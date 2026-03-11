from library.model.type import FilledModel
from library.object.type import Generic, Storage
from copy import copy

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
	__new.model = copy(object.model)
	__new.properties = copy(object.properties)
	return __new
