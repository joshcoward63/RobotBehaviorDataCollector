import os
import sys
import requests
import json
import threading
import time
import cozmo
import random
import time
from PIL import Image

class Robot:

    def __init__(self,ip):
        self.ip = ip

    def display_face(self, face, timeout):
        requests.post('http://{}/api/images/display'.format(self.ip),json={'FileName': face ,'TimeOutSeconds': timeout,'Alpha': 1})

    def set_volume(self, vol):
        requests.post('http://'+self.ip+'/api/audio/volume',json={"Volume": vol})         

    def say_text(self, text):
        requests.post('http://'+self.ip+'/api/tts/speak',json={"Text": '<speak>{}</speak>'.format(text)})       

    def move_arm(self,arm,position,velocity=75):
        assert position in range(-91,91), " moveArm: position needs to be -90 to 90"
        assert velocity in range(0,101), " moveArm: Velocity needs to be in range 0 to 100"
        requests.post('http://'+self.ip+'/api/arms',json={"Arm": arm, "Position":position, "Velocity": velocity})

    def move_head(self,roll,pitch,yaw,velocity=75):
        assert -45 <= roll <= 45
        assert -45 <= pitch <= 45
        assert -70 <= yaw <= 70
        assert velocity in range(0,101), " moveHead: Velocity needs to be in range 0 to 100"
        requests.post('http://'+self.ip+'/api/head',json={"Pitch": int(pitch), "Roll": int(roll), "Yaw": int(yaw), "Velocity": velocity})

    def drive_track(self,left_track_speed,right_track_speed):
        assert left_track_speed in range(-100,101) and right_track_speed in range(-100,101), " driveTrack: The velocities needs to be in the range -100 to 100"
        requests.post('http://'+self.ip+'/api/drive/track',json={"LeftTrackSpeed": left_track_speed,"RightTrackSpeed": right_track_speed})

    def reset(self):
        roll = 0
        pitch = 0
        yaw = 0
        position = 80
        self.move_head(roll, pitch, yaw, velocity=75)
        self.move_arm('left',position,velocity=75)
        self.move_arm('right',position,velocity=75)
        self.display_face('e_DefaultContent.jpg', 5)
    
    def stop(self):
        requests.post('http://'+self.ip+'/api/drive/stop')


class MistyBehavior():

    def __init__(self, ip, face_img_path='resources/misty_faces/'):
        self.ts = None
        # self.faces = [face_img_path+f for f in os.listdir(face_img_path) if os.path.isfile(os.path.join(face_img_path, f))]
        self.faces = ['e_Joy2.jpg', "e_Love.jpg",  "e_Sleepy4.jpg",
                        "e_ContentRight.jpg", "e_Amazement.jpg", "e_Terror.jpg",
                        "e_Anger.jpg", "e_Disoriented.jpg", "e_ApprehensionConcerned.jpg",
                        "e_Fear.jpg", "e_Sleepy.jpg", "e_Terror2.jpg", "e_Sleepy2.jpg",
                        "e_Sadness.jpg", "e_JoyGoofy2.jpg", "e_Rage4.jpg",  "e_Rage.jpg",
                        "e_ContentLeft.jpg", "e_Rage3.jpg", "e_DefaultContent.jpg", "e_EcstacyStarryEyed.jpg",
                        "e_Surprise.jpg", "e_Joy.jpg", "e_TerrorLeft.jpg",  "e_Sleepy3.jpg", 
                        "e_SystemCamera.jpg",  "e_TerrorRight.jpg"]
        self.robot = Robot(ip)
        self.robot.set_volume(20.0)
        self.current_behaviors = None

    def set_timestamp(self, ts):
        self.ts = ts


    def play_behavior(self):
        all_actions = self.current_behaviors
        for actions in all_actions:
            for behavior in actions:
                action = behavior[0]
                if action == 'display_face':
                    self.robot.display_face(behavior[1], behavior[2])
                if action == 'say_text':
                    self.robot.say_text(behavior[1])
                if action == 'move_arm':
                    arm = behavior[1]
                    position = behavior[2]
                    velocity = behavior[3]
                    if arm == 'both':
                        self.robot.move_arm('left',position,velocity=velocity)
                        self.robot.move_arm('right',position,velocity=velocity)
                    else:
                        self.robot.move_arm(arm,position,velocity=velocity)
                if action == 'move_head':
                    roll = behavior[1]
                    pitch = behavior[2]
                    yaw = behavior[3]
                    self.robot.move_head(roll, pitch, yaw, velocity=75)
                if action == 'drive_track':
                    left_track = behavior[1]
                    right_track = behavior[2]
                    duration = behavior[3]
                    self.robot.drive_track(left_track,right_track)  
                    time.sleep(duration)
                    self.robot.stop() 

            # starting position
            time.sleep(1.0)

        self.robot.reset() 
                


    def generate_random_behavior(self):

        num_loops = random.randint(1,5)

        all_actions = []

        for loop in range(num_loops):

            def bool_choice():
                return random.choice([True, False])

            actions = []

            if bool_choice():
                face = random.choice(self.faces)
                timeout = random.randint(1,5)
                actions.append(('display_face', face, timeout))             

            if bool_choice():
                utterance = random.choice(['oh!','hmm','oi','umm','aa?','aa!'])
                actions.append(('say_text', utterance))
                

            if bool_choice():
                arm = random.choice(['left', 'right', 'both'])
                position = random.randrange(-90, 90, 5)
                velocity = random.randrange(70,100,10)
                actions.append(('move_arm', arm, position, velocity))


            if bool_choice():   
                roll = 0
                pitch = 0
                yaw = 0
                velocity = 80
                if bool_choice(): roll += random.randrange(-45, 45, 5)
                if bool_choice(): pitch += random.randrange(-45, 45, 5)
                if bool_choice(): yaw = +random.randrange(-70, 70, 5)
                actions.append(('move_head', roll, pitch, yaw, velocity))                  
                

            if bool_choice():
                left_track = random.randrange(-50, 50, 2) 
                right_track = random.randrange(-50, 50, 2) 
                duration  = random.randrange(1,3)
                actions.append(('drive_track', left_track, right_track, duration))     

            velocity = 80
            actions.append(('move_head', 0, 0, 0, velocity))            
            actions.append(('move_arm', 'left', 80, velocity))
            actions.append(('move_arm', 'right', 80, velocity))                          
          
            all_actions.append(actions)

            self.current_behaviors = all_actions

        with open("functions_misty.txt", 'a') as file:
            for action in all_actions:
                file.write('-\n')
                for function in action:
                    file.write(str(self.ts) + ' ' + str(function)+'\n')

        return all_actions
