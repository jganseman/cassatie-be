# function taking a regex match and printing it out to use for spaCy training
# format: (u"Uber blew through $1 million a week", {"entities": [(0, 4, "ORG")]}),
def printmatch(mymatch, entityname):
	
	# create match tuple
	matchdef = ( str(mymatch.start()) , str(mymatch.end()), entityname )
	
	# put it into an entity json array
	myent = {'entities': [ matchdef ]}	
	
	# combine with source string into a tuple
	# do not strip() the string here, as that will screw up matched start and end positions
	mytuple = (mymatch.string, myent)  
	
	# print to command line
	print(mytuple, ',', sep='')

	# todo UTF encoding seems OK in Python3 (not Python2), but u"" signifier is not printed.
	# for the moment, considering that harmless
