# Gluon , a terminal-based inventory manager
# Copyright (C) 2022-2025 Simon Alligand | Arma_mainfeer
# contact : simon.alligand@gmail.com

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import typing
import uuid
import json
import enum

Version_changelog:dict[str,list[str]] = {
	"alpha-v0.0.0": ["Starting experimental rewrite","Currently no useable database","Incompatible with previous installation","run stable.py if you want previous stable version"]
}

Version_history = list(Version_changelog.keys())

Version = "alpha-v0.0.0"

Uuid = str

def genUUID(existing:set):
	new_uuid = uuid.uuid4().hex
	while new_uuid in existing:
		new_uuid = uuid.uuid4().hex
	return new_uuid	

def isInteger(value:int|float) -> bool:
	if type(value) == int:
		return True
	elif type(value) == float:
		return value.is_integer()
	else:
		return False

########################################################################################
#
# Logging
#
########################################################################################

SOURCE = "Gluon-Experimental"
OLD_SOURCE:list[str] = []

def AcquireSource(temp:str):
	global SOURCE
	global OLD_SOURCE
	OLD_SOURCE += [SOURCE]
	SOURCE = temp

def ReleaseSource():
	global SOURCE
	global OLD_SOURCE
	SOURCE = OLD_SOURCE.pop()

def getSource() -> str:
	return SOURCE

def Source(source: str):
	def __wrapper(func:typing.Callable):			
		def __wrapped_wrapper(*args,**kwargs):
			AcquireSource(source)
			temp =  func(*args,**kwargs)
			ReleaseSource()
			return temp
		return __wrapped_wrapper
	return __wrapper

def log(level,source,text):
	print(f"[{level}]({source}) : {text}")

logger = {
	"INFO" : lambda text:log("INFO",SOURCE,text),
	"WARN" : lambda text:log("WARN",SOURCE,text),
	"ERROR" : lambda text:log("ERROR",SOURCE,text),
	"FATAL" : lambda text:log("FATAL",SOURCE,text),
	"DEBUG" : lambda text:log("DEBUG",SOURCE,text),

}

def info(text):
	logger["INFO"](text)

def warn(text):
	logger["WARN"](text)

def error(text):
	logger["ERROR"](text)

def fatal(text):
	logger["FATAL"](text)

def debug(text):
	logger["DEBUG"](text)

def setLogger(logger:typing.Callable):
	global log
	log = logger

def setLoggerInfo(infoLogger):
	logger["INFO"] = infoLogger

def setLoggerWarn(warnLogger):
	logger["WARN"] = warnLogger

def setLoggerError(errorLogger):
	logger["ERROR"] = errorLogger

def setLoggerFatal(fatalLogger):
	logger["FATAL"] = fatalLogger

def setLoggerDebug(debugLogger):
	logger["DEBUG"] = debugLogger

def CtrlInfo():
	info("Press CTRL + C to cancel")

LEGAL_COMMAND_AVAILABLE = False
def legalInfo():
	print("Gluon  Copyright (C) 2022-2026  Simon Alligand | Arma_mainfeer")
	print("This program comes with ABSOLUTELY NO WARRANTY",end="")
	if LEGAL_COMMAND_AVAILABLE:
		print(";for details type `show w'.")
	else:
		print(".")
	print("This is free software, and you are welcome to redistribute it")
	if LEGAL_COMMAND_AVAILABLE:
		print("under certain conditions; type `show c' for details.")


########################################################################################
#
# Json related logging
#
########################################################################################

def printJson(object):
	print(json.dumps(object,ensure_ascii=False,indent="\t"))

def jsonMsg(msg,path) -> str:
	return f'In ({path})\t: {msg}'

@Source("JSON_READER")
def jsonInfo(msg,path):
	info(jsonMsg(msg,path))

@Source("JSON_READER")
def jsonWarn(msg,path):
	warn(jsonMsg(msg,path))

@Source("JSON_READER")
def jsonError(msg,path):
	error(jsonMsg(msg,path))

@Source("JSON_READER")
def jsonFatal(msg,path):
	fatal(jsonMsg(msg,path))

def jsonWrongType(expected,got,path):
	jsonError(f"expected type : {expected}, got {got}",path)

def jsonUseDefault(defaultValue,path):
	jsonInfo(f"Correcting to default value ({defaultValue})",path)

@Source("JSON_DECODER")
def jsonErrorSystem(errorMsg,path):
	error(f"in ({path}) at [{errorMsg.lineno},{errorMsg.colno}] : {errorMsg.msg}")

class ERROR(enum.IntFlag):
	MODIFIYING_UNIVERSE		= enum.auto()
	CREATING_UNIVERSE		= enum.auto()
	HAS_PARENT				= enum.auto()
	ALREADY_STORED			= enum.auto()
	NOT_STORED				= enum.auto()
	NOT_A_STORAGE			= enum.auto()
	NOT_EMPTY				= enum.auto()
	STACKED_STORAGE			= enum.auto()
	SAME_OBJECT				= enum.auto()
	UNEXPECTED				= enum.auto()
	DOES_NOT_EXIST			= enum.auto()
	JSON_DECODER_ERROR		= enum.auto()
	VERSION_OUTDATED		= enum.auto()
	UNKNOWN_VERSION			= enum.auto()
	MALFORMED_PARENT		= enum.auto()
	MALFORMED_TYPE			= enum.auto()
	MALFORMED_PROPERTY		= enum.auto()
	MALFORMED_ALIAS			= enum.auto()
	MALFORMED_ISCATEGORY	= enum.auto()
	
