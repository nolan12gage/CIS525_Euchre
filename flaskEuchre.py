
from EuchreDeck import EuchreDeck
from EuchrePlayer import EuchrePlayer
from EuchrePlayerAI import EuchrePlayerAI
from EuchrePlayerWeb import EuchrePlayerWeb
from EuchrePlayerWebAI import EuchrePlayerWebAI
from EuchreTable import EuchreTable
from database import *

from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os, re, sys
import mysql.connector
 
app = Flask(__name__)

deck = EuchreDeck()
p0 = EuchrePlayerWeb("CoolName")
p1 = EuchrePlayerWebAI("Adam")
p2 = EuchrePlayerWebAI("Becky")
p3 = EuchrePlayerWebAI("Ethan")
table = EuchreTable(p0, p1, p2, p3)

gameReturnPoint = '/'

@app.route('/about')
def about():
	print(gameReturnPoint)
	return render_template('about.html', gameReturnPoint=gameReturnPoint)  

@app.route('/rules')
def rules():
	return render_template('rules.html', gameReturnPoint=gameReturnPoint)

# @app.route('/score')
# def highScores():
# 	return render_template('score.html', gameReturnPoint=gameReturnPoint)
  
@app.route('/leaderboard')
def leaderBoard():
	leaders = getLeaders()
	print(len(leaders))
	return render_template('leaderboard.html', leaders=leaders, gameReturnPoint=gameReturnPoint)
  
  
@app.route('/join', methods=['GET', 'POST'])
def createAccount():  
	idErr = pwErr = confErr = emailErr = locErr = ageErr = ''
	if request.method == 'POST':
			idErr = validateID(request.form['userID'])
			pwErr = validatePassword(request.form['password'])
			confErr = validateConf(request.form['password'], request.form['confirmPassword'])
			emailErr = validateEmail(request.form['email'])
			locErr = validateLocation(request.form['country'])
			ageErr = validateAge(request.form['age'])
			if not idErr and not pwErr and not confErr and not emailErr and not locErr and not ageErr:
				createUser(request.form)
				return redirect(url_for('.login'))
			else: 
				userID = password = confPass = email = location = age = ''
				if not idErr:
					userID = request.form['userID']
				if not pwErr and not confErr:
					password = request.form['password']
					confPass = request.form['confirmPassword']
				if not emailErr:
					email = request.form['email']
				if not locErr:
					location = request.form['country']
				if not ageErr:
					age = request.form['age']
				return render_template('createAccount.html', idErr=idErr, pwErr=pwErr, confErr=confErr, emailErr=emailErr, 
															 locErr=locErr, ageErr=ageErr, gameReturnPoint=gameReturnPoint, userID=userID,
															 password=password, confPass=confPass, email=email, location=location, age=age)
	return render_template('createAccount.html', idErr=idErr, pwErr=pwErr, confErr=confErr, emailErr=emailErr, locErr=locErr, ageErr=ageErr, gameReturnPoint=gameReturnPoint)
  
@app.route('/login', methods=['GET', 'POST'])
def login():
	loginErr = idErr = pwErr = ''
	if request.method == 'POST':
		loginErr = verifyCredentials(request.form)
		if not loginErr:
			session['username'] = request.form['userID']
			updateLastLogin(session['username'])
			return redirect(url_for('start'))
		else:
			return render_template('loginForm.html', loginErr=loginErr, gameReturnPoint=gameReturnPoint, userID=request.form['userID'])
	return render_template('loginForm.html', loginErr=loginErr, gameReturnPoint=gameReturnPoint)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
	session.pop('username', None)
	return redirect(url_for('start'))

@app.route('/', methods=['GET', 'POST'])
def start():
	global gameReturnPoint
	gameReturnPoint = '/'
	if 'username' in session:
		table.seats[0].name = session['username']
		table.fullReset(deck)
		showTable = True
		return render_template('start.html',table=table, showTable=showTable, session=session) #posts an 'r' to orderUpOrPass()
	else:
		showTable = False
		return render_template('start.html',table=table, showTable=showTable, session=session)

@app.route('/pick1', methods=['GET', 'POST'])
def orderUpOrPass():
	global gameReturnPoint
	gameReturnPoint = '/pick1'
	showTable = True;	
	request.get_data()
	rawMessage = request.data.decode("utf-8")
	if not rawMessage: #this branch is reached when a deal is passed
		action = 'z'
	else:
		action = rawMessage[2]
		print('orderUpOrPass action: ' + action)

	if action == 'z':
		table.dealer = table.getNextPlayer(table.dealer)
		table.leader = table.getNextPlayer(table.dealer)
		table.reset(deck)
		deck.shuffle()
		table.dealer.euchreDeal(deck,table)
		table.printTable()
		print('dealer: ' + table.dealer.name)
		print('leader: ' + table.leader.name)
	if action == 'r':
		table.dealer = table.seats[0]
		table.leader = table.seats[1]
		table.fullReset(deck)
		deck.shuffle()
		table.dealer.euchreDeal(deck,table)
		table.printTable()
		print('dealer: ' + table.dealer.name)
		print('leader: ' + table.leader.name)
	
	if table.leader != table.seats[0]:
		for i in range(table.seats.index(table.leader),4):
			if not table.trump and not table.seats[i].pick1done:
				table.seats[i].orderUpOrPass(table)
				if table.trump and table.dealer == table.seats[0]:
					table.dealer.pickUpTrump(table)
					return redirect(url_for('discardExtra'))
				elif table.trump:
					table.dealer.pickUpTrump(table)
					return redirect(url_for('getCard'))
	if not table.trump and not table.seats[0].pick1done:
		if action != 'o' and action != 'p':
			return render_template('pick1.html', table=table, showTable=showTable)
		else:
			table.seats[0].orderUpOrPass(table, action)
			if table.trump and table.dealer == table.seats[0]:
				table.dealer.pickUpTrump(table)
				return redirect(url_for('discardExtra'))
			elif table.trump:
				table.dealer.pickUpTrump(table)
				return redirect(url_for('goAloneOrNot'))
	leaderIndex = table.seats.index(table.leader)
	if leaderIndex == 0: leaderIndex = 4
	for i in range(1,leaderIndex):
		if not table.trump and not table.seats[i].pick1done:
			table.seats[i].orderUpOrPass(table)
			if table.trump and table.dealer == table.seats[0]:
				table.dealer.pickUpTrump(table)
				return redirect(url_for('discardExtra'))
			elif table.trump:
				table.dealer.pickUpTrump(table)
				return redirect(url_for('getCard'))
	if not table.trump: 
		return redirect(url_for('chooseOrPass'))

