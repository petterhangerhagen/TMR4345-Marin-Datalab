from Phidget22.Phidget import *
from Phidget22.Devices.RCServo import *
from Phidget22.Devices.VoltageRatioInput import *

from PID import PID
from utilities import start_up, read_parameters_from_file, plot_PID,plot_pos, make_vtf_file


def main():

    run = True
    try:    # checks if the Phidget cards are connected
        rc = RCServo()
        ch = VoltageRatioInput()
        ch.setChannel(4)
        ch.openWaitForAttachment(5000)
        rc.openWaitForAttachment(5000)
    except:
        print("Not connected to the phidigets")
        run = False

    if run:
        print("main is running")

        # Reads the chosen parameters in
        parameters_list = read_parameters_from_file("textfiles/parameters.txt")
        kp = parameters_list[0]
        ki = parameters_list[1]
        kd = parameters_list[2]
        t = parameters_list[3]
        ref = parameters_list[4]

        # Runs the start up function which sets the boundaries conditions
        bound = start_up(rc, ch)
        # Calculate the reference to be correct with respect to the varying boundaries
        # This needed to be changed after the lab setup was fixed 06.05.2022
        # The potentiometer was changed to read higher voltage at the end then on the start
        # It was the opposite way before the change. 
        r = bound[1] + (1-ref) * (bound[0] - bound[1])  
        dt = 0.25 # integration step 
        PID(kp, ki, kd, t, dt, r, rc, ch) # PID runs

        # All the files with the data needed to make plots
        files = ["textfiles/pos.txt","textfiles/ref.txt","textfiles/P.txt","textfiles/I.txt","textfiles/D.txt"]

        # Plot for position vs reference
        plot_pos(files[0],files[1],kp,ki,kd,bound)

        # Plot the PID values
        plot_PID(files[2],files[3],files[4])

        # Making a VTF file 
        make_vtf_file(bound)

        # close the Phidget cards
        rc.close()
        ch.close()
    

if __name__ == "__main__":
    main()
