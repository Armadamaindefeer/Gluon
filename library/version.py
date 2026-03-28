from numbers import Number
import operator
from typing import Callable, Any

class Version:
	modules:dict[str,int] = dict()
	
	def __init__(self,module_name:str,version:int,brief:str="") -> None:
		self.name = module_name
		self.version = version
		self.brief = brief
		Version.modules[module_name] = version

	def __op__(self,value,op:Callable[[Any,Any],bool]) -> bool:
		if isinstance(value,self.__class__):
			return op(value.version,self.version)
		if isinstance(value,Number):
			return op(value,self.version)
		return False

	def __eq__(self, value) -> bool:
		return self.__op__(value,operator.eq)

	def __le__(self, value):
		return self.__op__(value,operator.le)
	
	def __lt__(self, value):
		return self.__op__(value,operator.lt)

	def __gt__(self, value):
		return self.__op__(value,operator.gt)

	def __ge__(self, value):
		return self.__op__(value,operator.ge)

	def __ne__(self, value: object) -> bool:
		return self.__op__(value,operator.ne)
