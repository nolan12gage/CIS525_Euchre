
from EuchreDeck import EuchreDeck
from EuchrePlayer import EuchrePlayer
from EuchrePlayerAI import EuchrePlayerAI
from EuchreTable import EuchreTable

#from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import sys
 
app = Flask(__name__)

deck = EuchreDeck()
p1 = EuchrePlayer("p1")
p2 = EuchrePlayerAI("p2")
p3 = EuchrePlayerAI("p3")
p4 = EuchrePlayerAI("p4")
table = EuchreTable(p1, p2, p3, p4)

# print("initial deck length: " + len(deck.cards), file=sys.stderr)

deck.shuffle()
table.dealer.euchreDeal(deck,table)

p1zoneArray = ""
p2zoneArray = ""
p3zoneArray = ""
p4zoneArray = ""


# print(len(deck.cards), file=sys.stderr)

# table.reset(deck)

# print(len(deck.cards), file=sys.stderr)

@app.route('/')
def home():
	message = "home"
	for card in deck.cards:
		print(card, file=sys.stderr)
	return render_template('index.html',table=table, message=message)

@app.route('/get')
def getCard():
	message = ""
	legalArray = [1,0,1,0,1]
	mailTo = "/result2"
	return render_template('getCard.html',**locals(), **globals())

@app.route('/pick1')
def orderUpOrPass():
	message = ""
	return render_template('pick1.html',**locals(), **globals())

@app.route('/pick2')
def chooseOrPass():
	message = ""
	suitTurnedDown = "d"
	return render_template('pick2.html',**locals(), **globals())

@app.route('/result1', methods=['POST'])
def displayChoice1():
	request.get_data()
	rawMessage = request.data.decode("utf-8")
	message = "Result 1: You played " + rawMessage[2] + rawMessage[6] + rawMessage[10]
	return render_template('index.html',**locals(), **globals())

@app.route('/result2', methods=['POST'])
def displayChoice2():
	request.get_data()
	rawMessage = request.data.decode("utf-8")
	message = "Result 2: You played " + rawMessage[2] + rawMessage[6] + rawMessage[10]
	return render_template('index.html',**locals(), **globals())  

@app.route('/deal')
def deal():
	# table.assignPoints()

	table.reset(deck)
	deck.shuffle()
	table.dealer.euchreDeal(deck,table)
	return home() 

@app.route('/detour')
def detour():
	return getCard( )


	





if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    # app.run(debug=True,host='0.0.0.0', port=4000)
    app.run(debug=True,host='127.0.0.1', port=5000)
	








	