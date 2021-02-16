import os
import sys
os.environ['COZMO'] = "/home/casey/git/cozmo-python-sdk/src"

sys.path.append(os.environ['COZMO'])
import cozmo
import random
import time

from cozmo.util import degrees, distance_mm, speed_mmps

class CozmoBehavior():

    def __init__(self):
        self.ts = None

    def set_timestamp(self, ts):
        self.ts = ts

    def generate_random_behavior(self, robot):

        num_loops = random.randint(1,5)

        all_actions = []

        for loop in range(num_loops):

            ar = random.randint(0,4)
            t = random.randint(1,3)
            # face = 
            he = random.randint(0,4)
            lwhe = random.randint(0,4)
            rwhe = random.randint(0,4)
            utterance = random.choice(['ehhhh?','ehhhh!','oh!','hmmm','oi','umm','aa?','aa!','uu?','uu!','rue!','rue?','eyy?','eyy!'])

            h = -25.00 + ((he/4) * 69.50)
            a = (ar/4) * 1.0 
            rw = (rwhe/4)*100 
            lw = (lwhe/4)*100 


            # random noise at a pitch determined by other features
            total = (he + ar + lwhe + rwhe) / 2    
            intensity = (total) / 8.0
            v_p = -1.0 + intensity

            def bool_choice():
                return random.choice([True, False])

            actions = []

            if bool_choice():
                actions.append(('say_text', utterance))
                robot.say_text(utterance, play_excited_animation=False, use_cozmo_voice=True, 
                            duration_scalar=t, voice_pitch=v_p, in_parallel=True, num_retries=1)

            if bool_choice():
                actions.append(('set_lift_height', a, 'accel=10.0', 'max_speed=10.0', 'duration={}'.format(t),'in_parallel=True', 'num_retries={}'.format(ar)))
                robot.set_lift_height(a, accel=10.0, max_speed=10.0, duration=t, 
                            in_parallel=True, num_retries=ar)

            if bool_choice():   
                actions.append(('set_head_angle','degrees({})'.format(h), 'accel=10.0', 'max_speed=10.0', 'duration={}'.format(t), 
                            'warn_on_clamp=True', 'in_parallel=True', 'num_retries={}'.format(he)))                  
                robot.set_head_angle(degrees(h), accel=10.0, max_speed=10.0, duration=t, 
                            warn_on_clamp=True, in_parallel=True, num_retries=he)

            if bool_choice():         
                actions.append(('drive_wheels', 'l_wheel_speed={}'.format(lw), 'r_wheel_speed='.format(rw), 
                                'l_wheel_acc=None', 'r_wheel_acc=None', 'duration={}'.format(t)))               
                robot.drive_wheels(l_wheel_speed=lw, r_wheel_speed=rw, 
                                l_wheel_acc=None, r_wheel_acc=None, 
                                duration=t)   
            # robot.display_oled_face_image(face_image, duration_s * 1000.0, in_parallel=True)   

            # starting position
            time.sleep(1.0)
            actions.append(('set_lift_height', '0', 'in_parallel=True'))
            robot.set_lift_height(0, in_parallel=True)
            actions.append(('set_head_angle', 'degrees(-10.0)', 'in_parallel=True'))
            robot.set_head_angle(degrees(-10.0), in_parallel=True)            
            all_actions.append(actions)

        with open("functions.txt", 'a') as file:
            for action in all_actions:
                file.write('-\n')
                for function in action:
                    file.write(str(self.ts) + ' ' + str(function)+'\n')

    def init_all(self, robot : cozmo.robot.Robot):
        self.generate_random_behavior(robot)

    def start(self):
        cozmo.run_program(self.init_all, use_viewer=False, force_viewer_on_top=False )