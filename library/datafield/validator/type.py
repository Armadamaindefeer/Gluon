DATAFIELD_TYPE = {
	"string" : str,
	"bool" : bool,
	"int" : int,
	"float" : float,
	"comment" : str
}

KEY_BASE = {
	"type",
	"allowNone",
	"default",
	"selectValue",
	"constraint"
}

DATAFIELD_KEY = {
	"string" : KEY_BASE,
	"bool" : KEY_BASE,
	"int" : KEY_BASE,
	"float" : KEY_BASE,
	"comment" : {"type","value"}
}

DATAFIELD_KEY_TYPE = {
	"type" : str,
	"allowNone" : bool,
	"default" : object,
	"selectValue" : list,
	"constraint" : dict
}

CONSTRAINT_BINARY = {
	"<" : lambda value,test : value < test,
	">" : lambda value,test : value > test,
	"<=" : lambda value,test : value <= test,
	">=" : lambda value,test : value >= test,
	"==" : lambda value,test : value == test,
	"!=" : lambda value,test : value != test
}

CONSTRAINT_SET = {
	"set" : lambda value, *set : value in set,
	"nset" : lambda value, *set : value not in set
}

CONSTRAINT_RANGE = {
	"range" : lambda value, a,b : value >= a and value <= b,
	"nrange" : lambda value, a,b : not (value >= a and value <= b)
}

DATAFIELD_CONSTRAINT_PER_TYPE = {
	"int" : CONSTRAINT_BINARY.keys() | CONSTRAINT_RANGE.keys() | CONSTRAINT_SET.keys(),
	"float" : CONSTRAINT_BINARY.keys() | CONSTRAINT_RANGE.keys() | CONSTRAINT_SET.keys(),
	"string" : CONSTRAINT_SET.keys()
}
