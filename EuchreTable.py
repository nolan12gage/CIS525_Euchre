
from EuchrePlayer import EuchrePlayer
from Player import Player
from Table import Table
from EuchreDeck import EuchreDeck
from Card import Card

class EuchreTable(Table):

	def __init__(self, player1, player2, player3, player4):
		Table.__init__(self)
		self.seats.append(player1)
		self.seats.append(player2)
		self.seats.append(player3)
		self.seats.append(player4)
		
		for i in range(0,6):
			self.zones.append([])
			
		self.trump = None
		self.dealer = self.seats[0] #random.randint(0,3)
		self.leader = self.seats[1] #right of randomly selected dealer
			
		
	def firstPlayOfTrick(self):
		if self.zones[0] or self.zones[1] or self.zones[2] or self.zones[3]: 
			return False
		else: 
			return True
			
	def getNextPlayer(self, currentPlayer):
		return self.seats[(self.seats.index(currentPlayer)+1)%4]
		
	def getTrickWinner(self):
		ledCard = self.zones[self.seats.index(self.leader)][0]
		print("led card: " + ledCard.__str__())
		ledCardSuit = ledCard.suit
		if ledCard == self.getLeft(): ledCardSuit = self.trump
		winningCard = ledCard
		winningValue = 0
		playedCardArray = []
		for i in range(0,4):
			playedCardArray.append(self.zones[(self.seats.index(self.leader)+i)%4][0])
		for card in playedCardArray:
			adjSuit = card.suit
			if card == self.getLeft(): adjSuit = self.trump
		
			if adjSuit == ledCardSuit: adjValue = card.getIntValue()
			if adjSuit == self.trump: adjValue = card.getIntValue() + 13
			if card == self.getRight(): adjValue = 29
			if card == self.getLeft(): adjValue = 28
			if adjSuit not in [self.trump, ledCardSuit]: adjValue = 0
			
			# print("%s: adjValue: %s adjSuit: %s" % (card.__str__(), adjValue, adjSuit))
				
			if adjValue > winningValue:
				winningCard = card
				winningValue = adjValue
		#winner = self.seats[(self.seats.index(self.leader) + self.zones[0].index(winningCard))%4]
		
		winner = self.seats[0];
		i = 0
		while self.zones[i][0] != winningCard:
			winner = self.getNextPlayer(winner)
			if winner.sittingOut: 
				winner = self.getNextPlayer(winner)
				i += 1
			i += 1
			
		
		winner.tricksWon += 1
		
		print("%s won with the %s" % (winner.__str__(), winningCard.__str__()))
		# print("self.seats.index(self.leader): " + str(self.seats.index(self.leader)))
		# print("self.zones[0].index(winningCard): " + str(self.zones[0].index(winningCard)))
		# print(winner.__str__())
		
		# while self.zones[0]:
		# 	self.zones[1].append(self.zones[0].pop())

		for i in range(0,4):
			self.zones[5].append(self.zones[i].pop())
		
		return winner
		
	def getLeft(self):
		if self.trump == "s": return Card("11","c")
		if self.trump == "h": return Card("11","d")
		if self.trump == "d": return Card("11","h")
		if self.trump == "c": return Card("11","s")
		
	def getRight(self):
		if self.trump == "s": return Card("11","s")
		if self.trump == "h": return Card("11","h")
		if self.trump == "d": return Card("11","d")
		if self.trump == "c": return Card("11","c")
		
	def assignPoints(self):
		teamAtricksWon = self.seats[0].tricksWon + self.seats[2].tricksWon
		teamBtricksWon = self.seats[1].tricksWon + self.seats[3].tricksWon
		teamAcalledTrump = self.seats[0].calledTrump or self.seats[2].calledTrump
		teamBcalledTrump = self.seats[1].calledTrump or self.seats[3].calledTrump
		teamAwentAlone = self.seats[0].goingAlone or self.seats[2].goingAlone
		teamBwentAlone = self.seats[1].goingAlone or self.seats[3].goingAlone
		
		if teamAtricksWon == 5 and teamAwentAlone:
			self.seats[0].points += 4
			self.seats[2].points += 4
		elif teamBtricksWon == 5 and teamBwentAlone:
			self.seats[1].points += 4
			self.seats[3].points += 4	
		elif teamAtricksWon == 5 or teamAtricksWon >= 3 and teamBcalledTrump: 
			self.seats[0].points += 2
			self.seats[2].points += 2
		elif teamBtricksWon == 5 or teamBtricksWon >= 3 and teamAcalledTrump: 
			self.seats[1].points += 2
			self.seats[3].points += 2
		elif teamAtricksWon >= 3:
			self.seats[0].points += 1
			self.seats[2].points += 1
		elif teamBtricksWon >= 3:
			self.seats[1].points += 1
			self.seats[3].points += 1
			
		if self.seats[0].calledTrump or self.seats[2].calledTrump: print("teamA called trump")
		if self.seats[1].calledTrump or self.seats[3].calledTrump: print("teamB called trump") 
		print("teamAtricksWon: " + str(teamAtricksWon))
		print("teamBtricksWon: " + str(teamBtricksWon))
		print("teamApoints: " + str(self.seats[0].points))
		print("teamBpoints: " + str(self.seats[1].points))
			
	def reset(self, deck):
		for player in self.seats:
			player.calledTrump = False
			player.goingAlone = False
			player.sittingOut = False
			player.tricksWon = 0
			while player.hand:
				deck.cards.append(player.hand.pop())
		# while self.zones[1]:
		# 	deck.cards.append(self.zones[1].pop())
		# while self.zones[4]:
		# 	deck.cards.append(self.zones[4].pop())
		
		# for zone in self.zones:
			# while len(zone) > 0:
				# deck.cards.append(zone.pop)
		
		for i in range(0,len(self.zones)):
			while self.zones[i]:
				deck.cards.append(self.zones[i].pop())
		
		
		self.trump = None
		
		
		
if __name__ == "__main__":

	deck = EuchreDeck()
	#deck.shuffle()
	deck.printDeck()
	p1 = EuchrePlayer("p1")
	p2 = EuchrePlayer("p2")
	p3 = EuchrePlayer("p3")
	p4 = EuchrePlayer("p4")
	
	table = EuchreTable(p1, p2, p3, p4)
	
	p1.euchreDeal(deck,table)
	table.printTable()
	
		