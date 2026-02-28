from library.object import type as object_type, factory as object_factory
from library.model import type as model_type
from library.common import genUUID, Uuid, ERROR

class Universe:
	def __init__(self) -> None:
		self.objects:dict[Uuid,object_type.Generic]

	def exist(self,uuid:Uuid) -> bool:
		return uuid in self.objects

	def register(self,object:object_type.Generic) -> Uuid:
		object.uuid = genUUID(existing=set(self.objects.keys()))
		self.objects[object.uuid] = object
		self.parent = "OMEGA"
		return object.uuid

	def create(self,model:model_type.FilledModel) -> Uuid:
		return self.register(object_factory.make_object(model))
	
	def destroy(self,objectUUID:Uuid,destroyChildren:bool = False) -> int:
		object_object = self.objects[objectUUID]

		if isinstance(object_object,object_type.Storage):
			if not destroyChildren:
				for child in object_object.childs:
					self.objects[child].parent = object_object.parent
			elif destroyChildren:
				for child in object_object.childs:
					self.destroy(child,destroyChildren)

		parent_object = self.objects[object_object.parent]
		if isinstance(parent_object,object_type.Storage):
			parent_object.childs.remove(objectUUID)
		self.objects.pop(objectUUID)

		return 0

	def storeObject(self,objectUUID:Uuid,storageUUID:Uuid) -> int:
		object_object = self.objects[objectUUID]
		storage_object = self.objects[storageUUID]

		if not isinstance(storage_object,object_type.Storeable):
			return ERROR.NOT_A_STORAGE

		if isinstance(storage_object,object_type.Storeable):
			if storage_object.count > 1:
				__new_storage_object = object_factory.make_storage(storage_object)
				self.register(__new_storage_object)
				storage_object.decrease(1)
				storage_object = __new_storage_object

		if isinstance(storage_object,object_type.Storage):
			if objectUUID in storage_object.childs:
				return ERROR.ALREADY_STORED
			object_object.move("")
			return storage_object.storeObject(object_object)

		return ERROR.UNEXPECTED

	def unstoreObject(self,objectUUID:Uuid,storageUUID:Uuid) -> int:
		object_object = self.objects[objectUUID]
		storage_object = self.objects[storageUUID]

		if not isinstance(storage_object,object_type.Storage):
			return ERROR.NOT_A_STORAGE
		elif isinstance(storage_object,object_type.Storage):
			return storage_object.removeChild(object_object)

		return ERROR.UNEXPECTED

	def moveObject(self,objectUUID:Uuid,fromUUID:Uuid,toUUID:Uuid) -> int:
		object_object = self.objects[objectUUID]
		from_object = self.objects[fromUUID]
		to_object = self.objects[toUUID]

		if not isinstance(from_object,object_type.Storage):
			return ERROR.NOT_A_STORAGE
		
		if not isinstance(to_object,object_type.Storeable):
			return ERROR.NOT_A_STORAGE

		if objectUUID not in from_object.childs:
			return ERROR.NOT_STORED

		if (res := self.unstoreObject(objectUUID,fromUUID)) != 0:
			return res

		return self.storeObject(objectUUID,toUUID)
