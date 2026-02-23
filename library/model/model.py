class MetaDataConstructor:
	...

class Model:
	def __init__(self) -> None:
		self.name:str
		self.alias:str
		self.filepath:str
		#self.metadata:dict[str,MetaDataConstructor]
		self.properties:list[dict]
