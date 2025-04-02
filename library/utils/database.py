from library.utils.common import Version, info, warn, error, Version, Source
import library.cmdUtils.cmdUtils as cutils

import os
import json

default_database = { "data" : dict()}
database = default_database

SOURCE = "Database"

def RAW_DATABASE():
	return database

def getDatabase():
	return database["data"]

def getUUIDsList() -> list[str]:
	return list(getDatabase().keys())

UniverseContainer = {
	"MetaData" : {
		"ObjectUUID" : "0",
		"StoredUUID" : [],
		"IsContainer" : True,
		"IsCountUnit" : False,
		"Count" : (1,"unit",None),
		"Type" : "Universe"
	},
	"Qualifier" : {
		'name' : "Omega",
		'version' : Version
	}
}

@Source(SOURCE)
def loadDatabase(path : str):
	global database

	info('Loading database file')

	if not os.path.isfile(path):
		warn("Database not found, creating one at (./database.json)")
		database = default_database
		json.dump(database,open(path,"wt"),indent = "\t",ensure_ascii=False)
	else:
		try :
			database = json.load(open(path))
		except json.JSONDecodeError as errorMsg:
			cutils.error(f"in (path) : {errorMsg.msg}","JSON_DECODER")
			warn("Using default default database")
			database = default_database
	if "0" not in database["data"]:
		database["data"]["0"] = UniverseContainer

	info("Done !")
	
def register(object:dict):
	if "MetaData" in object and "ObjectUUID" in object["MetaData"]:
		getDatabase()[object["MetaData"]["ObjectUUID"]] = object
