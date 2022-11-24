from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,flash,g
app = Flask(__name__)
from werkzeug.exceptions import abort
from db import get_db
import os
import random
import csv
from botConfig import myBotName, chatBG, botAvatar, useGoogle, confidenceLevel
from botRespond import getResponse



@app.route('/')
def indexx(page=1):
    db,c=get_db()
    c.execute('select * from publicacion where id>=%s and id<=%s',(page*10-10,page*10))
    calls=c.fetchall()
    num=len(calls)
    print(num)
    return render_template('tiak/index.html',calls=calls,num=num,page=page)

@app.route('/<int:page>')
def index(page):
    db,c=get_db()
    c.execute('select * from publicacion where id>=%s and id<=%s',(page*10-10,page*10))
    calls=c.fetchall()
    num=len(calls)/10+1
    print(num)
    return render_template('tiak/index.html',calls=calls,num=num,page=page)

@app.route('/crear',methods=('GET','POST'))
def create():
    if request.method=='POST':   
        hist=request.form['historia']
        error=None
        if not hist:
            error='historia requerida'
        if error is not None:
            flash(error)    
        else:
            db,c=get_db()
            c.execute('insert into publicacion (Comentario) values (%s)',(hist,))
            db.commit()
            return redirect(url_for('indexx')) 
        return redirect(url_for('indexx'))
    return render_template('tiak/historia.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'bot.png', mimetype='image/vnd.microsoft.icon')


# bot todo la programacion y ruta


chatbotName = myBotName
print("Bot Name set to: " + chatbotName)
print("Background is " + chatBG)
print("Avatar is " + botAvatar)
print("Confidence level set to " + str(confidenceLevel))

#Create Log file
try:
    file = open('BotLog.csv', 'r')
except IOError:
    file = open('BotLog.csv', 'w')

def tryGoogle(myQuery):
	#print("<br>Try this from my friend Google: <a target='_blank' href='" + j + "'>" + query + "</a>")
	return "<br><br>You can try this from my friend Google: <a target='_blank' href='https://www.google.com/search?q=" + myQuery + "'>" + myQuery + "</a>"

@app.route("/bot")
def bot():
    return render_template("bot.html", botName = chatbotName, chatBG = chatBG, botAvatar = botAvatar)

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    botReply = str(getResponse(userText))
    if botReply is "IDKresponse":
        botReply = str(getResponse('IDKnull')) ##Send the i don't know code back to the DB
        if useGoogle == "yes":
            botReply = botReply + tryGoogle(userText)
    elif botReply == "getTIME":
        botReply = getTime()
        print(getTime())
    elif botReply == "getDATE":
        botReply = getDate()
        print(getDate())
    ##Log to CSV file
    print("Logging to CSV file now")
    with open('BotLog.csv', 'a', newline='') as logFile:
        newFileWriter = csv.writer(logFile)
        newFileWriter.writerow([userText, botReply])
        logFile.close()
    return botReply




if __name__ == '__main__':
   app.run()