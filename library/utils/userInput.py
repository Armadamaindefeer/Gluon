import library.cmdUtils.cmdUtils as cutils
from library.utils.common import CtrlInfo, info, error, warn,SOURCE 
from library.utils.config import getConfig, getConfigModel
from library.utils.database import getDatabase
from library.utils.number import Number, unit_system, convert
from library.utils.modelType import getTypeModel, getTypeModels
from library.utils.object.object import Object, ObjectName, ObjectType, ObjectUUID

import library.utils.object.uuid as uuid
import library.utils.object.object as object
import library.utils.object.getUUID as guuid


from library.utils.filter import filtersList

def getNumber(text : str, chooseUnitSystem : bool = False, selectedUnitSystem= "unit",chooseUnit=True,selectedUnit: str = "") -> tuple[float |int,str,str]:
	if chooseUnitSystem: 
		available_unit = list(unit_system.keys())
		choice:int = cutils.Choice("Please choose a unit system (Leave empty for default : unit)", SOURCE,available_unit,enterIsNone=True) #TEXT
		if choice == -1:
			selectedUnitSystem = "unit"
		else:
			selectedUnitSystem = available_unit[choice]
	

	if len(unit_system[selectedUnitSystem]["unitSuffix"]) > 1 and chooseUnit:
		choice:int = cutils.Choice("Please choose a unit", SOURCE,[value for value in unit_system[selectedUnitSystem]["unitSuffix"] if value != None]) #TEXT
		selectedUnit = [value for value in unit_system[selectedUnitSystem]["unitSuffix"] if value != None][choice]
	elif selectedUnit not in unit_system[selectedUnitSystem]["unitSuffix"]:
		selectedUnit = unit_system[selectedUnitSystem]["defaultSuffix"]


	value = 0.0
	trying = True
	while trying:
		try :
			if unit_system[selectedUnitSystem]["IsFractional"]:
				value = float(cutils.Input(text,SOURCE)) 
			else:
				value = int(cutils.Input(text,SOURCE))
		except ValueError:
			error(f"Invalid integer,please try again...") #TEXT
		else:
			if value < 0:
				error("Quantity number cannot be negative") #TEXT
			else:
				trying = False

	return value,selectedUnitSystem,selectedUnit

def getType() -> tuple[str,dict]:
	modelName = ""
	while modelName not in getTypeModels():
		modelName:str = cutils.Input("Select model type name",SOURCE) #TEXT 
		if modelName not in getTypeModels():
			error("Invalid model type, please try again...") #TEXT
	return modelName,getTypeModel(modelName)

def getName(text: str) -> str:
	while True:
		name:str = cutils.Input(text,SOURCE) 
		if len(guuid.fromName(name)) == 0:
			error(f"Unable to found object with name {name}, please try again") #TEXT
		else:
			return name

def getUUID(text:str,allowNone=False)-> str:
	while True:
		uuid:str = cutils.Input(f"{text} {'(leave empty to select default container)' if allowNone else ''}",SOURCE) #TEXT
		if uuid == "":
			return getConfig("defaultContainerUUID") 
		elif uuid not in getDatabase():
			error(f"Unable to found object with uuid {uuid}, please try again") #TEXT
		else:
			return uuid

