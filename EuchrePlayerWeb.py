
from Card import Card
from Deck import Deck
from EuchrePlayer import EuchrePlayer
from Player import Player
from Table import Table

class EuchrePlayerWeb(EuchrePlayer):

	def __init__(self, name):
		EuchrePlayer.__init__(self,name)
		
	def orderUpOrPass(self, table, action):
		self.pick1done = True
		if action == 'o':
			print("%s ordered up the %s" % (self.__str__(), table.zones[4][0].__str__()))
			self.calledTrump = True
			table.trump = table.zones[4][0].getSuit()
		else:
			print(self.name + " passed")
			
	def pickUpTrump(self, table):
		self.hand.append(table.zones[4].pop())
		self.handSize += 1
		print("hand after picking up:")
		self.printHand()
		
	def pickSuit(self, table, suit):
		self.pick2done = True
		if suit == 's' or suit == 'h' or suit == 'd' or suit == 'c':
			print("%s called %s to be trump" % (self.__str__(), suit))
			self.calledTrump = True
			table.trump = suit
		else:
			print(self.name + " passed again")

	def getLegalPlays(self, table):
		if table.firstPlayOfTrick(): 
			legalArray = []
			for i in range(0,self.handSize):
					legalArray.append(1)
		else:
			suitInHand = False
			ledSuit = table.zones[table.seats.index(table.leader)][0].suit
			legalArray = []
			if table.zones[table.seats.index(table.leader)][0] == table.getLeft(): ledSuit = table.trump
			for card in self.hand: ### first condition doesn't handle bauers correctly
				if (card != table.getLeft() and card.suit == ledSuit) or (ledSuit == table.trump and card == table.getLeft()): 
					suitInHand = True
					legalArray.append(1)
				else:
					legalArray.append(0)
			if not suitInHand:
				for i in range(0,self.handSize):
					legalArray[i] = 1
		return legalArray
		
	def playCard(self,table, cardIndex):
		self.handSize -= 1
		table.zones[table.seats.index(self)].append(self.hand.pop(cardIndex))
		print(self.name + " played: " + table.zones[table.seats.index(self)][0].__str__())

	def discardSixthCard(self, table, cardIndex):
		print(self.name + " discarded: " + self.hand[cardIndex].__str__())
		self.handSize -= 1
		table.zones[5].append(self.hand.pop(cardIndex))
		
			
			
			
			
			
			