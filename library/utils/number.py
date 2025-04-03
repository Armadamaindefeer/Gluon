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

def metricUnitSystem(baseUnit) -> list[str]:
	baseSuffix = ["m","c","d","","da","h","k"]
	return [ suffix + baseUnit for suffix in baseSuffix]	

def HighBase1000(baseUnit,endSuffix=-1) -> list[str]:
	baseSuffix = ["k","M","G","T","P","E","Z","Y"]
	if endSuffix <= -1:
		endSuffix = len(baseSuffix) -1
	out = [baseUnit]
	for i,suffix in enumerate(baseSuffix):
		out += ["",""]
		out += [suffix+baseUnit]
		if i == endSuffix:
			return out
	return out

def NoGap(input:list) -> list:
	return[value for value in input if value != ""]

unit_system = {
				"percentage"	: {"unitSuffix" : ["%",""], "defaultSuffix":"%","Base" : 100, "IsFractional" : True},
				"masse"			: {"unitSuffix" : [*metricUnitSystem("g"), "", "q", "T"], "defaultSuffix" : "g", "IsFractional" : True, "Base" : 10}, 
				"length"		: {"unitSuffix" : metricUnitSystem("m"), "defaultSuffix" : "m", "IsFractional" : True, "Base" : 10},
				"volume"		: {"unitSuffix" : metricUnitSystem("L"), "defaultSuffix" : "L", "IsFractional" : True, "Base" : 10},
				"octet"			: {"unitSuffix" : NoGap(HighBase1000("o")), "defaultSuffix" : "o","IsFractional" : False, "Base" : 1000},
				"kibioctet"		: {"unitSuffix" : NoGap(HighBase1000("io"))[1::],"defaultSuffix" : "Kio", "IsFractional" : True, "Base": 1024},
				"hour"			: {"unitSuffix" : ["s","min","h"], "defaultSuffix" : "s", "isFractional" : True, "Base": 60},
				"unit"			: {"unitSuffix" : [""], "IsFractional" : False, "defaultSuffix" : ""},
				"ohm"			: {"unitSuffix" : NoGap(HighBase1000("o",endSuffix=2)), "IsFractional" : True, "defaultSuffix" : "Ω", "Base" : 100}
			}

def convert(unitSystemName:str, targetUnit:str, currentUnit:str, number:float|int) -> tuple[float|int,str,str]:
	posCurrentUnit = unit_system[unitSystemName]["unitSuffix"].index(currentUnit)
	posTargetUnit = unit_system[unitSystemName]["unitSuffix"].index(targetUnit)
	newValue = number * (unit_system[unitSystemName]["Base"]**(posCurrentUnit-posTargetUnit))
	return (newValue, unitSystemName, targetUnit)

class Number:
	def __init__(self,number : tuple):
		self.value = number[0]
		self.unitSystem = number[1]
		self.unit = number[2]
		return

	def __lt__(self, value: "Number") -> bool:
		if self.unitSystem != value.unitSystem:
				return False
		elif self.unit != value.unit:
			return self.value < convert(self.unitSystem,value.unit,self.unit,value.value)
		else:
			return self.value < value.value

	def __gt__(self, value: "Number") -> bool:
		if self.unitSystem != value.unitSystem:
				return False
		elif self.unit != value.unit:
			return self.value > convert(self.unitSystem,value.unit,self.unit,value.value)
		else:
			return self.value > value.value

	def __le__(self, value: "Number") -> bool:
		if self.unitSystem != value.unitSystem:
				return False
		elif self.unit != value.unit:
			return self.value <= convert(self.unitSystem,value.unit,self.unit,value.value)
		else:
			return self.value <= value.value

	def __ge__(self, value: "Number") -> bool:
		if self.unitSystem != value.unitSystem:
				return False
		elif self.unit != value.unit:
			return self.value >= convert(self.unitSystem,value.unit,self.unit,value.value)
		else:
			return self.value >= value.value

	def __eq__(self, value: "Number") -> bool:
		if self.unitSystem != value.unitSystem:
				return False
		elif self.unit != value.unit:
			return self.value == convert(self.unitSystem,value.unit,self.unit,value.value)
		else:
			return self.value == value.value

	def __ne__(self, value: "Number") -> bool:
		if self.unitSystem != value.unitSystem:
				return False
		elif self.unit != value.unit:
			return self.value != convert(self.unitSystem,value.unit,self.unit,value.value)
		else:
			return self.value != value.value	
