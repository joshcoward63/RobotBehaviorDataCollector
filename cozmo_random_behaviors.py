import os
import sys
os.environ['COZMO'] = "https://bitbucket.org/bsu-slim/cozmo-python-sdk"

sys.path.append(os.environ['COZMO'])
import cozmo
import retico
import random
import time

from cozmo.util import degrees, distance_mm, speed_mmps

from retico.core.debug.console import DebugModule
from retico.modules.cozmo.cozmo_state import CozmoStateModule

def generate_random_behavior(robot):

    num_loops = random.randint(1,5)

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
        rw = (rwhe/4)*500 
        lw = (lwhe/4)*500 


        # random noise at a pitch determined by other features
        total = (he + ar + lwhe + rwhe) / 2    
        intensity = (total) / 8.0
        v_p = -1.0 + intensity

        def bool_choice():
            return random.choice([True, False])

        if bool_choice():
            robot.say_text(utterance, play_excited_animation=False, use_cozmo_voice=True, 
                        duration_scalar=t, voice_pitch=v_p, in_parallel=True, num_retries=1)

        if bool_choice():
            robot.set_lift_height(a, accel=10.0, max_speed=10.0, duration=t, 
                        in_parallel=True, num_retries=ar)

        if bool_choice():                        
            robot.set_head_angle(degrees(h), accel=10.0, max_speed=10.0, duration=t, 
                        warn_on_clamp=True, in_parallel=True, num_retries=he)

        if bool_choice():                        
            robot.drive_wheels(l_wheel_speed=lw, r_wheel_speed=rw, 
                            l_wheel_acc=None, r_wheel_acc=None, 
                            duration=t)   
        # robot.display_oled_face_image(face_image, duration_s * 1000.0, in_parallel=True)   

        # starting position
        time.sleep(1.0)
        robot.set_lift_height(0, in_parallel=True)
        robot.set_head_angle(degrees(-10.0), in_parallel=True)                                       


def init_all(robot : cozmo.robot.Robot):

    cozmo_state = CozmoStateModule(robot)
    debug = DebugModule()

    cozmo_state.subscribe(debug)

    cozmo_state.run()
    debug.run()

    generate_random_behavior(robot)

    input()

    cozmo_state.stop()
    debug.stop()


def start():
    cozmo.run_program(init_all, use_viewer=False, force_viewer_on_top=False )