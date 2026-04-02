import sys

from library.server.default import PATH_CONFIG, PATH_DATABASE
from library.server.server import Server
from library.cmdUtils.command import Register, Shell, globalCommands, Command,CommandDir
from library.common import ERROR, debug,info, warn, error, fatal
from library.common import setLoggerInfo, setLoggerError, setLoggerWarn, setLoggerFatal, setLoggerDebug 
from library.common import legalInfo, SOURCE, getSource
from library.object.type import UUID_ROOT, Storage, Uuid
from library.model.type import FilledModel
from library.cli.utils import getCount, getProperty
from library.cli.display import print_properties, print_short, text_short
from library.config import config_scheme , save as saveConfig
from enum import IntEnum, auto
from library.version import Version

import library.cmdUtils.cmdUtils as cutils

class App:
	version = Version("GluonCLI",0)

	def __init__(self)-> None:
		self.CmdHandler = cutils.CmdHandler(SOURCE)
		self.Server = Server()

		self.selected_list:list[Uuid] = []
		self.selected_key:set[Uuid] = set()

		self.current_object:Uuid = UUID_ROOT

		legalInfo()

		setLoggerInfo(lambda text: cutils.info(text,getSource()))
		setLoggerWarn(lambda text: cutils.warn(text,getSource()))
		setLoggerError(lambda text: cutils.error(text,getSource()))
		setLoggerFatal(lambda text: cutils.fatal(text,getSource()))
		setLoggerDebug(lambda text: cutils.debug(text,getSource()))

		info(f"Initializing Gluon-v{self.Server.version_server.version}") #TEXT
		warn("Experimental version, proceed with caution") #TEXT

		Register(
			"help",
			"help command",
			"Show help about a command",
			optional=1
		)(self.cmd_help)

		self.CmdHandler.add_command(CommandDir(
			"reload",
			{
				"*" : Command("*",self.cmd_reload_all),
				"all" : Command("all",self.cmd_reload_all),
				"config" : Command("config",lambda _: self.reload_config()),
				"database" : Command("database",lambda _: self.reload_database()),
				"model" : Command("model",lambda _: self.reload_model())
			},
			"reload (*|all|config|database|model)",
			defaultHandler = Command("reload",self.cmd_reload_all)
		))

		# Register(
		# 	"start",
		# 	"start",
		# 	"start the Gluon server",
		# )(self.cmd_start)

		# Register(
		# 	"stop",
		# 	"stop",
		# 	"stop the Gluon server",
		# )(self.cmd_stop)

		Register(
			"new",
			"new model_name (storage:id)",
			"Create a new object",
			mandatory=1,
			optional=1
		)(self.cmd_new)

		self.CmdHandler.add_command(CommandDir(
			"model",
			{
				#"new" : Command("new",self.cmd_model_new,optional=1),
				"list": Command("list",self.cmd_model_list)				
			},
			"model list",
			"Various model utility"
		))

		self.CmdHandler.add_command(CommandDir(
			"show",
			{
				"selected" : Command("selected",self.cmd_show_selected),
			},
			"show (id|selected) ..."
			"show current context or selected objetcs",
			defaultHandler= Command("show",self.cmd_show,optional=1)
		))

		Register(
			"select",
			"select localId|*",
			"Select an object in current context",
			mandatory=1,
		)(self.cmd_select)

		Register(
			"unselect",
			"unselect selectedId|*",
			"Unselect an object in current context",
			mandatory=1,
		)(self.cmd_unselect)

		self.CmdHandler.add_command(CommandDir(
			"go",
			{
				"to" : Command("to",self.cmd_go_to,mandatory=1),
				"back" : Command("back",self.cmd_go_back)
			},
			"go <back|to id>","" \
			"Move around universe"
		))

		Register(
			"destroy",
			"destroy id",
			"destroy an object",
			mandatory=1,
		)(self.cmd_destroy)

		Register(
			"decrease",
			"decrease id amount",
			"Decrease an object count based on provided amount",
			mandatory=2
		)(self.cmd_decrease)

		Register(
			"increase",
			"increase id amount",
			"Increase an object count based on provided amount",
			mandatory=2
		)(self.cmd_increase)

		Register(
			"save",
			"save (path)",
			"Save database to path or default value",
			optional=1,
		)(self.cmd_save)

		Register(
			"move",
			"move objectId toId",
			"Move an object to specified id",
			mandatory=2
		)(self.cmd_move)

		Register(
			"version",
			"version (moduleName)",
			"Show version for the specified module (or all)",
			optional=1
		)(self.cmd_version)

		Register(
			"config",
			"config (configKey)",
			"Allow to configure application parameters",
			optional=1
		)(self.cmd_config)

		self.CmdHandler.add_multiple_command(globalCommands)
		self.Server.start()

		info("Gluon server has successfuly been initialized") #TEXT
		if self.Server.Config["Username"] != None:
			info(f"Welcome {self.Server.Config['Username']}") #TEXT
		else:
			info("You can configure the app via the 'config' command")

	class ERROR(IntEnum):
		INVALID_ARGUMENT = auto()
		INVALID_LOCAL_INDEX = auto()
		INVALID_SELECTED_INDEX = auto()
		INVALID_UUID = auto()
		UNEXPECTED = auto()

	def cmd_help(self,input:Shell) -> None:
		if len(input) == 0:
			for command in self.CmdHandler.cmd_list.values():
				info("- " + command.syntax)
				info("\t" + command.desc)
				info("\tusage : "+ command.usage)

		if len(input) == 1:
			for command in self.CmdHandler.cmd_list.values():
				if input[0] == command.syntax:
					info("- " + command.syntax)
					info("\t" + command.desc)
					info("\tusage : "+ command.usage)
					break
			else:
				error(f"Unrecognised commande : '{input[0]}'")
				return

	def reload_database(self):
		info(f"Reloading database")
		self.Server.loadDatabase(PATH_DATABASE)
		info(f"Loaded {len(self.Server.Database.objects)} object(s)")

	def reload_config(self):
		info(f"Reloading config")
		self.Server.loadConfig(PATH_CONFIG) 
		
	def reload_model(self):
		info(f"Reloading model library")
		self.Server.loadModels(self.Server.Config["ModelLibraryPath"])
		info(f"Loaded {len(self.Server.Model_library)} model(s)")

	def cmd_reload_all(self, shell:Shell):
		self.reload_config()
		self.reload_model()
		self.reload_database()

	def cmd_start(self, shell: Shell):
		if not self.Server.Initialized:
			self.Server.start()
		else:
			warn("Server already started")

	def cmd_stop(self, shell : Shell):
		warn("NYI")

	def index(self,index_str:str) -> tuple[int,Uuid]:
		PREFIX_SELECTED = "$"
		PREFIX_UUID = "@"

		if index_str.startswith(PREFIX_SELECTED):
			index_strip = index_str.removeprefix(PREFIX_SELECTED)
			if not index_strip.isdigit():
				return App.ERROR.INVALID_ARGUMENT,""
			if int(index_strip) < 1 or int(index_strip) > len(self.selected_list):
				return App.ERROR.INVALID_SELECTED_INDEX,""
			
			return 0,self.selected_list[int(index_strip)-1]
		elif index_str.startswith(PREFIX_UUID):
			index_strip = index_str.removeprefix(PREFIX_UUID)
			if index_strip not in self.Server.Database.objects:
				return App.ERROR.INVALID_UUID,""
			return 0,index_strip
		else:
			if not index_str.isdigit():
				return App.ERROR.INVALID_ARGUMENT,""
			current_ = self.Server.Database.objects[self.current_object]
			if isinstance(current_,Storage):
				if int(index_str) < 1 or int(index_str) > len(current_.childs):
					return App.ERROR.INVALID_LOCAL_INDEX,""
			
				return 0,current_.childs[int(index_str)-1]
			return App.ERROR.UNEXPECTED,""

	def cmd_new(self,shell: Shell):
		
		model = self.Server.Model_library.get(shell[0])
		if model == None:
			error(f"Unrecognised model name : '{shell[0]}'")
			info("Use 'model list' to get available models")
			return

		filled = FilledModel()
		filled.model = model

		filled.count = getCount()

		for property_name,property in model.properties.items():
			filled.properties[property_name] = getProperty(property_name,property)

		target = UUID_ROOT
		text = f"Created new <{model.name}>"
		if len(shell) > 1:
			res, target = self.index(shell[1])
			if res != 0:
				error(f"Invalid Index '{shell[1]}', error code : {res}")
				return
			target_ = self.Server.Database.objects[target]
			text += f" inside [{shell[1]}] of type <{target_.model.name}>"

		self.Server.Database.create(filled,target)
		info(text)

	def show_storage(self,uuid):
		storage_ = self.Server.Database.objects[uuid]
		if not isinstance(storage_, Storage):
			return

		print('Stored objects : ')
		if len(storage_.childs) == 0:
			print("Nothing to see here...")
		for i,childUuid in enumerate(storage_.childs,start=1):
			text = text_short(self.Server.Database.objects[childUuid])
			print(f"{'*' if childUuid in self.selected_key else " "}[{i}] : {text}")

	def show_current(self):
		current_ = self.Server.Database.objects[self.current_object]
		print_short(current_)	
		self.show_storage(self.current_object)

	def show_uuid(self,uuid:Uuid):
		object_ = self.Server.Database.objects[uuid]
		print("")
		print_short(object_)
		print_properties(object_)
		self.show_storage(uuid)

	def cmd_show(self, shell:Shell):
		if len(shell) == 0:
			self.show_current()
		elif len(shell) == 1:
			res, uuid = self.index(shell[0])
			if res != 0:
				error(f"Invalid Index '{shell[0]}', error code : {res}")
				return
			self.show_uuid(uuid)

	def cmd_show_selected(self, shell:Shell):
		if len(self.selected_list) == 0:
			info("No object currently selected")
			return
		for i,object_uuid in enumerate(self.selected_list,start=1):
			object = self.Server.Database.objects[object_uuid]
			print(f"[{i}] : {text_short(object)}")

	def cmd_move(self, shell:Shell):
		res, target = self.index(shell[0])
		if res != 0:
			error(f"Invalid Index '{shell[0]}', error code : {res}")
			return
		res, storage = self.index(shell[1])
		if res != 0:
			error(f"Invalid Index '{shell[1]}', error code : {res}")
			return
		if target == storage:
			error("Cannot save object inside itself")
			return
		if target == UUID_ROOT:
			error("Cannot move the universe")
			return
		if(res := self.Server.Database.moveObject(target,storage)) != 0:
			error(f"error code : {res}")
		

	def select_add(self,*uuidList:Uuid):
		for uuid in uuidList:
			if uuid in self.selected_key:
				continue
			self.selected_key.add(uuid)
			self.selected_list.append(uuid)
			info(f"Selected : {text_short(self.Server.Database.objects[uuid])}")

	def select_remove(self,*uuidIndex:int):
		for index in uuidIndex:
			if index > len(self.selected_key):
				continue
			if index < 0:
				continue
			object_uuid = self.selected_list.pop(index)
			self.selected_key.remove(object_uuid)
			object_object = self.Server.Database.objects[object_uuid]
			info(f"Unselected : {text_short(object_object)}")

	def cmd_select(self, shell:Shell):
		current_ = self.Server.Database.objects[self.current_object]
		if not isinstance(current_,Storage):
			error("Current object isn't a storage")
			return

		if shell[0] == "*":
			self.select_add(*current_.childs)
			return

		res, target = self.index(shell[0])
		if res != 0:
			error(f"Invalid Index '{shell[0]}', error code : {res}")
			return
		
		if target in self.selected_key:
			error("Object already selected")
			return

		self.select_add(target)			

	def cmd_unselect(self, shell:Shell):
		if shell[0] == "*":
			self.select_remove(*range(len(self.selected_list)))
		if not shell[0].isdigit():
			error(f"unrecognized argument {shell[0]}")
			return
		if int(shell[0]) < 1 or int(shell[0])  > len(self.selected_list):
			error(f"Invalid selected index {shell[0]}")
			return
		
		self.select_remove(int(shell[0])-1)

	def cmd_model_new(self, shell:Shell):
		...

	def cmd_model_list(self, shell:Shell):
		info(f"Currently {len(self.Server.Model_library)} loaded model(s) :")
		for model_name in self.Server.Model_library:
			print("\r" +model_name)

	def cmd_go_to(self, shell:Shell):
		object_ = self.Server.Database.objects[self.current_object]
		if not isinstance(object_,Storage):
			error("Current object isn't a storage")	
			return

		res, target = self.index(shell[0])
		if res != 0:
			error(f"Invalid Index '{shell[0]}', error code : {res}")
			return
		target_ = self.Server.Database.objects[target]

		if not isinstance(target_,Storage):
			error(f"Target index isn't a storage")
			return

		info(f"Moved to {text_short(target_)}")
		self.current_object = target

	def cmd_go_back(self, shell:Shell):
		if self.current_object == UUID_ROOT:
			error("Can't go past the Universe (yet)")
			return
		object_ = self.Server.Database.objects[self.current_object]
		self.current_object = object_.parent

	def cmd_destroy(self, shell:Shell):
		res, target = self.index(shell[0])
		if res != 0:
			error(f"Invalid Index '{shell[0]}', error code : {res}")
			return
		if target == self.current_object:
			error("Trying to delete current object")
			return
		if(res := self.Server.Database.destroy(target)) != 0:
			if res == ERROR.MODIFIYING_UNIVERSE:
				error("Trying to delete the universe")
			else:
				error(f"error code : {ERROR.from_bytes}")
			return

		if target == UUID_ROOT:
			error("Trying to delete the universe")
			return
		
		if target in self.selected_key:
			self.selected_list.remove(target)
			self.selected_key.remove(target)

	def cmd_increase(self,shell:Shell):
		res, target = self.index(shell[0])
		if res != 0:
			error(f"Invalid Index '{shell[0]}', error code : {res}")
			return
		target_ = self.Server.Database.objects[target]
		if isinstance(target_,Storage) and not target_.isEmpty():
			error("Cannot modify quantity of non-empty storage")
			return

		if not shell[1].isdigit():
			error(f"Invalid quantity '{shell[1]}'")
			return
		
		quantity = int(shell[1])
		target_.increase(quantity)

	def cmd_decrease(self,shell:Shell):
		res, target = self.index(shell[0])
		if res != 0:
			error(f"Invalid Index '{shell[0]}', error code : {res}")
			return
		target_ = self.Server.Database.objects[target]
		if isinstance(target_,Storage) and not target_.isEmpty():
			error("Cannot modify quantity of non-empty storage")
			return

		if not shell[1].isdigit():
			error(f"Invalid quantity '{shell[1]}'")
			return
		
		quantity = int(shell[1])
		target_.decrease(quantity)

	def cmd_save(self, shell:Shell):
		savePath = shell[0] if len(shell) != 0 else PATH_DATABASE
		info(f"Saving to '{savePath}'")
		res = self.Server.saveDatabase(savePath)
		if res != 0:
			error(f"error code : {res}")
		return

	def cmd_version(self,shell:Shell):
		info("Version:")
		if len(shell) == 1:
			res = Version.modules.get(shell[0])
			if res ==None:
				error(f"Unknown module '{shell[0]}'")
			else:
				info(f"{shell[0]} : {res}")
		else:
			for name,version in Version.modules.items():
				info(f"{name} : {version}")

	def cmd_exit(self,shell:Shell) -> None:
		exitCode:str = shell[0] if len(shell) > 0 else ""
		if cutils.Validate("Voulez vous quitter ?",SOURCE,enterIsYes=True): #TEXT
			sys.exit(exitCode)

	def cmd_config(self, shell:Shell) -> None:
		config_key_list = list(config_scheme.keys())
		config_key = config_key_list[0]
		if len(shell) == 0:
			index = cutils.Choice("Select a value to edit",SOURCE,config_key_list)
			config_key = config_key_list[index]
		else:
			if shell[0] not in config_scheme:
				error("Invalid config key provided")
				return
			else:
				config_key = shell[0]
		current_value = self.Server.Config.get(config_key)
		info(f"Current value for key '{config_key}' = {current_value}")
		new_value = getProperty(config_key,config_scheme[config_key])
		res = cutils.Validate(f"Replace '{current_value}' by '{new_value}' ?",SOURCE,True)
		if not res:
			info("Cancelling")
			return
		self.Server.Config[config_key] = new_value
		saveConfig(self.Server.Config,PATH_CONFIG)
