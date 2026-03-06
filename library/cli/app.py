from library.server.server import Server
from library.cmdUtils.command import Register, Shell, globalCommands, Command,CommandDir
import library.cmdUtils.cmdUtils as cutils
from library.common import debug,info, warn, error, fatal
from library.common import setLoggerInfo, setLoggerError, setLoggerWarn, setLoggerFatal, setLoggerDebug 
from library.common import legalInfo, Version, SOURCE, getSource
from library.object.type import Uuid

class App:
		
	def __init__(self,config_path:str,database_path:str,model_library_path:str)-> None:
		self.CmdHandler = cutils.CmdHandler(SOURCE)
		self.Server = Server()
		legalInfo()

		setLoggerInfo(lambda text: cutils.info(text,getSource()))
		setLoggerWarn(lambda text: cutils.warn(text,getSource()))
		setLoggerError(lambda text: cutils.error(text,getSource()))
		setLoggerFatal(lambda text: cutils.fatal(text,getSource()))
		setLoggerDebug(lambda text: cutils.debug(text,getSource()))

		info(f"Initializing Gluon-{Version}") #TEXT
		warn("Experimental version, proceed with caution") #TEXT

		Register(
			"reload",
			"reload (*|all|config|model|database)",
			"desc",
			optional=1
		)(self.reload)

		Register(
			"start",
			"start",
			"start the Gluon server",
		)(self.start)

		Register(
			"stop",
			"stop",
			"stop the Gluon server",
		)(self.stop)

		Register(
			"show",
			"show (uuid)",
			"Show current storage location",
			optional=1
		)(self.show)

		Register(
			"new",
			"new model_name",
			"Create a new object",
			mandatory=1
		)(self.new)

		Register(
			"move",
			"move selectedId ...",
			"move selected object into current context",
			mandatory=1,
			optional=-1
		)(self.move)

		Register(
			"select",
			"select localId ...",
			"select one or more object for later use (remain after context change)",
			mandatory=1,
			optional=-1
		)(self.select)

		Register(
			"unselect",
			"unselect (selectedId ...)",
			"unselect one or more object",
			optional=-1
		)(self.unselect)

		self.CmdHandler.add_command(CommandDir(
			"model",
			{
				"new" : Command("new",self.model_new),
				"list": Command("list",self.model_list)				
			}
		))

		self.CmdHandler.add_command(CommandDir(
			"go",
			{
				"to" : Command("to",self.go_to,mandatory=1),
				"back" : Command("back",self.go_back,optional=1)
			},
			"go <to|back> (uuid)",
			"Allow to move inside the universe"
		))

		Register(
			"destroy",
			"destroy localId ...",
			"destroy an object",
			mandatory=1,
			optional=-1
		)(self.destroy)

		self.CmdHandler.add_multiple_command(globalCommands)
		self.Server.start(config_path,database_path,model_library_path)

		self.selected:list[Uuid] = []
		self.context:Uuid = Uuid()

		info("Gluon server has successfuly been initialized") #TEXT
		info(f"Welcome {self.Server.Config['username']}") #TEXT


	def reload(self, shell:Shell):
		if len(shell.input) == 0:
			self.Server.loadConfig(self.Server.Config_path) 
			self.Server.loadDatabase(self.Server.Database_path)
			self.Server.loadModels(self.Server.Model_library_path)
		else:
			match shell.input[0]:
				case "all"|"*":
					info(f"Reloading everything")
					self.Server.loadConfig(self.Server.Config_path) 
					self.Server.loadDatabase(self.Server.Database_path)
					self.Server.loadModels(self.Server.Model_library_path)
				case "database":
					info(f"Reloading database")
					self.Server.loadDatabase(self.Server.Database_path)
				case "config":
					info(f"Reloading config")
					self.Server.loadConfig(self.Server.Config_path) 
				case "model":
					info(f"Reloading model library")
					self.Server.loadModels(self.Server.Model_library_path)
				case _:
					error(f"Unrecognised argument \'{shell.input[0]}\'")

	def start(self, shell: Shell):
		if not self.Server.Initialized:
			self.Server.start(
				self.Server.Config_path,
				self.Server.Database_path,
				self.Server.Model_library_path
			)
		else:
			warn("Server already started")

	def stop(self, shell : Shell):
		warn("NYI")

	def new(self,shell: Shell):
		if shell[0] not in self.Server.Model_library:
			error(f"Unrecognised model name : '{shell[0]}'")
		warn("WIP")

	def show(self,shell:Shell):
		warn("NYI")

	def move(self,shell:Shell):
		warn("NYI")
	
	def select(self, shell:Shell):
		warn("NYI")

	def unselect(self, shell:Shell):
		warn("NYI")

	def model_new(self, shell:Shell):
		warn("NYI")

	def model_list(self, shell:Shell):
		info(f"Currently {len(self.Server.Model_library)} loaded model(s) :")
		for model_name in self.Server.Model_library:
			print("\r" +model_name)

	def go_to(self, shell:Shell):
		warn("NYI")

	def go_back(self, shell:Shell):
		warn("NYI")

	def destroy(self, shell:Shell):
		warn("WIP")
