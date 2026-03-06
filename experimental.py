import library.cmdUtils.cmdUtils as cutils
from library.common import SOURCE
import sys
from library.cli.app import App

def main() -> None:	
	#cutils.toggleInternalDebug()
	app = App("./env/config.json","./env/database.json","./env/model/example/")

	running = True
	while running:
		try :
			app.CmdHandler.handle_input()
		except KeyboardInterrupt:
			if cutils.Validate("Voulez vous quitter ?",SOURCE,enterIsYes=True): #TEXT
				sys.exit()

if __name__ == "__main__":
	main()
