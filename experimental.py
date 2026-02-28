import library.object.universe as universe
import library.cmdUtils.cmdUtils as cutils
from library.common import legalInfo, Version, info, warn, error, SOURCE, setLoggerInfo, setLoggerError, setLoggerWarn, setLoggerFatal, setLoggerDebug , getSource
from library.config import loadConfig
from library.model.loader.loader import constructModels
import sys
import library.user_interface.command

def main() -> None:	
	legalInfo() #TEXT

	cutils.toggleInternalDebug()
	cmd = cutils.CmdHandler(SOURCE)

	setLoggerInfo(lambda text: cutils.info(text,getSource()))
	setLoggerWarn(lambda text: cutils.warn(text,getSource()))
	setLoggerError(lambda text: cutils.error(text,getSource()))
	setLoggerFatal(lambda text: cutils.fatal(text,getSource()))
	setLoggerDebug(lambda text: cutils.debug(text,getSource()))

	Omega = universe.Universe()

	info(f"Initializing Gluon-{Version}") #TEXT

	config = loadConfig("./env/config.json")
	model = constructModels("./env/model/example/")
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
