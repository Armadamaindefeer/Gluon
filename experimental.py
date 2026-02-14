import library.object as object
import library.cmdUtils.cmdUtils as cutils
from library.cmdUtils.command import globalCommands, Wrapper
from library.common import CtrlInfo, Version, Version_changelog, Version_history, info, isInteger, warn, error, SOURCE, genUUID
from library.utils.config import getConfig, RAW_CONFIG, loadConfig
import json
import sys

def main() -> None:	
	cutils.toggleInternalDebug()
	cmd = cutils.CmdHandler(SOURCE)

	info(f"Running Virgil {Version}") #TEXT

	loadConfig("./config.json")
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

	info("Virgil launch has succeed") #TEXT
	print("Gluon  Copyright (C) 2022-2026  Simon Alligand | Arma_mainfeer")
	#print("This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.")
	print("This program comes with ABSOLUTELY NO WARRANTY.")
	print("This is free software, and you are welcome to redistribute it")
	#print("under certain conditions; type `show c' for details.")

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
