from library.object.universe import Universe
import library.model.type as model_type
from library.common import info, error, warn, debug, fatal, ERROR
from library.config import loadConfig
from library.model.loader.loader import constructModels
from library.object.factory import make_dict
import library.object.type as object_type

import sys
import json
import os

class Server:
	def __init__(self) -> None:
		self.Database:Universe = Universe()
		self.Database_path = ""
		self.Config = dict()	
		self.Config_path = ""
		self.Model_library:dict[str,model_type.Model] = dict()
		self.Model_library_path = ""
		self.Initialized = False
	
	def loadConfig(self,path) -> int:
		self.Config = loadConfig(path)
		return 0

	def loadModels(self,path) -> int:
		self.Model_library = constructModels(path)
		return 0

	def loadDatabase(self,path) -> int:
		data = {}
		if not os.path.exists(path):
			return ERROR.UNEXISTANT_FILE
		with open(path,"rt",encoding="utf-8") as f:
			data = json.load(f)
		if "version" not in data:
			return ERROR.UNKNOWN_VERSION
		if data["version"] != 1:
			return ERROR.UNKNOWN_VERSION
		if "data" not in data:
			return ERROR.MALFORMED_DATABASE
		if type(data["data"]) != dict:
			return ERROR.MALFORMED_DATABASE

		self.Database.objects = {}

		for uuid,object_dict in data["data"].items():
			if type(uuid) != str:
				continue
			if type(object_dict) != dict:
				continue
			object_ = None
			match object_dict["type"]:
				case "Basic":
					object_ = object_type.Generic()
				case "Storage":
					object_ = object_type.Storage()
					object_.childs = object_dict["child"]
				case _:
					object_ = object_type.Generic()
			object_.properties = object_dict["properties"]
			object_.count = object_dict["count"]
			object_.parent = object_dict["parent"]
			object_.type = object_dict["type"]
			object_.uuid = uuid
			if uuid == object_type.UUID_ROOT:
				object_.model = model_type.Universe()
			elif object_dict["model"] not in self.Model_library:
				error_model = model_type.Faulty()
				error_model.target_model = object_dict["model"]
				object_.model = error_model
			else:
				object_.model = self.Model_library[object_dict["model"]]
			
			self.Database.objects[uuid] = object_

		return 0

	def saveDatabase(self,save_path) -> int:
		save_data = {
			"version" : 1,
			"data" : {}
		}
		for object_ in self.Database.objects.values():
			save_data["data"][object_.uuid] =  make_dict(object_)[1]
		with open(save_path,"wt",encoding="utf-8") as o:
			json.dump(save_data,o,ensure_ascii=False,indent="\t")
		return 0

	def start(self,config_path:str,database_path:str,model_library_path:str):
		self.Config_path = config_path
		self.Database_path = database_path
		self.Model_library_path = model_library_path
		if(res := self.loadConfig(config_path)) != 0:
			fatal(f"Could not load config (code :{res})")
			self.exit(res)
		if(res := self.loadModels(model_library_path)) != 0:
			fatal(f"Could not load model library (code : {res})")
			self.exit(res)

		if os.path.exists(self.Database_path):
			res = self.loadDatabase(database_path)
			if res != 0:
				fatal(f"Could not load database (code : {res})")
				self.exit(res)			
		self.Initialized = True

	def exit(self,error_code):
		self.saveDatabase(save_path=self.Config["defaultSavePath"])
		sys.exit(error_code)
