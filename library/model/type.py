class Model:
	def __init__(self) -> None:
		self.name:str = ""
		self.alias:list[str] = []
		self.filepath:str = ""
		self.isCategory:bool = False
		self.type_name:str = "Basic"
		self.parent:list[str] = []
		self.properties:dict = {}

class FilledModel:
	def __init__(self) -> None:
		self.model:Model = Model()
		self.count:float = 0
		self.properties:dict = dict()

class Universe(Model):
	def __init__(self) -> None:
		self.name = "Universe"
		self.alias = ["Omega"]
		self.filepath = ""
		self.isCategory = False
		self.type_name = "Storage"
		self.parent = []
		self.properties = {}

class Faulty(Model):
	def __init__(self) -> None:
		self.name = "FAULTY"
		self.target_model:str = ""
		self.alias = []
		self.target_path = ""
		self.isCategory = False
		self.type_name = "Storage"
		self.parent = []
		self.properties = {}
		self.error = []
