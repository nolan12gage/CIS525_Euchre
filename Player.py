
from Card import Card
from Deck import Deck
from EuchreDeck import EuchreDeck

class Player(object):

	def __init__(self, name):
		self.name = name
		self.hand = []
		self.handSize = 0
		
	def __str__(self):
		return "Player %s" % (self.name)
		
	def draw(self, deck):
		self.hand.append(deck.cards.pop())
		self.handSize += 1;
		
	def printHand(self):
		print(self.name,": ", end = '')
		if self.hand:
			for card in self.hand[:-1]:
				print(card, ", ",end = '')
			print(self.hand[-1])
		else: 
			print("")
		
	def deal(self, deck, player):
		player.draw(deck)
		
if __name__ == "__main__":
	deck = EuchreDeck()
	deck.shuffle()
	deck.printDeck()
	p1 = Player("Eli")
	p2 = Player("Nat")
	
	p1.draw(deck)
	p1.draw(deck)
	p1.deal(deck, p2)
	p2.printHand()
	p1.printHand()
