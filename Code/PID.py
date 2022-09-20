import matplotlib.pyplot as plt
import time
from datetime import datetime

from utilities import clear_file, write_to_file, get_pos, set_thrust, scale_u


# The PID controller
def PID(kp, ki, kd, timeout, dt, r, rc, ch):
    
    # sets the start deviation 
    # This also needed to be changed, when the setup was changed, 06.05.2022
    e_prev = -r + get_pos(ch)  # e = r - y
    e_sum = 0
    e = e_prev

    # All the files i need to save data
    files = ["textfiles/pos.txt","textfiles/ref.txt","textfiles/P.txt","textfiles/I.txt","textfiles/D.txt"]

    # Clear all the files
    for file in files:
        clear_file(file)

    sleep = 0.20    # the sleep time of the while loop
    timeout_start = time.time()

    # The loop runs until the time reaches timeout
    while time.time() < timeout_start + timeout: 
        # the current time from the loop started
        now_time = time.time()-timeout_start 
        # Changes the reference at mid time. Used to test the systems strengh
        # if ((timeout/2) - sleep/2) < now_time < ((timeout/2) + sleep/2):
        #    r -= 0.04

        e_prev = e  # e_prev is set to be the error from the last timed the loop 
        # gets a new error
        # This also needed to be changed, when the setup was changed, 06.05.2022    
        e = -r + get_pos(ch) 

        # Proprotional part
        P = kp*e

        # Integrator part, sums the errors
        e_sum = e_sum + e * dt
        I = ki * e_sum
        # Needs make sure the integration doesn't gets to big or low
        if I > 90:
            e_sum = 90/ki
        elif I < -90:
            e_sum = -90/(ki)
        

        # Derivative part
        dedt = (e - e_prev)/dt
        D = kd * dedt
        

        
        # Needs to add 90 because this is the angle where the thrust is zero
        u = P + I + D + 90  
        # Scales the thurst to be within working range, else its zero 
        new_u = scale_u(u)
        # Apply thrust 
        set_thrust(rc,new_u)


        # Write the positon and reference to file
        write_to_file(files[0],now_time,get_pos(ch))
        write_to_file(files[1],now_time,r)


        # write the PID values to file
        write_to_file(files[2],now_time,P)
        write_to_file(files[3],now_time,I)
        write_to_file(files[4],now_time,D)


        # Sleep the loop to make it run approximatly every 0.25 seconds, 
        # becuase it's when the voltage also is updated
        time.sleep(sleep)
        
    # Stops the thrust appleied when the loop is finished
    rc.setEngaged(False)




