from flask import Flask, render_template,request, redirect, request
import webbrowser
from threading import Timer
from cozmo_random_behaviors import CozmoBehavior
import json
import os
import csv
import time

app = Flask(__name__)

cozmo_behavior = CozmoBehavior()
current_timestamp = None

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/startRandomBehavior', methods=['POST'])
def startRandomBehavior(): 
    global current_timestamp
    current_timestamp = time.time()
    cozmo_behavior.set_timestamp(current_timestamp)
    cozmo_behavior.start()
    return "success"

def open_browser():
      webbrowser.open_new('http://127.0.0.1:8080/')

@app.route('/enterDataInFile', methods=['POST'])
def enterDataInFile():
    global current_timestamp
    description = request.form["description"]
    data = request.form["form"]
    data = data.split("&")
    dataAsDict = {}

    for key in data:
        key = key.split("=")
        dataAsDict[key[0]] = key[1]

    interest_alarm = dataAsDict["likert2"]
    confusion_understanding = dataAsDict["likert3"]
    frusteration_relief = dataAsDict["likert4"]
    sorrow_joy = dataAsDict["likert5"]
    anger_gratitude = dataAsDict["likert6"]
    fear_hope = dataAsDict["likert7"]
    boredom_surprise = dataAsDict["likert8"]
    disgust_desire = dataAsDict["likert9"]
    
    if os.path.isfile("responses.csv"):
         with open("data.csv", 'a') as file:
            writer = csv.writer(file)
            writer.writerow([current_timestamp, description, interest_alarm, confusion_understanding, frusteration_relief, sorrow_joy, anger_gratitude, fear_hope, boredom_surprise, disgust_desire])
    else:
        with open("responses.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp, Description", "Interst/Alarm", "Confusion/Understanding", "Frusteration/Relief","Sorrow/Joy", "Anger/Gratitude","Fear/Hope", "Boredom/Surprise","Disgust/Desire"])
            writer.writerow([current_timestamp, description, interest_alarm, confusion_understanding, frusteration_relief, sorrow_joy, anger_gratitude, fear_hope, boredom_surprise, disgust_desire])    
    return "success"

@app.route('/addEmail', methods=["POST"])
def addEmail():
    userEmail = request.form["email"]
    if os.path.isfile("email.txt"):
        with open("email.txt", 'a') as file:
            file.write("\n" + userEmail)
    else:
        with open("email.txt", 'w') as file:
            file.write(userEmail)
    return "success"

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(port=8080)
