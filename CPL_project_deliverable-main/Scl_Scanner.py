from Token import *
import sys
import json



def filter_File(path):

	try:
		srcFile = open(path, 'r')
	except:
		sys.exit("The file does not exist.")

	
	lineList = []
	blockComment = False

	for line in srcFile:
		
		lineTokens = []
		#removes new lines and tabs special characters
		line = ' '.join(line.split())
		
		#skip empty lines
		if line == '':
			continue

		#constants for block comments
		C_START = "/*"
		C_END = "*/"

		#if the beginning  character for a comment block exists set the bool to true
		if C_START in line:
			blockComment = True

		
		#if you hit the end of the block comment continue to the next line 
		if C_END in line:
			blockComment = False
			continue

		if not blockComment:
			lineList.append(lineTokens)

		#filter line comments
		line = line.split('//',1)[0].strip()
		if not line:
			continue
		#if you aren't in a block comment filter the line 
		if not blockComment:
			#filter "" literals 
			if '"' in line:
				#split the line at the first instance of "
				splitLoc = line.find('"')

				firstHalf = line[:splitLoc]
				secondHalf = line[splitLoc:]

				#find the next " in the line and split it again
				secondSplitLoc = splitLoc + secondHalf[1:].find('"') + 1
				statement = line[splitLoc:secondSplitLoc + 1]
				secondHalf = line[secondSplitLoc + 1:]

				

				#split the string of tokens on the first half of the statement
				tokens = firstHalf.split(' ' )
				for token in tokens:
					lineTokens.append(token)
				#append the statement literal to the tokens list
				lineTokens.append(statement)

				#if the statement has more tokens, add them to the list
				if secondHalf  != '\n':
					secondHalfTokens = secondHalf.split(' ')
					for token in secondHalfTokens:
						lineTokens.append(token)
				#remove any null indices in the lineTokens list
				lineTokens = list(filter(None, lineTokens))
				continue
		
			lineTokens = line.split(" ")
			lineList.append(lineTokens)
		
	#filter indexes w/ value None in lineList
	lineList = list(filter(None, lineList))

	count = 0
	while count < len(lineList):
		#filter any empty string indexes in each list of tokens in the line list
		lineList[count] = list(filter(None, lineList[count]))
		count += 1
	#return the filtered list of lines from the program
	return lineList

#function to check if a num is a float
def isFloat(num):
	try:
		float(num)
		return True
	except ValueError:
		return False
#converts a given list to a dictionary
def listToDict(ls):
	listIter = iter(ls)
	resultDict = dict(zip(listIter, listIter))

	
	return resultDict


#generate a json file
def generate_Json(classifiedTokens):
	#open a new json file
	jsonFile = open("outTokens.json", "w")

	#create the json dictionary
	jsonDict = {}
	megaDict = {}
	counter = 0

	

	
	counter = 0
	for token in classifiedTokens:

		#get the values for the token
		tokenData = token.getTokenData()
		#update the token w/ a json format
		jsonToken = ['type', tokenData[0], 'id', tokenData[1], 'value', tokenData[2]]

		#convert the  token list to a dictionary
		newTokenDict = listToDict(jsonToken)
		
		#create a token key
		tokenStr = 'Token_id_' + str(counter)
		if tokenStr not in megaDict:
			megaDict[tokenStr] = {}
		
		megaDict[tokenStr].update(newTokenDict)

		counter += 1

	jsonObj = json.dumps(megaDict, indent=4)
	jsonFile.write(jsonObj)




#does look ups on the tokens in each line of the list	
def parse_Lines(lineList):
	classifiedTokens = []

	#classify each token in each token list using the look ups in the Token class
	for tokens in lineList:
		for token in tokens:
			if token in tokenList["keywords"]:
				newToken = Token('keywords', tokenList["keywords"][token], token)
			
			elif token in tokenList["identifiers"]:
				newToken = Token("identifiers", tokenList["identifiers"][token], token)

			elif token in tokenList["operators"]:
				newToken = Token("operators", tokenList["operators"][token], token)

			elif token in tokenList["specialSymbols"]:
				newToken = Token("specialSymbols", tokenList["specialSymbols"][token], token)
			elif '"' in token:
				newToken = Token("literals", tokenList["literals"]["str"], token)
			elif token.isdigit():
				newToken = Token("literals", tokenList["literals"]["int"], token)
			elif isFloat(token):
				newToken = Token("literals", tokenList["literals"]["float"], token)
			else:
				newToken = Token("UKNOWN", 1000, token)

			classifiedTokens.append(newToken)
			print("New token: ", newToken.getTokenData())

	
	return classifiedTokens		
			



		
#main
if __name__ == '__main__':
	#get the cmd line args
	args = sys.argv
	#run the argument through the file filter
	lineList = filter_File(args[1])

	classifiedTokens = parse_Lines(lineList)
	generate_Json(classifiedTokens)
	




	
	
	

