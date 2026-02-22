import library.object as object
import library.cmdUtils.cmdUtils as cutils
from library.cmdUtils.command import globalCommands, Wrapper
from library.common import legalInfo, Version, info, warn, error, SOURCE, setLoggerInfo, setLoggerError, setLoggerWarn, setLoggerFatal, setLoggerDebug , getSource
from library.config import loadConfig
from library.model.loader import loadModels
import sys

@Wrapper("exit","exit exitCode","Exit application on use",maxQuantity=1) #TEXT
def _exit(input : cutils.InputParameter) -> None:
	exitCode:str = input[0] if len(input.input) > 0 else ""
	if cutils.Validate("Voulez vous quitter ?",SOURCE,enterIsYes=True): #TEXT
		sys.exit(exitCode)

@Wrapper("help","help (TOPIC ENTRY)","Show help", maxQuantity=2) #TEXT
def _help(input:cutils.InputParameter) -> None:
	topicData = {
		"Command": {
			"desc" : "Show all available commands", #TEXT
			"entry" : {command.call_name:(command.desc,command.usage) for command in globalCommands},
		},
	}

	if len(input) == 0:
		info("List of available topic, type \'help <topic>\'")
		for topicName,topicData in topicData.items():
			info(f"{topicName} : {topicData['desc']}")

	elif len(input) > 0:
		if input[0] not in list(topicData.keys()):

			return error(f"Unknown topic \"{input[0]}\"")
	
		if len(input) == 1:
			info(f"Available entry for {input[0]}")
			for topicEntryName,topicEntry in topicData[input[0]]["entry"].items():
				info(f"{topicEntryName} : {topicEntry[0]}")

		elif len(input) == 2:
			if input[1] not in topicData[input[0]]["entry"]:
				print(topicData[input[0]])
				return error(f"Unknown entry \"{input[1]}\" for topic \"{input[0]}\"")
			info(f'{input[0]}: {input[1]}')
			info(f"{topicData[input[0]]['entry'][input[1]][0]}")
			info("")
			info(f"{topicData[input[0]]['entry'][input[1]][1]}")

def main() -> None:	
	legalInfo() #TEXT

	cutils.toggleInternalDebug()
	cmd = cutils.CmdHandler(SOURCE)

	setLoggerInfo(lambda text: cutils.info(text,getSource()))
	setLoggerWarn(lambda text: cutils.warn(text,getSource()))
	setLoggerError(lambda text: cutils.error(text,getSource()))
	setLoggerFatal(lambda text: cutils.fatal(text,getSource()))
	setLoggerDebug(lambda text: cutils.debug(text,getSource()))

	Omega = object.Universe()

	info(f"Initializing Gluon-{Version}") #TEXT

	config = loadConfig("./env/config.json")
	model = loadModels("./env/model/model_error/")
	warn("Experimental version, proceed with caution") #TEXT

	info("Gluon launch has succeed") #TEXT
	info(f"Welcome {config['username']}") #TEXT

	running = True
	while running:
		try :
			cmd.handle_input()
		except KeyboardInterrupt:
			if cutils.Validate("Voulez vous quitter ?",SOURCE,enterIsYes=True): #TEXT
				sys.exit()

if __name__ == "__main__":
	main()
