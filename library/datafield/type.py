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

CONSTRAINT_COMPARAISON = {
	"<",
	">",
	"==",
	"!=",
	"<=",
	">=",
}

CONSTRAINT_RANGE = {
	"range",
	"set"
}

CONSTRAINT_BINARY = {
	"<" : lambda value,test : value < test,
	">" : lambda value,test : value > test,
	"<=" : lambda value,test : value <= test,
	">=" : lambda value,test : value >= test,
	"==" : lambda value,test : value == test,
	"!=" : lambda value,test : value != test,
	"<" : lambda value,test : value < test,
}

CONSTRAINT_LIST = {
	"range" : lambda value, a,b : value >= a and value <= b,
	"set" : lambda value, *set : value in set 
}

CONSTRAINT_SET = lambda value, *args : value in args

DATAFIELD_CONSTRAINT_PER_TYPE = {
	"int" : CONSTRAINT_COMPARAISON | CONSTRAINT_RANGE,
	"float" : CONSTRAINT_COMPARAISON | CONSTRAINT_RANGE,
	"string" : {"set"}
}
