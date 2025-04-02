from library.utils.database import getDatabase
import library.utils.object.object as object
import library.utils.filter as filter

def fromFilter(filter : dict, tolerance: float=0) -> list[str]:
	return [
		uuid
		for uuid,objectData in getDatabase().items()
		if object.objectMatch(filter,objectData,tolerance)
	]

def fromName(name : str) -> list[str]:
	return fromFilter({"Qualifier" : {"name" : filter.isEqualTo(name)}}) + fromFilter({"MetaData" : {"Type" : filter.isEqualTo(object.ObjectType(name))}})

def fromType(type: str) -> list[str]:
	return fromFilter({"MetaData" : {"Type" : filter.isEqualTo(object.ObjectType(type))}})

def isContainer() -> list[str]:
	return fromFilter({"MetaData" : {"IsContainer" : filter.isEqualTo(True)}})

def fromName_isContainer(name : str) -> list[str]:
	return fromFilter({"MetaData" : {"IsContainer" : filter.isEqualTo(True)}, "Qualifier" : {"name" : filter.isEqualTo(name)}})

def fromType_isContainer(type : str) -> list[str]:
	return fromFilter({"MetaData" : {"IsContainer" : filter.isEqualTo(True), "Type" : filter.isEqualTo(object.ObjectType(type))}})

def fromFilter_isContainer(inputFilter : dict,tolerance) -> list[str]:
	inputFilter["MetaData"]["IsContainer"] = filter.isEqualTo(True)
	return fromFilter(inputFilter,tolerance)
