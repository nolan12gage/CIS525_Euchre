from flask import Flask, flash, redirect, render_template, request, session, abort
import mysql.connector
import re

host = 'localhost'
database = 'euchre_users'
user = 'root'
password = 'mysql'

def validateID(id):
  return id

def validatePassword(password):
  return password
  
def validateAge(age):
  return age

def validateEmail(email):
  return email

def validateLocation(location):
  return location

def validateForm(form):  
  return True

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
  