def getFilter() -> tuple[dict,float]:
	CtrlInfo()

	available_namespace = ["MetaData", "Qualifier"]

	map_metadata_type = {"Count": "number", "StoredUUID" : "list", "IsContainer" : "bool", "IsCountUnit" : "bool", "ObjectUUID" : "uuid", "Type" : "type"}
	available_metadata = list(map_metadata_type.keys())
	map_target_type = dict()

	map_type_str ={"string" : str,"bool": bool,"number": Number, "type" : ObjectType, "uuid" : ObjectUUID, "any" :Object, "list" : list}

	filters = dict()
	filtering = True
	while filtering:
		try : 
			choice:int = cutils.Choice("Select filter namespace", SOURCE,available_namespace) #
			namespace = available_namespace[choice]
			if namespace not in filters:
				filters[namespace] = dict()
			available_target = []
			target = ""
			target_type = None
			test = None

			numberParameter:dict

			# implémente les teste sur Objets

			if namespace == "MetaData":
				available_target = available_metadata
				map_target_type = map_metadata_type

			elif namespace == "Qualifier":

				modelType = getType()[1]["args"]
				available_target = list(modelType.keys())
				
				for parameterName,parameterType in modelType.items():
					if parameterType["type"] == "object":
						map_target_type[parameterName] = parameterType['objectType']
					else:
						map_target_type[parameterName] = parameterType["type"]
					if parameterType["type"] == "number":
						numberParameter = parameterType


			choice:int = cutils.Choice("Select filter target", SOURCE,available_target) #TEXT
			target = available_target[choice]
			target_type = map_type_str[map_target_type[target]]

			available_test = [(name,test) for name,test in filtersList.items() if target_type in test["validType"]] 
			available_test_str = [f"Name : {name} ({test['symbol']})" for name,test in available_test] #TEXT

			choice:int = cutils.Choice("Select filter", SOURCE,available_test_str) #TEXT
			test = available_test[choice]

			# Implémente le choix de la valeur du teste
			testValue = ""
			match map_target_type[target]:
				case "string":
					testValue = cutils.Input("Enter comparaison value (string)",SOURCE) #TEXT
				case "number":
					info("Comparaison between different unit system (e.g. \"masse\" and \"volume\") will always be False") #TEXT
					if "unitSystem" in numberParameter:
						testValue = Number(getNumber("Enter comparaison value",chooseUnitSystem=False,selectedUnitSystem=numberParameter["unitSystem"])) #TEXT
					else:
						testValue = Number(getNumber("Enter comparaison value",chooseUnitSystem=True)) #TEXT
				case "bool":
					choice:int = cutils.Choice("Choose comparaison value (leave empty for False)",SOURCE,[False,True],enterIsNone=True) #TEXT
					if choice == -1 or choice ==0:
						testValue = False
					else:
						testValue = True
				case "type":
					testValue = ObjectType({"type" : getType()[0]})
				case "uuid":
					testValue = ObjectUUID({"uuid" : getUUID("Enter comparaison value (UUID)")}) #TEXT
				case "name":
					testValue = ObjectName({"name" : getName("Enter comparaison value (ObjectName)")}) #TEXT
				case "any":
					available_choice = ["type","uuid","name"]
					choice:int = cutils.Choice("Choose input method",SOURCE,available_choice) #TEXT
					if choice == 0:
						testValue = Object({"objectType" : "type","type" : getType()[0]}) 
					elif choice == 1:
						testValue = Object({"objectType" : "uuid","uuid" : getUUID("Enter comparaison value (UUID)")}) #TEXT
					elif choice == 2:
						testValue = Object({"objectType" : "name","name" : getName("Enter comparaison value (ObjectName)")}) #TEXT

				case "list":
					trying = True
					while trying:
						try:
							testValue = int(cutils.Input("Enter comparaison value (integer)",SOURCE)) #TEXT
						except ValueError:
							error("Invalid integer : try again") #TEXT
						else:
							if testValue < 0:
								error("Quantity number cannot be negative") #TEXT
							else:
								trying = False
			print(f"{namespace}:{target} : {test[0]}")
			if cutils.Validate("Is Filter correct ?",SOURCE,enterIsYes=True): #TEXT
				filters[namespace][target] = test[1]["filter"](testValue)


		except KeyboardInterrupt:
			pass
		finally:
			if not cutils.Validate("Create Another filter ?",SOURCE): #TEXT
				filtering = False

	tolerance = 0
	try :
		tolerance = float(cutils.Input("Select tolerance over difference filter/object",SOURCE))  #TEXT
	except ValueError:
		error("Invalid number, defaulting to zero-tolerance") #TEXT

	return filters,tolerance			

