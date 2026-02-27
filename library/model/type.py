class Model:
	def __init__(self) -> None:
		self.name:str
		self.alias:list[str]
		self.filepath:str
		self.isCategory:bool
		self.type_name:str
		self.properties:dict

class FilledModel:
	def __init__(self) -> None:
		self.model:Model
		self.count:float
		self.properties:dict
