import math
from library.model.type import Model
from library.common import Uuid, ERROR
from copy import copy, deepcopy
from typing import Self

unitSystem = str
UUID_ROOT = "0"

class Generic:
	def __init__(self) -> None:
		self.uuid:Uuid = Uuid()
		self.type:str = "Basic"
		self.parent:Uuid = UUID_ROOT
		self.properties:dict = dict()
		self.count:float = 0
		self.model:Model = Model()


	def decrease(self,amount:float) -> int:
		if self.count < amount:
			return ERROR.OVERCONSUMPTION
		if amount > 0:
			self.count -= math.trunc(amount)
			return 0
		return ERROR.UNEXPECTED

	def increase(self,amount:float) -> int:
		if amount > 0:
			self.count += math.trunc(amount)
			return 0
		return ERROR.UNEXPECTED

	def move_to(self,toUuid:Uuid):
		self.parent = toUuid
	
	def copy(self) -> Self:
		__new = self.__class__()
		__new.uuid = UUID_ROOT
		__new.type = copy(self.type)
		__new.count = copy(self.count)
		__new.parent = copy(self.parent)
		__new.properties = deepcopy(self.properties)
		__new.model = copy(self.model)
		return __new

class Storage(Generic):
	def __init__(self) -> None:
		super().__init__()
		self.type = "Storage"
		self.childs:list[Uuid] = []

	def isEmpty(self) -> bool:
		return len(self.childs) == 0

	def decrease(self, amount:float) -> int:
		if self.isEmpty():
			return super().decrease(amount)
		else:
			return ERROR.NOT_EMPTY

	def increase(self, amount:float) -> int:
		if self.isEmpty():
			return super().increase(amount)
		else:
			return ERROR.NOT_EMPTY

	def store(self,object:Generic) -> int:
		if object.parent != UUID_ROOT:
			return ERROR.HAS_PARENT
		if (res := self.storeUUID(object.uuid)) !=0:
			return res
		object.move_to(self.uuid)
		return 0

	def storeUUID(self,uuid:Uuid) -> int:
		if uuid in self.childs:
			return ERROR.ALREADY_STORED
		if self.count > 1:
			return ERROR.STACKED_STORAGE
		self.childs.append(uuid)
		return 0
	
	def unstore(self,object:Generic) -> int:
		if (res := self.unstoreUuid(object.uuid)) != 0:
			return res
		object.move_to(UUID_ROOT)
		return 0

	def unstoreUuid(self,uuid:Uuid) -> int:
		if uuid not in self.childs:
			return ERROR.NOT_STORED
		self.childs.remove(uuid)
		return 0

	def copy(self) -> Self:
		__new = super().copy()
		__new.childs = []
		return __new
