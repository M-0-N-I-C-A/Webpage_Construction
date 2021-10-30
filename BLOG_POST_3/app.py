# export FLASK_ENV=development
# flask run
# by Monica Z

from flask import Flask, Blueprint, current_app, g, render_template, redirect, request, flash, url_for, session
from flask.cli import with_appcontext

import sqlite3
import click

import random
import string


app = Flask(__name__)


@app.route("/")
def main():
	return render_template("main_better.html")


@app.route('/submit/', methods=['POST', 'GET'])
def submit():
	if request.method == 'POST':
		try:
			insert_message(request)
			return render_template('submit.html', submission = True)
		except:
			return render_template('submit.html', failure = True)
	return render_template('submit.html')



@app.route('/view/')
def view():
    messages=random_messages(3)
    return render_template('view.html', messages=messages)


@app.route('/viewall/')
def viewall():
	db = get_message_db()
	messages = db.execute("SELECT * FROM messages").fetchall()
	return render_template('viewall.html', messages = messages)



def get_message_db():
    if 'message_db' not in g:
        g.message_db = sqlite3.connect('message_db.sqlite')

    cursor = g.message_db.cursor()
    cmd = """CREATE TABLE IF NOT EXISTS messages(id INTEGER, handle TEXT, message TEXT)"""
    cursor.execute(cmd)
    return g.message_db


def insert_message(request):
    message = request.form['message']
    handle = request.form['handle']
    db = get_message_db()
    cursor = db.cursor()
    cmd = """SELECT COUNT(*) FROM messages"""
    cursor.execute(cmd)
    db.execute(f""" INSERT INTO messages(id, handle, message) VALUES ({cursor.fetchone()[0]+1}, "{handle}", "{message}");""")
    db.commit()
    db.close()



def random_messages(n):
    db = get_message_db()
    cursor = db.cursor()
    cmd = f"""SELECT * FROM messages LIMIT {n}"""
    cursor.execute(cmd)
    data = cursor.fetchall()
    db.close()
    return data 




		




