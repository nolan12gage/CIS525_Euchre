
from Card import Card
from Deck import Deck
from Player import Player
from Table import Table

class EuchrePlayer(Player):

	def __init__(self, name):
		Player.__init__(self,name)
		self.tricksWon = 0
		self.points = 0
		self.calledTrump = False
		self.goingAlone = False
		self.sittingOut = False

		self.pick1done = False
		self.pick2done = False
				
	def euchreDeal(self, deck, table):
		dealerIndex = table.seats.index(self)
		for i in range(1,2*len(table.seats)+1):
			target = (dealerIndex + i)%len(table.seats)
			if (i <= 4 and i%2 == 1) or (i > 4 and i%2 == 0): 
				for i in range(0,2): table.seats[target].draw(deck)
			else: 
				for i in range(0,3): table.seats[target].draw(deck)
		# for i in range(0,4):
		# 	table.zones[4].append(deck.cards.pop(0))
		table.zones[4].append(deck.cards.pop(0)) #deck should still have 3 cards
			
	def orderUpOrPass(self, table):
		self.pick1done = True
		orderUp = input("%s: Do you want %s to be trump?" % (self.__str__(), table.zones[4][0].__str__()))
		if orderUp == "yes": 
			table.trump = table.zones[4][0].getSuit()
			self.calledTrump = True
			table.dealer.pickUpTrump(table)
			goAlone = input("%s: Do you want to go alone?" % (self.__str__()))
			if goAlone == "yes": 
				self.goingAlone = True
				table.seats[(table.seats.index(self)+2)%4].sittingOut = True
				print("%s is sitting out" % table.seats[(table.seats.index(self)+2)%4].__str__())
			return True
		else: return False
		
	def pickUpTrump(self, table):
		self.hand.append(table.zones[4].pop())
		display = table.dealer.name + ": Pick the index of a card to discard: "
		index = int(input(display))
		# table.zones[4].append(self.hand.pop(index))
		table.zones[5].append(self.hand.pop(index))
		
	def pickSuit(self,table):
		display = self.name + ": Pick a suit to be trump (besides " + table.zones[5][0].getSuit() + "): " ##what zone??
		choice = input(display)
		while choice == table.zones[5][0].getSuit() or choice not in ["s", "h", "d", "c", "pass"]:
			choice = input("please pick a valid suit: ")
		if choice != "pass": 
			table.trump = choice
			self.calledTrump = True
			goAlone = input("%s: Do you want to go alone?" % (self.__str__()))
			if goAlone == "yes": 
				self.goingAlone = True
				table.seats[(table.seats.index(self)+2)%4].sittingOut = True
				print("%s is sitting out" % table.seats[(table.seats.index(self)+2)%4].__str__())
			return True
		else: return False
		
	def playCard(self,table):
		if table.firstPlayOfTrick(): 
			while True:
				display = self.name + " select index of card to lead: "
				cardIndex = int(input(display))
				if cardIndex > len(self.hand)-1 or cardIndex < 0:
					print("index out of range")
					continue
				break
			# table.zones[0].append(self.hand.pop(cardIndex))
			table.zones[table.seats.index(self)].append(self.hand.pop(cardIndex))
			self.handSize -= 1;
			# print(self.name + " led: " + table.zones[0][-1].__str__())
			print(self.name + " led: " + table.zones[table.seats.index(self)][0].__str__())
		else:
			suitInHand = False
			ledSuit = table.zones[table.seats.index(table.leader)][0].suit
			# print("ledSuit: %s" % ledSuit)
			# if table.zones[0][0] == table.getLeft(): ledSuit = table.trump
			if table.zones[table.seats.index(table.leader)][0] == table.getLeft(): ledSuit = table.trump
			for card in self.hand: 
				if (card != table.getLeft() and card.suit == ledSuit) or (ledSuit == table.trump and card == table.getLeft()): suitInHand = True
			while True:
				display = self.name + "select index of card to follow with: "
				cardIndex = int(input(display))
				if cardIndex > len(self.hand)-1 or cardIndex < 0:
					print("index out of range")
					continue
				adjSuit = self.hand[cardIndex].suit
				if self.hand[cardIndex] == table.getLeft(): adjSuit = table.trump
				if suitInHand and (adjSuit != ledSuit):
					print("please follow suit")
					continue
				break
			# table.zones[0].append(self.hand.pop(cardIndex))
			table.zones[table.seats.index(self)].append(self.hand.pop(cardIndex))
			self.handSize -= 1;
			print(self.name + " played: " + table.zones[table.seats.index(self)][0].__str__())
				
		
	
if __name__ == "__main__":
	
	deck = Deck()
	player = EuchrePlayer("p1")
	player.draw(deck)
	player.printHand()