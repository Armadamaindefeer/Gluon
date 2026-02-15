import library.object as object
import library.cmdUtils.cmdUtils as cutils
from library.cmdUtils.command import globalCommands, Wrapper
from library.common import legalInfo, Version, Version_changelog, Version_history, info, isInteger, warn, error, SOURCE, genUUID
from library.config import getConfig, RAW_CONFIG, loadConfig
from library.model.loader import loadModels
import json
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

@Wrapper("changelog", "changelog","Get changelog for selected version",needQuantity=0) #TEXT
def _changelog(input:cutils.InputParameter) -> None:
	available_version = Version_history
	choice:int = cutils.Choice("Select version (sorted from earliest to latest)",SOURCE,available_version) #TEXT

	info(f"Changelog for version {available_version[choice]} :") #TEXT
	if len(Version_changelog[available_version[choice]]) > 0:
		for entry in Version_changelog[available_version[choice]]:
			info(f"- {entry}")
	else:
		info("- No Changelog") #TEXT

def main() -> None:	
	legalInfo() #TEXT

	cutils.toggleInternalDebug()
	cmd = cutils.CmdHandler(SOURCE)
	Omega = object.Universe()

	info(f"Initializing Gluon-{Version}") #TEXT

	loadConfig("./config.json")
	loadModels("./model/")
	warn("Experimental version, proceed with caution")

	latestVersion = getConfig("latestVersion")
	latestVersionIndex = Version_history.index(latestVersion)
	for i,version in enumerate(Version_history[latestVersionIndex+1::]):
			info(f"Changelog for version {version} :")
			if len(Version_changelog[version]) > 0:
				for entry in Version_changelog[version]:
					info(f"- {entry}")
			else:
				info("- No Changelog")

	RAW_CONFIG()["latestVersion"] = Version
	json.dump(RAW_CONFIG(),open("./config.json","wt"),indent="\t",ensure_ascii=False)

	info("Gluon launch has succeed") #TEXT
	info(f"Welcome {getConfig('username')}") #TEXT

	running = True
	while running:
		try :
			cmd.handle_input()
		except KeyboardInterrupt:
			if cutils.Validate("Voulez vous quitter ?",SOURCE,enterIsYes=True): #TEXT
				if getConfig("saveOnExit"):
					...
				sys.exit()

if __name__ == "__main__":
	main()
