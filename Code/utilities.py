from PIL import Image, ImageTk
import subprocess
import time
import matplotlib.pyplot as plt
from datetime import datetime

# Startup function, to get the maximum position and minimum position.
# Uses sleep to be sure it's on the right positions
def start_up(rc, ch):
    bound = []                          
    startPos = ch.getVoltageRatio()     
    bound.append(startPos)              
    rc.setTargetPosition(140)           
    rc.setEngaged(True)
    time.sleep(5)                       
    endPos = ch.getVoltageRatio()       
    time.sleep(1)
    bound.append(endPos)
    rc.setTargetPosition(100)
    rc.setEngaged(True)
    time.sleep(8)
    rc.setEngaged(False)
    print(f'Start position is {startPos}')
    print(f'End position is {endPos}')
    write_to_bound_file(bound)
    return bound

# Reads out the position as voltage
def get_pos(ch):
    return ch.getVoltageRatio()

# Sets the thrust of the vessel
def set_thrust(rc,thrust):
    rc.setTargetPosition(thrust)
    rc.setEngaged(True)

# Scales the thrust to operate within reasonable thurst areas
def scale_u(u):
    new_u = 0
    if u < 90:
        new_u = 90
    elif u > 145:
        new_u = 145
    else:
        new_u = u
    return new_u

# Here comes all the functions doing operations on text files:
# -------------------------------------------------------------

# Write the boundaries to file with correct syntax
def write_to_bound_file(liste):
    temp = []
    filename = "textfiles/bound.txt"
    f = open(filename, "w")
    temp.append(str(liste[0]) + "\n")
    temp.append(str(liste[1]))
    f.writelines(temp)
    f.close()

# Reads out the boundaries and return them as a list
def read_bound():
    file = open("textfiles/bound.txt","r").read()
    lines = file.split("\n")
    return [float(lines[0]),float(lines[1])]

# Clears a file
def clear_file(filename):
    file = open(filename, "w")  
    file.write('')
    file.close()

# Reads out parameters from a given file and retun them as a list
def file_to_list(filename):
    file = open(filename,'r').read()
    lines = file.split('\n')
    xs, ys = [],[]
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(float(x))
            ys.append(float(y))
    return xs,ys

# Appends two value to a given file
def write_to_file(filename,a,b):
    file = open(filename, "a")  
    file.write(f'{str(a)},{str(b)}\n')
    file.close()

# Reads out the parameters from a file, given a filename
def read_parameters_from_file(filename):
    f = open(filename,'r').read()
    lines = f.split('\n')
    temp = []
    for elem in lines:
        temp.append(float(elem.split('=')[1]))
    return temp

# Overwrite the parameters of a given file 
def write_parameters_to_file(filename,kp,ki,kd,time,ref):
    f = open(filename,'w')
    f.write(f"kp = {kp}\n")
    f.write(f"ki = {ki}\n")
    f.write(f"kp = {kd}\n")
    f.write(f"t = {time}\n")
    f.write(f"ref = {ref}")

# -------------------------------------------------------------

# a function which loads images in the GUI_plot function
def load_image(path, window, key):
    try:
        image = Image.open(path)
        image.thumbnail((600, 600))
        photo_img = ImageTk.PhotoImage(image)
        window[key].update(data=photo_img)
    except:
        print(f"Not possible to open file from {path}!")

# plot the position and refernce and save them
def plot_pos(file1,file2,kp,ki,kd,bound):
    fig, ax = plt.subplots()
    xs_pos,ys_pos = file_to_list(file1)
    xs_ref,ys_ref = file_to_list(file2)
    ax.plot(xs_pos, ys_pos, label = "Pos")
    ax.plot(xs_ref, ys_ref, label = "Ref")
    ax.set_ylim(bound[0] + 0.05 ,bound[1] - 0.05)
    ax.legend()
    ax.grid(True)
    ax.set_xlabel("Time")
    ax.set_ylabel("Thrust")
    ax.set_title(f"Position of the vessel, kp = {kp},ki = {ki},kd = {kd}")

    # Saves plot
    save_results_to = 'Results/Results_pos_ref/' 
    plt.savefig(save_results_to + f'image{datetime.now().strftime("%d,%m %H:%M:%S")}.png',dpi=600)
    save_results_to = 'Results/GUI_plots/' 
    plt.savefig(save_results_to + f'pos.png',dpi=600)

