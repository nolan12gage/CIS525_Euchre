
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
p0 = EuchrePlayer("p0")
p1 = EuchrePlayerAI("p1")
p2 = EuchrePlayerAI("p2")
p3 = EuchrePlayerAI("p3")
table = EuchreTable(p0, p1, p2, p3)

deck.shuffle()
table.dealer.euchreDeal(deck,table)


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
  # Only do the following on a POST request
  if request.method == 'POST':
    # If the form is valid, then create the user in the db
    if validateForm(request.form):
      createUser(request.form)      
      print('hello', file=sys.stderr)
      
  return render_template('loginForm.html')
  
@app.route('/start', methods=['GET', 'POST'])
def start():
  # We need to add a check in here once sessions and MySQL is implemented to make sure that the user is logged
  # in before proceeding. If they are not logged in, then they need to be redirected back to the login page
	message = "start"
	mailTo = '/pick1'
	return render_template('start.html', table=table, mailTo=mailTo, message=message)
  
@app.route('/get', methods=['GET', 'POST'])
def getCard():
	message = ""
	legalArray = [1,0,1,0,1]
	mailTo = "/result2"
	return render_template('getCard.html', table=table, mailTo=mailTo, message=message, legalArray=legalArray)

@app.route('/pick1', methods=['GET', 'POST'])
def orderUpOrPass():
	message = ""
	mailTo = '/result1'
	return render_template('pick1.html', table=table, mailTo=mailTo, message=message)

@app.route('/pick2', methods=['GET', 'POST'])
def chooseOrPass():
	message = ""
	suitTurnedDown = "d"
	mailTo = '/result1'
	return render_template('pick2.html', table=table, mailTo=mailTo, message=message, suitTurnedDown=suitTurnedDown)

@app.route('/result1', methods=['GET', 'POST'])
def displayChoice1():
	request.get_data()
	rawMessage = request.data.decode("utf-8")
	message = "Result 1: You played " + rawMessage[2] + rawMessage[6] + rawMessage[10]
	mailTo = ''
	return render_template('start.html', table=table, mailTo=mailTo, message=message)

@app.route('/result2', methods=['GET', 'POST'])
def displayChoice2():
	request.get_data()
	rawMessage = request.data.decode("utf-8")
	message = "Result 2: You played " + rawMessage[2] + rawMessage[6] + rawMessage[10]
	mailTo = ''
	return render_template('start.html', table=table, mailTo=mailTo, message=message)

@app.route('/deal', methods=['GET', 'POST'])
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
	








	