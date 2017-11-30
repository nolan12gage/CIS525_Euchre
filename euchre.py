
from EuchreDeck import EuchreDeck
from EuchrePlayer import EuchrePlayer
from EuchrePlayerAI import EuchrePlayerAI
from EuchreTable import EuchreTable

deck = EuchreDeck()
p0 = EuchrePlayerAI("p0")
p1 = EuchrePlayerAI("p1")
p2 = EuchrePlayerAI("p2")
p3 = EuchrePlayerAI("p3")
table = EuchreTable(p0, p1, p2, p3)

while table.seats[0].points < 1 and table.seats[1].points < 1:
	deck.shuffle()
	table.dealer.euchreDeal(deck,table)
	activePlayer = table.leader
	table.printTable()

	for player in table.seats:
		if activePlayer.orderUpOrPass(table): break
		activePlayer = table.getNextPlayer(activePlayer)
		
	if table.trump is None:
		table.zones[5].append(table.zones[4].pop())
		for player in table.seats:
			if activePlayer.pickSuit(table): break
			activePlayer = table.getNextPlayer(activePlayer)
	
	if table.trump is None: 
		print("No trump was selected, deal passes")
	else:
		if table.leader.sittingOut: table.leader = table.getNextPlayer(table.leader)
		handSize = len(table.dealer.hand)
		for i in range(0,handSize):
			table.printTable()
			activePlayer = table.leader
			for player in table.seats:
				if not activePlayer.sittingOut: activePlayer.playCard(table)
				activePlayer = table.getNextPlayer(activePlayer)
			table.leader = table.getTrickWinner()
	
	table.printTable()
	table.assignPoints()
	table.reset(deck)
	table.dealer = table.getNextPlayer(table.dealer)
	table.leader = table.getNextPlayer(table.leader)
	








	