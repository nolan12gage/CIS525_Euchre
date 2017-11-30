
from Card import Card
import random

class Deck(object):

	def __init__(self):
		self.cards = []
		for value in ["02","03","04","05","06","07","08","09","10","11","12","13","01"]:
			for suit in ["s","h","d","c"]:
				newcard = Card(value,suit)
				self.cards.append(newcard)
				
	def shuffle(self):
		for i in range(0,100):
			index1 = random.randint(0,len(self.cards)-1)
			index2 = random.randint(0,len(self.cards)-1)
			
			temp = self.cards[index1]
			self.cards[index1] = self.cards[index2]
			self.cards[index2] = temp
			
	def printDeck(self):
		for card in self.cards:
			print(card)


if __name__ == "__main__":
	deck = Deck()
	deck.shuffle()
	#for card in deck.cards:
	#	print(card)
	deck.printDeck()
		
	
	
