
from Card import Card
from Player import Player

class Table(object):
	
	def __init__(self):
		self.zones = []
		self.seats = []
		
	def printZone(self, index):
	
		print("z",index," : ", sep = '', end = '')
		for card in self.zones[index][:-1]:
			print(card, ", ",end = '')
		print(self.zones[index][-1])
		
	def printTable(self):
		for player in self.seats:
			player.printHand()
		for i in range(0,len(self.zones)):
			if self.zones[i]: self.printZone(i)
		
		