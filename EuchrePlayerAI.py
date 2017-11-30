
from Card import Card
from Deck import Deck
from EuchrePlayer import EuchrePlayer
from Player import Player
from Table import Table

class EuchrePlayerAI(EuchrePlayer):

	def __init__(self, name):
		EuchrePlayer.__init__(self,name)
		
	def orderUpOrPass(self, table):
		numberOfPotentialTrump = 0
		for card in self.hand:
			if card.getSuit() == table.zones[4][0].getSuit(): numberOfPotentialTrump += 1 #add left logic
		if table.dealer == self: numberOfPotentialTrump += 1
		if numberOfPotentialTrump >= 3: orderUp = "yes"
		else: orderUp = "no"

		if orderUp == "yes": 
			print("%s ordered up the %s" % (self.__str__(), table.zones[4][0].__str__()))
			self.calledTrump = True
			table.trump = table.zones[4][0].getSuit()
			table.dealer.pickUpTrump(table)
			trumpCount = 0
			for card in self.hand:
				if card.getSuit() == table.trump: trumpCount += 1
			if trumpCount == 5 or trumpCount == 4 and table.getRight() in self.hand or trumpCount == 3 and table.getLeft() in self.hand:
				print(self.__str__() + " going alone")
				self.goingAlone = True
				table.seats[(table.seats.index(self)+2)%4].sittingOut = True
				print("%s is sitting out" % table.seats[(table.seats.index(self)+2)%4].__str__())
			return True
		else: 
			print(self.name + " passed")
			return False
			
	def pickUpTrump(self, table):
		self.hand.append(table.zones[4].pop())
		index = 0
		table.zones[5].append(self.hand.pop(index))
		
	def pickSuit(self,table):
		suitCount = {"s": 0, "h": 0, "d": 0, "c": 0}
		choice = "pass"
		for card in self.hand:
			suitCount[card.getSuit()] += 1 #add left logic
		for key in suitCount:
			if suitCount[key] >= 3 and key != table.zones[5][0].getSuit(): choice = key
		if choice != "pass": 
			print("%s called %s to be trump" % (self.__str__(), choice))
			self.calledTrump = True
			table.trump = choice
			trumpCount = 0
			for card in self.hand:
				if card.getSuit() == table.trump: trumpCount += 1
			if trumpCount == 5 or trumpCount == 4 and table.getRight() in self.hand or trumpCount == 3 and table.getLeft() in self.hand:
				print(self.__str__() + " going alone")
				self.goingAlone = True
				table.seats[(table.seats.index(self)+2)%4].sittingOut = True
				print("%s is sitting out" % table.seats[(table.seats.index(self)+2)%4].__str__())
			return True
		else: 
			print(self.name + " passed again")
			return False
		
	def playCard(self,table):
		if table.firstPlayOfTrick(): 
			cardIndex = 0
			table.zones[table.seats.index(self)].append(self.hand.pop(cardIndex))
			self.handSize -= 1
			print(self.name + " led: " + table.zones[table.seats.index(self)][0].__str__())
		else:
			suitInHand = False
			ledSuit = table.zones[table.seats.index(table.leader)][0].suit
			# print("ledSuit: %s" % ledSuit)
			if table.zones[table.seats.index(table.leader)][0] == table.getLeft(): ledSuit = table.trump
			for card in self.hand: ### first condition doesn't handle bauers correctly
				if (card != table.getLeft() and card.suit == ledSuit) or (ledSuit == table.trump and card == table.getLeft()): suitInHand = True
			cardIndex = 0
			while True:
				
				adjSuit = self.hand[cardIndex].suit ###causes errors when following with right bauer
				if self.hand[cardIndex] == table.getLeft(): adjSuit = table.trump
				#print("cardIndex: %s, adjSuit: %s, ledSuit: %s" % (str(cardIndex), adjSuit, ledSuit))
				if suitInHand and (adjSuit != ledSuit):
					cardIndex += 1
					continue
				break
			table.zones[table.seats.index(self)].append(self.hand.pop(cardIndex))
			self.handSize -= 1
			print(self.name + " played: " + table.zones[table.seats.index(self)][0].__str__())
			
			
			
			
			
			