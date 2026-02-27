from library.model.type import FilledModel
from library.object.type import Object, Storage, Storeable


def make_object(model:FilledModel) -> Object:
	__new = None

	match(model.model.type_name):
		case "storage":
			__new = Storeable()

		case "basic":
			__new = Object()

		case _:
			__new = Object()

	__new.count = model.count
	__new.properties = model.properties
	return __new

def make_copy(object:Object) -> FilledModel:
	__new = FilledModel()
	__new.model = object.model
	__new.properties = object.properties
	__new.count = object.count
	return __new

def make_storage(storeable_object:Storeable) -> Storage:
	new_storage = Storage()
	new_storage.type = storeable_object.type
	new_storage.capacity = storeable_object.capacity
	new_storage.properties = storeable_object.properties
	new_storage.count = 1
	return new_storage
