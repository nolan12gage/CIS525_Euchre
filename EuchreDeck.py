from Card import Card
from Deck import Deck

class EuchreDeck(Deck):

	def __init__(self):
		Deck.__init__(self)
		self.cards = self.cards[28:]
		
if __name__ == "__main__":
	deck = EuchreDeck()
	deck.shuffle()
	#for card in deck.cards:
	#	print(card)
	deck.printDeck()
	