def getValue(parameterData:dict,parameterName:str):
	value = None
	match parameterData["type"]:
		case "string":
			while value == None:
				value = cutils.Input(f"Enter value for <{parameterName}> {'(Press ENTER to leave empty)' if parameterData['allowNone'] else ''}",SOURCE) #TEXT
				if value == "" and not parameterData['allowNone']:
					info(f"Value cannot be empty, please try again...") #TEXT
					value = None
		case "number":
			info(f"Choose value for<{parameterName}>") #TEXT
			if "unitSystem" in parameterData and "unitSuffix" not in parameterData:
				value = getNumber(f"Enter number",chooseUnitSystem=False,selectedUnitSystem=parameterData["unitSystem"]) #TEXT
			elif "unitSystem" in parameterData and "unitSuffix" in parameterData:
				number = getNumber(f"Enter number",chooseUnitSystem=False,selectedUnitSystem=parameterData["unitSystem"]) #TEXT
				value = convert(parameterData["unitSystem"],parameterData["unitSuffix"],number[2],number[0])
			else:
				value = getNumber(f"Enter number") #TEXT
		case "bool":
			choice:int = cutils.Choice(f"Choose value for<{parameterName}>",SOURCE,[False,True]) #TEXT
			if choice == -1 or choice ==0:
				value = False
			else:
				value = True
		case "choice":
			choice:int = cutils.Choice(f"Choose a value for <{parameterName}> {'(Press ENTER to leave empty)' if parameterData['allowNone'] else ''}",SOURCE,parameterData['available'],parameterData['allowNone']) #TEXT
			if choice == -1 and parameterData["allowNone"]:
				value = ""
			else:
				value = parameterData['available'][choice]
		case "object":
			match parameterData["objectType"]:
				case "type":
					cutils.info(f"Enter type for parameter <{parameterName}>") #TEXT
					value = {"type" : getType()[0]}

				case "uuid":
					cutils.info(f"Enter object uuid for parameter <{parameterName}>") #TEXT
					value = {"uuid" : getUUID("Enter target object (UUID)")} #TEXT
				case "name":
					cutils.info(f"Enter object name for parameter <{parameterName}>") #TEXT
					value = {"name" : getName("Enter target object (ObjectName)")} #TEXT
				case "any":
					available_choice = ["type","uuid","name"]
					choice:int = cutils.Choice("Choose input method",SOURCE,available_choice) #TEXT 
					if choice == 0:
						cutils.info(f"Enter type for parameter <{parameterName}>") #TEXT
						value = {"objectType" : "type","type" : getType()[0]}

					elif choice == 1:
						cutils.info(f"Enter object uuid for parameter <{parameterName}>") #TEXT					
						value = {"objectType" : "uuid","uuid" : getUUID("Enter target object  (UUID)")} #TEXT

					elif choice == 2:
						cutils.info(f"Enter object name for parameter <{parameterName}>") #TEXT
						value = {"objectType" : "name","name" : getName("Enter target object  (ObjectName)")} #TEXT

	return value

def getObject() -> str:
	inputMethod = getConfig("defaultInputMethod") #TEXT
	if inputMethod == "Ask":
		available_method = [method for method in getConfigModel()["defaultInputMethod"]["available"] if method != "Ask"]
		inputMethod = available_method[cutils.Choice("Select input method",SOURCE,available_method)] #TEXT

	outObjectUUID = "0"

	match inputMethod:
		case "ByName":
			objectName = getName("Enter object name") #TEXT
			available_object = guuid.fromName(objectName)
			if len(available_object) > 1:
				info("Multiple object with the same name were found") #TEXT
				choice:int = cutils.Choice("Please choose one (Press ENTER to select Universe)",SOURCE,[uuid.getPrettyName(objectUUID) for objectUUID in available_object],enterIsNone=True) #TEXT
				if choice == -1:
					outObjectUUID = "0"
				else:
					outObjectUUID = available_object[choice]
			elif len(available_object) == 1 :
				outObjectUUID = available_object[0]
			#Normalement, else n'arrive jamais
			else:
				warn(f"No available container with specified name (defaulted to {uuid.getPrettyName(getConfig('0'))})") #TEXT
				outObjectUUID = getConfig("defaultContainerUUID")

		case "ByUUID":
			outObjectUUID = ""
			while not outObjectUUID in getDatabase():
				outObjectUUID = getUUID("Enter object UUID") #TEXT

		case "ByType":
			objectType = getType()[0]
			available_object = guuid.fromType(objectType)
			if len(available_object) > 1:
				info("Multiple object with the type were found") #TEXT
				choice:int = cutils.Choice("Please choose one (Press ENTER to select Universe)",SOURCE,[uuid.getPrettyName(objectUUID) for objectUUID in available_object],enterIsNone=True) #TEXT
				if choice == -1:
					outObjectUUID = "0"
				else:
					outObjectUUID = available_object[choice]
			elif len(available_object) == 1 :
				outObjectUUID = available_object[0]
			else:
				warn(f"No available container with specified type (defaulted to {uuid.getPrettyName(getConfig('0'))})") #TEXT
				outObjectUUID = getConfig("defaultContainerUUID")

		case "ByFilter":
			filters,tolerance = getFilter()
			available_object = guuid.fromFilter(filters,tolerance)
			if len(available_object) > 1:
				info("Multiple object match with selected filter") #TEXT
				choice:int = cutils.Choice("Please choose one (leave empty to skip)",SOURCE,[uuid.getPrettyName(objectUUID) for objectUUID in available_object],enterIsNone=True) #TEXT
				if choice == -1:
					outObjectUUID = getConfig("defaultContainerUUID") #TEXT
				else:
					outObjectUUID = available_object[choice]
			elif len(available_object) == 1 :
				outObjectUUID = available_object[0]
			else:
				cutils.warn(f"No available container match with selected filter (defaulted to {uuid.getPrettyName(getConfig('defaultContainerUUID'))})") #TEXT
				outObjectUUID = getConfig("defaultContainerUUID")

	return outObjectUUID
