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

import json
import os

from library.utils.common import Version, Version_history, jsonError, jsonErrorSystem, jsonInfo, jsonUseDefault, jsonWarn, jsonWrongType, error, info, warn, Source

config = {}

SOURCE = "Configurator"

config_default = {
	"username" : "user",
	"defaultInputMethod" : "ByUUID",
	"defaultContainerUUID" : "0",
	"defaultContainerName" : "Omega",
	"defaultContainerType" : "Universe",
	"saveOnExit" : True,
	"latestVersion" : Version
}


config_model ={
	"username" : { "type" : "string","allowNone" : False},
	"defaultInputMethod" : { "type" : "choice", "available" : ["ByUUID","ByName","ByType","ByFilter","Ask"],"allowNone" : False},
	"defaultContainerUUID" : {"type" :  "object", "objectType" : "uuid","allowNone" : False},
	"defaultContainerName" : {"type" : "object", "objectType" : "name","allowNone" : False},
	"defaultContainerType" : {"type" : "object", "objectType" : "type","allowNone" : False},
	"saveOnExit" : {"type"	: "bool","allowNone" : False},
	"latestVersion" : {"type" : "choice", "available" : Version_history, "canUserEdit" : False}
}

def getConfigModel() -> dict:
	return config_model

@Source(SOURCE)
def getConfig(name:str) -> str:
	if name not in config:
		error(f"Key {name} not in config")		
	else:
		return config[name]
	return ""

@Source(SOURCE)
def loadConfig(path : str):
	global config

	
	info('Loading config file')
	if not os.path.isfile(path):
		config = config_default
		json.dump(config,open(path,"wt"),indent="\t",ensure_ascii=False)
	else:
		try :
			temp = json.load(open(path))
		except json.decoder.JSONDecodeError as errorMsg:
			jsonErrorSystem(errorMsg,path)
		else:
			if type(temp) != dict:
				jsonWrongType(dict,type(temp),path) 

			for key,data in temp.items():
				keyPath = f"{path}::{key}"

				if key not in list(config_model.keys()):
					warn(f"in ({path}) : unknown key {key}")
					temp.pop(key)

				if config_model[key]["type"] == "choice" and type(data) != str:
					jsonWrongType(str,type(data),keyPath)
					jsonUseDefault(config_default[key],keyPath)
					temp[key] = config_default[key]

				elif config_model[key]["type"] == "choice" and data not in config_model[key]["available"]:
					jsonError(f"Expected value to be in : {config_model[key]['available']}, got {data}",keyPath)
					jsonUseDefault(config_default[key],keyPath)
					temp[key] = config_default[key]

				elif config_model[key]["type"] == "bool" and type(data) != bool:
					jsonWrongType(bool,type(data),keyPath)
					jsonUseDefault(config_default[key],keyPath)
					temp[key] = config_default[key]

				elif config_model[key]["type"] == "object" and type(data) != str:
					jsonWrongType(bool,type(data),keyPath)
					jsonUseDefault(config_default[key],keyPath)
					temp[key] = config_default[key]

			for key in config_default.keys():
				if key not in temp:
					jsonWarn(f"Missing key {key}",path)
					jsonUseDefault(config_default[key],path)
					temp[key] = config_default[key]

			config = temp
	json.dump(config,open(path,"wt"),indent="\t",ensure_ascii=False)
	info("Done !")


def RAW_CONFIG():
	return config
