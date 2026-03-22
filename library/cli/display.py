import library.object.type as object_type


def text_short_generic(object:object_type.Generic):
	text = f"<{object.model.name}> : {object.count} unit(s)"
	if "name" in object.properties:
		text = f"{object.properties['name']} <{object.model.name}> : {object.count} unit(s)"
	return text

def print_short_generic(object:object_type.Generic):
	print(text_short_generic(object))

def text_short_storage(object:object_type.Storage):
	text = f"<{object.model.name}> : {len(object.childs)} different stored object"
	if "name" in object.properties:
		text = f"{object.properties['name']} <{object.model.name}> : {len(object.childs)} different stored object"
	return text

def print_short_storage(object:object_type.Storage):
	print(text_short_storage(object))

def text_short(object:object_type.Generic):
	if isinstance(object,object_type.Storage):
		return text_short_storage(object)
	elif isinstance(object,object_type.Generic):
		return text_short_generic(object)


def print_short(object:object_type.Generic):
	print("\r" + text_short(object))

def print_properties(object:object_type.Generic):
	if len(object.properties) == 0:
		return
	print("Properties:")
	for properties_name,data in object.properties.items():
		print(f"\t {properties_name} : {data}")

def print_generic(object:object_type.Generic):
	print_short_generic(object)
	print_properties(object)

def print_storage(object:object_type.Storage):
	print_short_storage(object)
	print_properties(object)


def printObject(object:object_type.Generic):
	if isinstance(object,object_type.Storage):
		print_storage(object)
	elif isinstance(object,object_type.Generic):
		print_generic(object)
	else:
		print_generic(object)
