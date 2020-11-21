from spellchecker import SpellChecker

def autocorrect(word):
	spell = SpellChecker()

	# find those words that may be misspelled
	misspelled = spell.unknown(word)


	a=spell.correction(word)
	
	return a

	    # Get a list of `likely` options
	   # print(spell.candidates(word))


autocorrect("pythin")