# plot the PID values and save them
def plot_PID(fileP,fileI,fileD):
    fig, ax = plt.subplots()
    colors = ['red','yellow','black']
    files = [fileP,fileI,fileD]
    labels = ["P","I","D"]
    for i in range(3):
        xs,ys = file_to_list(files[i])
        ax.plot(xs,ys,color = colors[i],label = labels[i])
    ax.legend()
    ax.grid(True)
    ax.set_xlabel("Time")
    ax.set_ylabel("Thrust")
    ax.set_title("PID values compared")

    # Saves plot
    save_results_to = 'Results/Results_PID/' 
    plt.savefig(save_results_to + f'image{datetime.now().strftime("%d,%m %H:%M:%S")}.png',dpi=600)
    save_results_to = 'Results/GUI_plots/' 
    plt.savefig(save_results_to + f'PID.png',dpi=600)

# write the vtf file 
def make_vtf_file(bound):
    filename = "textfiles/pos.txt"
    x,y_pos = file_to_list(filename)

    filename2 = 'vtf_file.vtf'
    file = open(filename2,'w')

    # Parameters for vessel
    l = 8
    w = 2
    h = 1

    # hardcoe the vessel
    file.write("*VTF-1.00\n")
    file.write("\n")
    file.write("!   8 noder i en firkant :\n")
    file.write("*NODES            1\n")
    file.writelines([f"{int(-w/2)}. {int(-l/2)}. 0.\n",f"{int(-w/2)}.  {int(l/2)}. 0.\n",f" {int(w/2)}. {int(-l/2)}. 0.\n",f" {int(w/2)}.  {int(l/2)}. 0.\n",f"{int(-w/2)}. {int(-l/2)}. {h}.\n",f"{int(-w/2)}.  {int(l/2)}. {h}.\n",f" {int(w/2)}. {int(-l/2)}. {h}.\n",f" {int(w/2)}.  {int(l/2)}. {h}.\n"])
    file.write("\n")

    # Parameters for tank
    l_t = 32
    w_t = 6

    # hardcode the tank
    file.write("!   4 noder i et plan :\n")
    file.write("*NODES            2\n")
    file.writelines([f"{int(-w_t/2)} {int(-l_t/2)} 0\n",f"{int(w_t/2)} {int(-l_t/2)} 0\n",f"{int(-w_t/2)} {int(l_t/2)} 0\n",f"{int(w_t/2)} {int(l_t/2)} 0\n"])
    file.write("\n")


    file.write("!   8 noder i en firkant :\n")
    file.write("*ELEMENTS            1\n")
    file.write("%NODES #1\n")
    file.write("%QUADS\n")
    file.writelines(["1 2 4 3\n","5 6 8 7\n","1 2 6 5\n","3 4 8 7\n","1 3 7 5\n","2 4 8 6\n"])
    file.write("\n")


    file.write("!   8 noder i en firkant :\n")
    file.write("*ELEMENTS            2\n")
    file.write("%NODES #2\n")
    file.write("%QUADS\n") 
    file.write("1 2 4 3\n") 
    file.write("\n")


    file.write("*GLVIEWGEOMETRY 1\n")
    file.write("%ELEMENTS\n")
    file.write("1 2\n")
    file.write("\n")

    # iterates to write all the position to the file
    scaled_y_pos = []
    for i in range(len(y_pos)):
        scaled_y = (y_pos[i]-bound[0])/(bound[1]-bound[0])
        n_scaled_y = -l_t/2 * (scaled_y - 0.5)
        scaled_y_pos.append(int(n_scaled_y))


    for i in range(0,len(y_pos)):
        file.write(f"*RESULTS   {i+1}\n")
        file.write("%DIMENSION 3\n")
        file.write("%PER_NODE #1\n")
        for j in range(0,8):
            file.write(f"0. {scaled_y_pos[i]}. 0\n")
        file.write("\n")
    

    file.write("*GLVIEWVECTOR   1\n")
    file.write('%NAME "Displacement"\n')
    for i in range(0,len(y_pos)):
        file.write(f"%STEP   {i+1}\n")
        file.write(f" {i+1}\n")


    file.close()
    print("Finished with writing to file")

# runs the run.sh script which runes both main and live_plot
def subprocess_call():
    subprocess.call(['sh','./run.sh'])

