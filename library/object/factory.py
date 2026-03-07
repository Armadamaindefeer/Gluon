from library.model.type import FilledModel
from library.object.type import Generic, Storage, Storeable


def make_object(model:FilledModel) -> Generic:
	__new = None

	match(model.model.type_name):
		case "storage":
			__new = Storeable()

		case "basic":
			__new = Generic()

		case _:
			__new = Generic()

	__new.count = model.count
	__new.properties = model.properties
	__new.model = model.model
	return __new

def make_copy(object:Generic) -> FilledModel:
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
