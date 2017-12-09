from flask import Flask, flash, redirect, render_template, request, session, abort
from validate_email import validate_email
import mysql.connector
import re

host = 'euchre.czwljjbvkc3f.us-east-2.rds.amazonaws.com'
database = 'euchre_users'
user = 'euchre'
password = 'cis525team7'

def validateID(id):
  idErr = ''
  if(len(id) < 1):
    idErr = 'Field is required'
    return idErr
  if(len(id) > 30 or len(id) < 8):
    idErr = 'Must be between 8 and 30 characters'
    return idErr
  if not re.match("^[A-Za-z0-9]*$", id):  
    idErr = 'Only letters and numbers are allowed'
  return idErr

def validatePassword(password):
  pwErr = ''
  if(len(password) < 1):
    pwErr = 'Field is required'
    return pwErr
  if(len(password) > 30 or len(password) < 6):
    pwErr = 'Must be between 6 and 30 characters'
    return pwErr
  if not re.match("^[A-Za-z0-9]*$", password):  
    pwErr = 'Only letters and numbers are allowed'
  return pwErr

def validateConf(password, conf):
  confErr = ''
  if(password != conf):
    confErr = 'Passwords do not match'
  return confErr
  
def validateAge(age):
  ageErr = ''
  if len(age) < 1:
    ageErr = 'Field is required'
    return ageErr
  if not re.match("^[0-9]*$", age) or not age:  
    ageErr = 'Only numbers are allowed'
    return ageErr
  if int(age) > 120 or int(age) < 1:
    ageErr = 'Please enter a number from 1-120'
  return ageErr

def validateEmail(email):
  emailErr = ''
  if(len(email) < 1): 
    emailErr = 'Field is required'
    return emailErr
  if(len(email) > 100):
    emailErr = 'Must be fewer than 100 characters'
    return emailErr
  if(not validate_email(email)):
    emailErr = 'Not a valid email'
  return emailErr

def validateLocation(location):
  locErr = ''
  if(len(location) < 1):
    locErr = 'Field is required'
    return locErr
  return locErr

def getLeaders():
  leaders = []
  conn = mysql.connector.connect(host=host, database=database, user=user, password=password)
  cursor = conn.cursor()
  select_leaders = ("SELECT USER_ID, CAREER_WINS, AGE, LOCATION, LAST_LOGIN FROM USER_INFO ORDER BY CAREER_WINS DESC")
  cursor.execute(select_leaders)
  row = cursor.fetchone()
  rownum = 1
  while row is not None and rownum < 20:
    leaders.append(row)
    row = cursor.fetchone()
    rownum += 1
    
  return leaders
  
def verifyCredentials(form):
  credErr = idErr = pwErr = ''
  idErr = validateID(form['userID'])
  pwErr = validatePassword(form['password'])
  
  # If the id or password don't meet criteria, automatically return an error
  if idErr or pwErr:
    credErr = 'Invalid user name or password'
    return credErr
    
  conn = mysql.connector.connect(host=host, database=database, user=user, password=password)
  cursor = conn.cursor(buffered=True)
  select_query = ("SELECT USER_ID FROM USER_INFO WHERE USER_ID = %s and PASSWORD = %s")
  select_criteria = (form['userID'], form['password'])
  cursor.execute(select_query, select_criteria)
  numRows = cursor.rowcount
  cursor.close()
  conn.close()
  
  if numRows < 1: 
    credErr = 'Invalid user name or password'
    return credErr
  
  return credErr  
	
def updateLastLogin(username):
	conn = mysql.connector.connect(host=host, database=database, user=user, password=password)
	cursor = conn.cursor()
	update_login = ("UPDATE USER_INFO SET LAST_LOGIN = CURDATE() WHERE USER_ID = %s")
	update_crit = (username,)
	cursor.execute(update_login, update_crit)
	conn.commit()
	cursor.close()
	conn.close()

def createUser(form):
  conn = mysql.connector.connect(host=host, database=database, user=user, password=password)
  cursor = conn.cursor()
  add_user = ("INSERT INTO USER_INFO"
              "(USER_ID, PASSWORD, EMAIL_ADDRESS, AGE, LOCATION)"
               "VALUES (%s, %s, %s, %s, %s)")
  user_data = (form['userID'], form['password'], form['email'], form['age'], form['country'])
  cursor.execute(add_user, user_data)
  conn.commit()
  cursor.close()
  conn.close()
  
def addWin(username):
  conn = mysql.connector.connect(host=host, database=database, user=user, password=password)
  cursor = conn.cursor()
  add_win = ("UPDATE USER_INFO SET CAREER_WINS = CAREER_WINS + 1 WHERE USER_ID = %s")
  add_crit = (username,)
  cursor.execute(add_win, add_crit)
  conn.commit()
  cursor.close()
  conn.close()
  
  

