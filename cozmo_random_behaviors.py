import os
import sys
os.environ['COZMO'] = "/home/casey/git/cozmo-python-sdk/src"
sys.path.append(os.environ['COZMO'])
import cozmo
import random
import time
from PIL import Image


from cozmo.util import degrees, distance_mm, speed_mmps

class CozmoBehavior():

    def __init__(self, face_img_path='resources/cozmo_faces/'):
        self.ts = None
        self.faces = [face_img_path+f for f in os.listdir(face_img_path) if os.path.isfile(os.path.join(face_img_path, f))]
        self.current_behaviors = None
        self.random_variables = None

    def set_timestamp(self, ts):
        self.ts = ts


    def play_behavior_1(self, robot):        
        all_actions = self.current_behaviors
        random_variables = self.random_variables
        for actions in all_actions:
            for behavior in actions:
                action = behavior[0]
                if action == 'display_oled_face_image':
                   robot.display_oled_face_image(random_variables['f'], random_variables['f_d'] * 1000.0, in_parallel=True)               
                if action == 'say_text':
                    robot.say_text(behavior[1], play_excited_animation=False, use_cozmo_voice=True, 
                            duration_scalar=random_variables['t'], voice_pitch=random_variables['v_p'], in_parallel=True, num_retries=1)
                if action == 'set_lift_height':
                    robot.set_lift_height(random_variables['a'], accel=10.0, max_speed=10.0, duration=random_variables['t'], 
                            in_parallel=True, num_retries=random_variables['ar'])
                if action == 'set_head_angle':
                    robot.set_head_angle(degrees(random_variables['h']), accel=10.0, max_speed=10.0, duration=random_variables['t'], 
                            warn_on_clamp=True, in_parallel=True, num_retries=random_variables['he'])
                if action == 'drive_wheels':
                    robot.drive_wheels(l_wheel_speed=random_variables['lw'], r_wheel_speed=random_variables['rw'], 
                                    l_wheel_acc=None, r_wheel_acc=None, 
                                    duration=random_variables['t'])  
            # starting position
            time.sleep(1.0)
        robot.set_lift_height(0, in_parallel=True)
        robot.set_head_angle(degrees(-10.0), in_parallel=True)            


    def generate_random_behavior_1(self,robot):

        num_loops = random.randint(1,5)

        all_actions = []

        for loop in range(num_loops):

            ar = random.randint(0,4)
            t = random.randint(1,3)
            he = random.randint(0,4)
            lwhe = random.randint(0,4)
            rwhe = random.randint(0,4)
            utterance = random.choice(['ehhhh?','ehhhh!','oh!','hm','oi','umm','aa?','aa!','uu?','uu!','rue!','rue?','eyy?','eyy!'])

            h = -25.00 + ((he/4) * 69.50)
            a = (ar/4) * 1.0 
            rw = (rwhe/4)*100 
            lw = (lwhe/4)*100 

            # random noise at a pitch determined by other features
            total = (he + ar + lwhe + rwhe) / 2    
            intensity = (total) / 8.0
            v_p = -1.0 + intensity
            random_variables = {'ar': ar,'t': t, 'he': he, 'lwhe': lwhe, 'rwhe': rwhe, 'utterance' : utterance, 'h': h, 'a' : a, 'rw' : rw, 'lw' : lw, 'v_p' : v_p}            
            print(v_p)
            def bool_choice():
                return random.choice([True, False])

            actions = []

            if bool_choice():
                face = random.choice(self.faces)
                f = Image.open(face).resize(cozmo.oled_face.dimensions(), Image.NEAREST)
                f = cozmo.oled_face.convert_image_to_screen_data(f, invert_image=False)
                f_d = random.randint(2,5)
                random_variables['f'] = f
                random_variables['f_d'] = f_d               
                actions.append(('display_oled_face_image', face, '{} * 1000.0'.format(f_d), 'in_parallel=True'))
                robot.display_oled_face_image(f, f_d * 1000.0, in_parallel=True)               

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


            # starting position
            time.sleep(1.0)
            actions.append(('set_lift_height', '0', 'in_parallel=True'))
            robot.set_lift_height(0, in_parallel=True)
            actions.append(('set_head_angle', 'degrees(-10.0)', 'in_parallel=True'))
            robot.set_head_angle(degrees(-10.0), in_parallel=True)            
            all_actions.append(actions)
            self.current_behaviors = all_actions
            self.random_variables = random_variables

        with open("functions.txt", 'a') as file:
            for action in all_actions:
                file.write('-\n')
                for function in action:
                    file.write(str(self.ts) + ' ' + str(function)+'\n')
        return all_actions

    def init_all(self, robot : cozmo.robot.Robot):
        self.generate_random_behavior_1(robot)

    def init_all_1(self, robot : cozmo.robot.Robot):
        self.play_behavior_1(robot)
        
    def generate_random_behavior(self):
        cozmo.run_program(self.init_all, use_viewer=False, force_viewer_on_top=False)

    def play_behavior(self):
        cozmo.run_program(self.init_all_1, use_viewer=False, force_viewer_on_top=False)