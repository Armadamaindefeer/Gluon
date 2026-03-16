class Model:
	def __init__(self) -> None:
		self.name:str = ""
		self.alias:list[str] = []
		self.filepath:str = ""
		self.isCategory:bool = False
		self.type_name:str = "Basic"
		self.parent:list[str] = []
		self.properties:dict = dict()

class FilledModel:
	def __init__(self) -> None:
		self.model:Model = Model()
		self.count:float = 0
		self.properties:dict = dict()

Universe = Model()
Universe.name = "Universe"

