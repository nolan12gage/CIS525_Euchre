
class Card():

	def __init__(self, value, suit):
		self.value = value
		self.suit = suit
		
	def __str__(self):
		# return "%s of %s" % (self.value, self.suit)
		return "%s%s" % (self.suit, self.value)
		
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.value == other.value and self.suit == other.suit
		return False
		
	def __ne__(self, other):
		return not self.__eq__(other)
		
	def getValue(self):
		return self.value
		
	def getSuit(self):
		return self.suit
		
	def getIntValue(self):
		result = int(self.value)
		if result == 1: result = 14
		return result
		
		
if __name__ == "__main__":
	newcard = Card("Ace","Hearts")
	print(newcard)