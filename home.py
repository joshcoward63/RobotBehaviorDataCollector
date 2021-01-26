from flask import Flask, render_template,request, redirect, request
import webbrowser
from threading import Timer
# import cozmo_random_behaviors
import json
import os
import csv

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/startRandomBehavior', methods=['POST'])
def startRandomBehavior(): 
    print("it ran")
    # cozmo_random_behaviors.start()
    return "hello"

def open_browser():
      webbrowser.open_new('http://127.0.0.1:8080/')

@app.route('/enterDataInFile', methods=['POST'])
def enterDataInFile():
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
    try:
        with open("data.csv", 'a') as file:
            writer = csv.writer(file)
            writer.writerows([description, interest_alarm, confusion_understanding, frusteration_relief, sorrow_joy, anger_gratitude, fear_hope, boredom_surprise, disgust_desire])
    except IOError:
        with open("data.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(["Description", "Interst/Alarm", "Confusion/Understanding", "Frusteration/Relief","Sorrow/Joy", "Anger/Gratitude","Fear/Hope", "Boredom/Surprise","Disgust/Desire"])
            writer.writerow([description, interest_alarm, confusion_understanding, frusteration_relief, sorrow_joy, anger_gratitude, fear_hope, boredom_surprise, disgust_desire])
       


if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(port=8080)
