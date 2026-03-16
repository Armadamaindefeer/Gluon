from library.object.universe import Universe
from library.model.type import Model
from library.common import info, error, warn, debug, fatal, ERROR
from library.config import loadConfig
from library.model.loader.loader import constructModels
from library.object.factory import make_dict

import sys
import json

class Server:
	def __init__(self) -> None:
		self.Database:Universe = Universe()
		self.Database_path = ""
		self.Config = dict()	
		self.Config_path = ""
		self.Model_library:dict[str,Model] = dict()
		self.Model_library_path = ""
		self.Initialized = False
	
	def loadConfig(self,path) -> int:
		self.Config = loadConfig(path)
		return 0

	def loadModels(self,path) -> int:
		self.Model_library = constructModels(path)
		return 0

	def loadDatabase(self,path) -> int:
		warn(f"Currently, the database isn't loaded from disk")
		data = {}
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
		if(res := self.loadDatabase(database_path)) != 0:
			fatal(f"Could not load database (code : {res})")
			self.exit(res)
		if(res := self.loadModels(model_library_path)) != 0:
			fatal(f"Could not load model library (code : {res})")
			self.exit(res)
		self.Initialized = True

	def exit(self,error_code):
		sys.exit(error_code)
