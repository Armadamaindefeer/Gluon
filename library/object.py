import math

uuid = str
unitSystem = str

def genUuid(existing:set[uuid]) -> uuid:
	new_uuid = 0
	while uuid(new_uuid) in existing:
		new_uuid += 1
	return uuid(new_uuid)

class Object:
	def __init__(self) -> None:
		self.uuid:uuid
		self.type:str
		self.parent:uuid
		self.metadata:dict
		self.count:float

	def decrease(self,count:float) -> float:
		if count > 0:
			self.count -= math.trunc(count)
		return self.count

	def increase(self,count:float) -> float:
		self.count += math.trunc(count)
		return self.count 

	def move(self,toUuid) -> bool:
		self.parent = toUuid
		return True

	def getSub(self) -> set[uuid]:
		return set()

class UnCountable(Object):
	def __init__(self) -> None:
		super().__init__()
		self.unit:unitSystem

	def decrease(self,count:float) -> float:
		...

	def increase(self,count:float) -> float:
		...

class Storeable(Object):
	def __init__(self) -> None:
		super().__init__()
		self.capacity:int

	def isEmpty(self) -> bool:
		return True

class Storage(Object):
	def __init__(self) -> None:
		super().__init__()
		self.capacity:int
		self.childs:set[uuid]
		self.count = 1

	def decrease(self) -> float:
		return 1

	def increase(self) -> float:
		return 1

	def isEmpty(self) -> bool:
		return len(self.childs) == 0

	def storeObject(self,object:Object) -> bool:
		#On part du principe que l'objet est dans l'espace global
		if object.uuid in self.childs:
			return False
		self.childs.add(object.uuid)
		object.parent = self.uuid
		return True

	def storeObjectUUID(self,uuid:uuid) -> bool:
		if uuid in self.childs:
			return False
		self.childs.add(uuid)
		return True
	
	def removeChild(self,object:Object) -> bool:
		if object.uuid not in self.childs:
			return False
		
		self.childs.remove(object.uuid)
		object.parent = ""
		return True


	def removeChildUUID(self,uuid:uuid) -> bool:
		if uuid not in self.childs:
			return False
		
		self.childs.remove(uuid)
		return True

	def getSub(self) -> set[uuid]:
		return self.childs

	@staticmethod
	def fromStoreable(storeable_object:Storeable) -> "Storage":
		new_storage = Storage()
		new_storage.type = storeable_object.type
		new_storage.capacity = storeable_object.capacity
		new_storage.metadata = storeable_object.metadata
		new_storage.count = 1
		return new_storage

class Universe:
	def __init__(self) -> None:
		self.objects:dict[uuid,Object]

	def create(self,object:Object) -> uuid:
		object.uuid = genUuid(set(self.objects.keys()))
		self.objects[object.uuid] = object
		self.parent = "OMEGA"
		return object.uuid

	def destroy(self,uuidToRemove:list[uuid]) -> int:
		uuidToExplore = uuidToRemove.copy()
		for uuid in uuidToRemove:
			parent_uuid = self.objects[uuid].parent
			parent_object = self.objects[parent_uuid]
			if isinstance(parent_object,Storage):
				parent_object.removeChildUUID(uuid)

		while len(uuidToExplore) != 0:
			temp = list()
			for uuid in uuidToExplore:
				temp += self.objects[uuid].getSub()
			uuidToExplore = temp
			uuidToRemove += temp

		total = len(uuidToRemove)

		for uuid in uuidToRemove:
			self.objects.pop(uuid)

		return total

	def storeObject(self,objectUUID:uuid,storageUUID:uuid) -> bool:
		#On part du principe que l'objet est dans l'espace global
		storage = self.objects[storageUUID]
		object = self.objects[objectUUID]
		if isinstance(storage,Storeable) and storage.count > 1:
			storage.decrease(1)
			storage = Storage.fromStoreable(storage)
			self.create(storage)
			self.storeObject(objectUUID,storage.parent)
		if isinstance(storage,Storage):
			return storage.storeObject(object)
		return False

	def unstoreObject(self,objectUUID:uuid,storageUUID:uuid) -> bool:
		storage = self.objects[storageUUID]
		object = self.objects[objectUUID]
		if isinstance(storage,Storage):
			return storage.removeChild(object)
		return False

	def moveObject(self,objectUUID:uuid,fromUUID:uuid,toUUID:uuid) -> bool:
		res = self.unstoreObject(objectUUID,fromUUID)
		if res:
			return self.storeObject(objectUUID,toUUID)
		return False
