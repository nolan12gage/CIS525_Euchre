
from EuchreDeck import EuchreDeck
from EuchrePlayer import EuchrePlayer
from EuchrePlayerAI import EuchrePlayerAI
from EuchreTable import EuchreTable
from database import *

from flask import Flask, flash, redirect, render_template, request, session, abort
import os, re, sys
import mysql.connector
 
app = Flask(__name__)

deck = EuchreDeck()
p1 = EuchrePlayer("p1")
p2 = EuchrePlayerAI("p2")
p3 = EuchrePlayerAI("p3")
p4 = EuchrePlayerAI("p4")
table = EuchreTable(p1, p2, p3, p4)

host = 'localhost'
database = 'euchre_users'
user = 'root'
password = 'mysql'

deck.shuffle()
table.dealer.euchreDeal(deck,table)

p1zoneArray = ""
p2zoneArray = ""
p3zoneArray = ""
p4zoneArray = ""

#table.reset(deck)
#deck.shuffle()
#table.dealer.euchreDeal(deck,table)

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html')  

@app.route('/rules')
def rules():
  return render_template('rules.html')

@app.route('/score')
def highScores():
  return render_template('score.html')
  
@app.route('/join')
def createAccount():  
  return render_template('createAccount.html')
  
@app.route('/login', methods=['GET', 'POST'])
def login():
  # Validate the form if this was a POST request and get rid of the 
  if request.method == 'POST':
    if validateForm(request.form):
      print('hello', file=sys.stderr)
      
  return render_template('loginForm.html')
  
@app.route('/start', methods=['GET', 'POST'])
def start():
  # We need to add a check in here once sessions and MySQL is implemented to make sure that the user is logged
  # in before proceeding. If they are not logged in, then they need to be redirected back to the login page
	message = "start"
	return render_template('start.html', p1=p1, p2=p2, p3=p3, p4=p4, p1zoneArray=p1zoneArray, p2zoneArray=p2zoneArray, p3zoneArray=p3zoneArray, p4zoneArray=p4zoneArray, message=message, table=table)
  
@app.route('/get')
def getCard():
	message = ""
	legalArray = [1,0,1,0,1]
	mailTo = "/result2"
	return render_template('getCard.html', p1=p1, p2=p2, p3=p3, p4=p4, p1zoneArray=p1zoneArray, p2zoneArray=p2zoneArray, p3zoneArray=p3zoneArray, p4zoneArray=p4zoneArray, message=message, table=table, legalArray=legalArray, mailTo=mailTo)

@app.route('/pick1')
def orderUpOrPass():
	message = ""
	return render_template('pick1.html', p1=p1, p2=p2, p3=p3, p4=p4, p1zoneArray=p1zoneArray, p2zoneArray=p2zoneArray, p3zoneArray=p3zoneArray, p4zoneArray=p4zoneArray, message=message, table=table)

@app.route('/pick2')
def chooseOrPass():
	message = ""
	suitTurnedDown = "d"
	return render_template('pick2.html', p1=p1, p2=p2, p3=p3, p4=p4, p1zoneArray=p1zoneArray, p2zoneArray=p2zoneArray, p3zoneArray=p3zoneArray, p4zoneArray=p4zoneArray, message=message, table=table)

@app.route('/result1', methods=['POST'])
def displayChoice1():
	request.get_data()
	rawMessage = request.data.decode("utf-8")
	message = "Result 1: You played " + rawMessage[2] + rawMessage[6] + rawMessage[10]
	return render_template('start.html', p1=p1, p2=p2, p3=p3, p4=p4, p1zoneArray=p1zoneArray, p2zoneArray=p2zoneArray, p3zoneArray=p3zoneArray, p4zoneArray=p4zoneArray, message=message, table=table)

@app.route('/result2', methods=['POST'])
def displayChoice2():
	request.get_data()
	rawMessage = request.data.decode("utf-8")
	message = "Result 2: You played " + rawMessage[2] + rawMessage[6] + rawMessage[10]
	return render_template('start.html', p1=p1, p2=p2, p3=p3, p4=p4, p1zoneArray=p1zoneArray, p2zoneArray=p2zoneArray, p3zoneArray=p3zoneArray, p4zoneArray=p4zoneArray, message=message, table=table)

@app.route('/deal')
def deal():
	# table.assignPoints()
	# table.reset(deck)
	deck.shuffle()

	table.dealer.euchreDeal(deck,table)
	return start() 

@app.route('/detour')
def detour():
	return getCard()


	





if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='127.0.0.1', port=5000)
	








	