@app.route('/discard', methods=['GET', 'POST'])
def discardExtra():
	global gameReturnPoint
	gameReturnPoint = '/discard'
	showTable = True
	request.get_data()
	rawMessage = request.data.decode("utf-8")
	if not rawMessage or rawMessage == '':
		return render_template('discard.html', table=table, showTable=showTable)
	else:
		cardIndexStr = rawMessage[2]
		table.seats[0].discardSixthCard(table, int(cardIndexStr))
	
	if table.seats[0].calledTrump: 
		return redirect(url_for('goAloneOrNot'))
	else: 
		return redirect(url_for('getCard'))

@app.route('/pick2', methods=['GET', 'POST'])
def chooseOrPass():
	global gameReturnPoint
	gameReturnPoint = '/pick2'
	showTable = True
	if(table.zones[4]): table.zones[5].append(table.zones[4].pop())
	table.printTable()
	if table.leader != table.seats[0]:
		for i in range(table.seats.index(table.leader),4):
			if not table.trump and not table.seats[i].pick2done:
				table.seats[i].pickSuitOrPass(table)
				if table.trump:
					return redirect(url_for('getCard'))
	if not table.trump and not table.seats[0].pick2done:
		request.get_data()
		rawMessage = request.data.decode("utf-8")
		print('rawMessage: ' + rawMessage)
		if not rawMessage or rawMessage == '':
			suitTurnedDown = table.zones[5][0].suit
			return render_template('pick2.html', table=table, suitTurnedDown=suitTurnedDown, showTable=showTable)
		else:
			action = rawMessage[2]
			table.seats[0].pickSuit(table, action)
			if table.trump:
				return redirect(url_for('goAloneOrNot'))
	leaderIndex = table.seats.index(table.leader)
	if leaderIndex == 0: leaderIndex = 4
	for i in range(1,leaderIndex):
		if not table.trump and not table.seats[i].pick2done:
			table.seats[i].pickSuitOrPass(table)
			if table.trump:
				return redirect(url_for('getCard'))
	if not table.trump: 
		print("passing deal")
		return redirect(url_for('orderUpOrPass'))

@app.route('/alone', methods=['GET', 'POST'])
def goAloneOrNot():
	global gameReturnPoint
	gameReturnPoint = '/alone'
	showTable = True
	request.get_data()
	rawMessage = request.data.decode("utf-8")
	if not rawMessage or rawMessage == '':
		return render_template('alone.html', table=table, showTable=showTable)
	else:
		action = rawMessage[2]
		if action == 'g':
			table.seats[0].goingAlone = True
			print("player p0 is going alone")
			table.seats[2].sittingOut = True
	return redirect(url_for('getCard'))

@app.route('/get', methods=['GET', 'POST'])
def getCard():
	global gameReturnPoint
	gameReturnPoint = '/get'
	showTable = True
	if table.leader != table.seats[0]:
		for i in range(table.seats.index(table.leader),4):
			if not table.zones[i] and not table.seats[(i+2)%4].goingAlone:
				table.seats[i].playCard(table)
	if not table.zones[0] and not table.seats[2].goingAlone:
		request.get_data()
		rawMessage = request.data.decode("utf-8")
		if not rawMessage or rawMessage == '':
			legalArray = table.seats[0].getLegalPlays(table)
			return render_template('getCard.html', table=table, legalArray=legalArray, showTable=showTable)
		else:
			cardIndexStr = rawMessage[2]
			table.seats[0].playCard(table, int(cardIndexStr))
	leaderIndex = table.seats.index(table.leader)
	if leaderIndex == 0: leaderIndex = 4
	for i in range(1, leaderIndex):
		if not table.zones[i] and not table.seats[(i+2)%4].goingAlone:
			table.seats[i].playCard(table)
	table.leader = table.getTrickWinner()
	if table.getTrickCount() < 5: 
		return redirect(url_for('getCard'))
	else:
		return endOfRound()

def endOfRound():
  showTable = True
  table.assignPoints()
  if table.seats[0].points < 5 and table.seats[1].points < 5:
    return render_template('endRound.html', table=table, showTable=showTable)
  else:
    if table.seats[0].points >= 5:
     addWin(session['username'])
    return render_template('endGame.html', table=table, showTable=showTable)







if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='127.0.0.1', port=5000)
	








	