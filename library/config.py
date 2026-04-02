import os
import json

from library.dataField import default_dict, validate_value, default_schema
from library.common import jsonErrorSystem

config_scheme = {
	"Username" : {"type" : "string","allowNone": True,"default" : None},
	"ModelLibraryPath" : {"type" : "string", "allowNone" : False, "default" : "./env/model/"}
}

def save(data,path):
	os.makedirs(os.path.dirname(path),exist_ok=True)
	with open(path,"wt",encoding="utf-8") as o:
		json.dump(data,o,indent="\t",ensure_ascii=False)

def default_and_save(path):
	out = default_dict(config_scheme)
	save(out,path)
	return out

def loadConfig(path:str) -> dict:
	config = dict()

	if not os.path.exists(path):
		config = default_and_save(path)

	if not (os.path.splitext(path)[1] == ".json"):
		config = default_and_save(path)
	with open(path,"rt") as f:
		try:
			config = json.load(f)
		except json.decoder.JSONDecodeError as error:
			jsonErrorSystem(error,path)
			config = default_and_save(path)

	for key,value in config.items():
		if key not in config_scheme:
			continue
		if not validate_value(value,config_scheme[key]):
			config[key] = default_schema(config_scheme[key])

	for key in config_scheme:
		if key not in config:
			config[key] = default_schema(config_scheme[key])

	save(config,path)
	return config
