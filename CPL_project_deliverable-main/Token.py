#token class to 
tokenList = {
	"keywords" : {
		'import' : 1,
		'implementations' : 2,
		'function': 3,
		'exit' : 4,
		'is' : 5,
		'variables' : 6,
		'define' : 7,
		'of' : 8,
		'type' : 9,
		'double' : 10,
		'begin' : 11,
		'input' : 12,
		'display' : 13,
		'set' : 14,
		'endfun' : 15

	},
	"identifiers": {
		'h' : 100,
		'b' : 101,
		'area' : 102
	},
	"operators" : {
		'+' : 200,
		'-' : 201,
		'*' : 202,
		'/' : 203,
		'=' : 204

	},
	"specialSymbols" : {
		',' : 300,
		'.' : 301
	},
	"literals" : {
		'str' : 600,
		'int' : 601,
		'float' : 602

	}

}


class Token:
	def __init__(self, type, id, value):
		self.type = type
		self.id = id
		self.value = value


	def getTokenData(self):
		return [self.type, self.id, self.value]


