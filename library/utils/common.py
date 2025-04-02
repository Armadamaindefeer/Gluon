import library.cmdUtils.cmdUtils as cutils

import typing
import uuid
import json

SOURCE = "Virgil"
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
	def __wrapper(func:typing.Callable[[typing.Any],typing.Any]):			
		def __wrapped_wrapper(*args,**kwargs):
			AcquireSource(source)
			temp =  func(*args,**kwargs)
			ReleaseSource()
			return temp
		return __wrapped_wrapper
	return __wrapper


Version_history = ["alpha-v0.1","alpha-v0.2","alpha-v1","alpha-v2","alpha-v3","alpha-v4"]

Version_changelog = {
	"alpha-v0.1" : [],
	"alpha-v0.2" : [],
	"alpha-v1" : ["Add versionning and changelogs"],
	"alpha-v2" : ["Fixed somes bug and still trying to fixe input with Windows"],
	"alpha-v3" : ["Allow absence of \'args\' in models type","Add version tracking", "Fixe bug related to using \'new\' without argument","Now all command can be canceled without triggering exiting", "Add two new unit : hour and kibioctet"],
	"alpha-v4" : ["All object input follow input method config parameter (except direc UUID input from command)","Improved cmdUtils debug utilites","Add LEFT and RIGHT arrow to move cursor while inputing command","Moving debug input utilities to F2"]
}

Version = "alpha-v4"

def debug(text:str):
	cutils.debug(text,SOURCE)

def info(text:str):
	cutils.info(text,SOURCE)

def CtrlInfo():
	info("Press CTRL + C to cancel")

def warn(text:str):
	cutils.warn(text,SOURCE)

def error(text:str):
	cutils.error(text,SOURCE)

def fatal(text:str):
	cutils.fatal(text,SOURCE)

def genUUID(database:dict):
	new_uuid = uuid.uuid4().hex
	while new_uuid in database:
		new_uuid = uuid.uuid4().hex
	return new_uuid	

def printJson(object):
	print(json.dumps(object,ensure_ascii=False,indent="\t"))


def isInteger(value:int|float) -> bool:
	if type(value) == int:
		return True
	elif type(value) == float:
		return value.is_integer()
	else:
		return False


###########################
#
# Json Validation Message
#
###########################

def jsonMsg(msg,path) -> str:
	return f'In ({path})\t: {msg}'

def jsonInfo(msg,path):
	info(jsonMsg(msg,path))

def jsonWarn(msg,path):
	warn(jsonMsg(msg,path))

def jsonError(msg,path):
	error(jsonMsg(msg,path))

def jsonFatal(msg,path):
	fatal(jsonMsg(msg,path))

def jsonWrongType(expected,got,path):
	jsonError(f"expected type : {expected}, got {got}",path)

def jsonUseDefault(defaultValue,path):
	jsonInfo(f"Correcting to default value ({defaultValue})",path)

def jsonErrorSystem(errorMsg,path):
	cutils.error(f"in ({path}) at [{errorMsg.lineno},{errorMsg.colno}] : {errorMsg.msg}","JSON_DECODER")
