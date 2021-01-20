from flask import Flask, render_template,request, redirect
import webbrowser
from threading import Timer
import cozmo_random_behaviors
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/startRandomBehavior', methods=['POST'])
def startRandomBehavior(): 
    print("it ran")
    cozmo_random_behaviors.start()

def refreshTime():
    #Time is set to 0
    pass

def startTimer():
    #Waits 5 minutes if no response from user refresh page.
    pass

def open_browser():
      webbrowser.open_new('http://127.0.0.1:8080/')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(port=8080)
