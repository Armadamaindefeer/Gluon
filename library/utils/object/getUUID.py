# Gluon , a terminal-based inventory manager
# Copyright (C) 2022-2025 Simon Alligand | Arma_mainfeer
# contact : simon.alligand@gmail.com

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
