from library.object.universe import Universe
from library.common import info, error, warn, debug, fatal
from library.config import loadConfig
from library.model.loader.loader import constructModels

import sys

class Server:
	def __init__(self) -> None:
		self.Database:Universe = Universe()
		self.Database_path = ""
		self.Config = dict()	
		self.Config_path = ""
		self.Model_library = dict()
		self.Model_library_path = ""
		self.Initialized = False
	
	def loadConfig(self,path) -> int:
		self.Config = loadConfig(path)
		return 0

	def loadModels(self,path) -> int:
		self.Model_library = constructModels(path)
		return 0

	def loadDatabase(self,path) -> int:
		warn(f"Currently, the database isn't loaded from/to disk")
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
