from library.object.universe import Universe
import library.model.type as model_type
from library.common import info, error, warn, debug, fatal, ERROR
from library.config import loadConfig, save as saveConfig
from library.model.loader.loader import constructModels
from library.object.factory import make_dict
import library.object.type as object_type
from library.server.default import PATH_CONFIG, PATH_DATABASE
from library.version import Version

import sys
import json
import os

class Server:
	version_server = Version("GluonServer",0)
	version_database_loader = Version("database_loader",1)

	def __init__(self) -> None:
		self.Database:Universe = Universe()
		self.Config = dict()	
		self.Model_library:dict[str,model_type.Model] = dict()
		self.Initialized = False
	
	def loadConfig(self,path:str) -> int:
		self.Config = loadConfig(path)
		return 0

	def loadModels(self,path:str) -> int:
		self.Model_library = constructModels(path)
		return 0

	def loadDatabase(self,path:str) -> int:

		if not os.path.exists(path):
			return self.saveDatabase(path)
		
		data = {}
		with open(path,"rt",encoding="utf-8") as f:
			data = json.load(f)
		if "version" not in data:
			return ERROR.UNKNOWN_VERSION
		if data["version"] != Server.version_database_loader.version:
			return ERROR.UNKNOWN_VERSION
		if "data" not in data:
			return ERROR.MALFORMED_DATABASE
		if type(data["data"]) != dict:
			return ERROR.MALFORMED_DATABASE

		self.Database.objects = {}
		self.Database.objects[object_type.UUID_ROOT] = self.Database

		for uuid,object_dict in data["data"].items():
			if uuid == object_type.UUID_ROOT:
				self.Database.childs = object_dict["child"]
				continue

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

			if object_dict["model"] not in self.Model_library:
				error_model = model_type.Faulty()
				error_model.target_model = object_dict["model"]
				object_.model = error_model
			else:
				object_.model = self.Model_library[object_dict["model"]]
			
			self.Database.objects[uuid] = object_

		return 0

	def saveDatabase(self,save_path=PATH_DATABASE) -> int:
		save_data = {
			"version" : 1,
			"data" : {}
		}

		for object_ in self.Database.objects.values():
			save_data["data"][object_.uuid] =  make_dict(object_)[1]
		try:
			os.makedirs(os.path.dirname(save_path),exist_ok=True)
		except OSError as e:
			error(e)
			return ERROR.UNEXPECTED
		with open(save_path,"wt",encoding="utf-8") as o:
			json.dump(save_data,o,ensure_ascii=False,indent="\t")
		return 0

	def start(self):
		if (res := self.loadConfig(PATH_CONFIG)) != 0:
			fatal(f"Could not load config (code : {res})")

		Model_library_path = self.Config["ModelLibraryPath"]

		if(res := self.loadModels(Model_library_path)) != 0:
			fatal(f"Could not load model library (code : {res})")
			self.exit(res)
			
		if(res := self.loadDatabase(PATH_DATABASE)) != 0:
			fatal(f"Could not load model library")
			self.exit(res)

	def exit(self,error_code):
		self.saveDatabase(PATH_DATABASE)
		saveConfig(self.Config,PATH_CONFIG)
		sys.exit(error_code)
