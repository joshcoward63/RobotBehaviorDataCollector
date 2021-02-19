### Robot Data Collector

Locally hosted web app used to deploy random behaviors for 10-15 seconds on either the Cozmo or Misty robots.  
Once the random behavior has been performed the user will be asked to describe what they saw and rate a set of  
attributes on a scale of 1-5.

Files Incuded:
main.py - flask app that deploys webite on localhost (main file)  
cozmo_random_behaviors.py - file contains code responsible for generating random behaviors  
templates/index.html - main file displayed in web  
static/index.css - styling sheet for app  
README.md - this file  

Execution instructions:  
    1. Make sure flask is installed, from terminal type ```pip install flask``` and press enter.  
    2. Navigate to this directory and run the following command to run the program ```python main.py```  
    