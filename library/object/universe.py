from library.object import type as object_type, factory as object_factory
from library.model import type as model_type
from library.common import genUUID, Uuid, ERROR

class Universe(object_type.Storage):
	def __init__(self) -> None:
		super().__init__()
		self.model = model_type.Universe()
		self.uuid = object_type.UUID_ROOT
		self.objects:dict[Uuid,object_type.Generic] = {self.uuid : self}

	def isEmpty(self) -> bool:
		return False

	def decrease(self, amount: float) -> int:
		return ERROR.MODIFIYING_UNIVERSE

	def increase(self, amount: float) -> int:
		return ERROR.MODIFIYING_UNIVERSE

	def exist(self,uuid:Uuid) -> bool:
		return uuid in self.objects

	def create(self,model:model_type.FilledModel,storage:Uuid=object_type.UUID_ROOT) -> Uuid:
		object = object_factory.make_object(model)
		object.uuid = genUUID(existing=set(self.objects.keys()))
		self.objects[object.uuid] = object 
		self.store(object)
		if storage != object_type.UUID_ROOT:
			self.storeObject(object.uuid,storage)
		return object.uuid

	def destroy(self,objectUUID:Uuid,destroyChildren:bool = False) -> int:
		if objectUUID == object_type.UUID_ROOT:
			return ERROR.MODIFIYING_UNIVERSE

		object_ = self.objects[objectUUID]

		if isinstance(object_,object_type.Storage):
			if destroyChildren:
				for child in object_.childs:
					self.destroy(child,destroyChildren)
			else:
				for child in object_.childs:
					self.objects[child].parent = object_.parent

		parent_ = self.objects[object_.parent]
		if isinstance(parent_,object_type.Storage):
			parent_.childs.remove(objectUUID)

		self.objects.pop(objectUUID)
		return 0

	def storeObject(self,object:Uuid,storage:Uuid) -> int:
		object_ = self.objects[object] # Object may not exist
		storage_ = self.objects[storage] # Object may not exist
		if object == storage:
			return ERROR.SAME_OBJECT

		if isinstance(object_,self.__class__):
			return ERROR.MODIFIYING_UNIVERSE

		if not isinstance(storage_,object_type.Storage):
			return ERROR.NOT_A_STORAGE

		#Storage is considered empty
		if storage_.count > 1:
			storage_filledModel = object_factory.make_filledModel(storage_)
			storage_filledModel.count -= 1
			storage_.count = 1
			self.create(storage_filledModel)

		self.unstore(object_)
		return storage_.store(object_)

	def unstoreObject(self,object:Uuid) -> int:
		object_ = self.objects[object]
		storage_ = self.objects[object_.parent]
		if isinstance(object_,self.__class__):
			return ERROR.MODIFIYING_UNIVERSE

		if not isinstance(storage_,object_type.Storage):
			return ERROR.NOT_A_STORAGE

		return storage_.unstore(object_)

	def moveObject(self,object:Uuid,to:Uuid) -> int:
		object_ = self.objects[object]
		from_ = self.objects[object_.parent]
		to_ = self.objects[to]
		if isinstance(object_,self.__class__):
			return ERROR.MODIFIYING_UNIVERSE

		if not isinstance(from_,object_type.Storage):
			return ERROR.NOT_A_STORAGE
		
		if not isinstance(to_,object_type.Storage):
			return ERROR.NOT_A_STORAGE

		if object not in from_.childs:
			return ERROR.NOT_STORED

		if (res := self.unstoreObject(object)) != 0:
			return res
		
		return self.storeObject(object,to)
