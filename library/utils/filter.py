import typing
from library.utils.number import Number
from library.utils.object.object import ObjectType, ObjectName, ObjectUUID, Object

filtersList = dict()

def Filter(name: str,symbol : str, availableComparaisonType : list[type]):
	def __wrapper(func:typing.Callable[[typing.Any],typing.Any]):			
		global filtersList
		filtersList[name] = {"filter"  : func, "validType" : availableComparaisonType, "symbol" : symbol}
		return func
	return __wrapper

@Filter("isEqualTo","==",[str,Number,bool,ObjectType])
def isEqualTo(value):
	return lambda x : x == value

@Filter("isDifferentTo","!=",[str,Number,bool,ObjectType])
def isDifferentTo(value):
	return lambda x : x != value

@Filter("isLessThan","<",[Number])
def isLessThan(value):
	return lambda x : x < value

@Filter("isGreaterThan",">",[Number])
def isGreaterThan(value):
	return lambda x : x > value

@Filter("isLessOrEqualTo","<=",[Number])
def isLessOrEqualTo(value):
	return lambda x : x <= value

@Filter("isGreaterOrEqualThan",">=",[Number])
def isGreaterOrEqualThan(value):
	return lambda x : x >= value

@Filter("isLenEqualTo","==",[list])
def isLenEqualTo(value):
	return lambda x : len(x) == value

@Filter("isLenDifferentTo","!=",[list])
def isLenDifferentTo(value):
	return lambda x : len(x) != value

@Filter("isLenLessThan","<",[list])
def isLenLessThan(value):
	return lambda x : len(x) < value

@Filter("isLenGreaterThan",">",[list])
def isLenGreaterThan(value):
	return lambda x : len(x) > value

@Filter("isLenLessOrEqualTo","<=",[list])
def isLenLessOrEqualTo(value):
	return lambda x : len(x) <= value

@Filter("isLenGreaterOrEqualThan",">=",[list])
def isLenGreaterOrEqualThan(value):
	return lambda x : len(x) >= value

@Filter("isSubOf", "sub of", [ObjectType])
def isSubOf(parent):
	return lambda x: parent in x 

#@Filter("isStoredIn", "stored in", [ObjectUUUID,Object])
def isStoredIn():
	...

def hasDirectChild():
	...

def hasChild():
	...	

def prettyPrintFilters(filters:dict):
	for namespace,targets in filters.items():
		for target in targets:
			print(f"{namespace}:{target}")
