import math
from library.model.type import Model
from library.common import Uuid
from enum import IntFlag, auto

unitSystem = str

class ERROR(IntFlag):
	HAS_PARENT = auto()
	ALREADY_STORED = auto()
	NOT_STORED = auto()

class Object:
	def __init__(self) -> None:
		self.uuid:Uuid
		self.type:str
		self.parent:Uuid
		self.properties:dict
		self.count:float
		self.model:Model

	def decrease(self,count:float) -> float:
		if count > 0:
			self.count -= math.trunc(count)
		return self.count

	def increase(self,count:float) -> float:
		if count > 0:
			self.count += math.trunc(count)
		return self.count 

	def move(self,toUuid:Uuid):
		self.parent = toUuid

	def getSub(self) -> set[Uuid]:
		return set()

class Storeable(Object):
	def __init__(self) -> None:
		super().__init__()
		self.capacity:int

	def isEmpty(self) -> bool:
		return True

class Storage(Storeable):
	def __init__(self) -> None:
		super().__init__()
		self.childs:set[Uuid]
		self.count = 1

	def decrease(self) -> float:
		return 1

	def increase(self) -> float:
		return 1

	def isEmpty(self) -> bool:
		return len(self.childs) == 0

	def storeObject(self,object:Object) -> int:
		if object.parent != "":
			return ERROR.HAS_PARENT
		if object.uuid in self.childs:
			return ERROR.ALREADY_STORED
		self.childs.add(object.uuid)
		object.parent = self.uuid
		return 0

	def storeObjectUUID(self,uuid:Uuid) -> int:
		if uuid in self.childs:
			return ERROR.ALREADY_STORED
		self.childs.add(uuid)
		return 0
	
	def removeChild(self,object:Object) -> int:
		if object.uuid not in self.childs:
			return ERROR.NOT_STORED
		
		self.childs.remove(object.uuid)
		object.parent = ""
		return 0

	def removeChildUUID(self,uuid:Uuid) -> int:
		if uuid not in self.childs:
			return ERROR.NOT_STORED
		
		self.childs.remove(uuid)
		return 0

	def getSub(self) -> set[Uuid]:
		return self.childs
