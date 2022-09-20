#!/usr/local/bin/python

import PySimpleGUI as sg
from PIL import Image, ImageTk

from main import main
from utilities import read_parameters_from_file, load_image, write_parameters_to_file, subprocess_call

#--------------------------------------------------------------------------------------------------------------------- 

# GUI_plots pops up when the simulation is over, and load the saved plots

def GUI_plots():

    path1 = 'Results/GUI_plots/pos.png' 
    path2 = 'Results/GUI_plots/PID.png'

    layout = [  [sg.Image(key = "image1"),sg.Image(key = "image2")],
                [sg.Button("Load plots",font=("Helvetica", 20)),sg.Button("Exit",font=("Helvetica", 20))]
        
                    ]
    window = sg.Window("Plot GUI",layout,size=(1250,520))

    while(True):
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            break
        if event == "Load plots":
            load_image(path1,window,"image1")
            load_image(path2,window,"image2")

    window.close()

#---------------------------------------------------------------------------------------------------------------------

def GUI_startup():
    # The layout consists of the GUI window with text,buttons and input cells
    layout = [  [sg.Text("Welcome to dynamic positioning controll system",font=("Helvetica", 30))], 
                [sg.Text("You have two choicses: run the code with tuned PID values or run ",font=("Helvetica", 20))],
                [sg.Text("the code with your own PID values",font=("Helvetica", 20))],
                [sg.Button("Tuned PID values",key="pd",font=("Helvetica", 20)), sg.Button("Your own PID values",key="yov",font=("Helvetica", 20))],

                [sg.Text("Kp:", key="kp", visible=False, font=("Helvetica", 20)),sg.InputText(key="input_kp",visible=False,font=("Helvetica", 20),size = (10,1))],
                [sg.Text(" Ki:", key="ki", visible=False, font=("Helvetica", 20)),sg.InputText(key="input_ki",visible=False,font=("Helvetica", 20),size = (10,1))],
                [sg.Text("Kd:", key="kd", visible=False, font=("Helvetica", 20)),sg.InputText(key="input_kd",visible=False,font=("Helvetica", 20),size = (10,1))],
                [sg.Text("Duration:", key="time", visible=False, font=("Helvetica", 20)),sg.InputText(key="input_time",visible=False,font=("Helvetica", 20),size = (10,1))],
                [sg.Text("Reference point:", key="ref", visible=False, font=("Helvetica", 20)),sg.InputText(key="input_ref",visible=False,font=("Helvetica", 20),size = (10,1))],
                [sg.Button('Confirm',key="confirm",visible=False,font=("Helvetica", 20)), sg.Text("Try again!",key="error",visible=False,font=("Helvetica", 20))],
                [sg.Button('Run',key="run",visible=False,font=("Helvetica", 20)),sg.Button('Show live plots',key="live_plot",visible=False,font=("Helvetica", 20))],


                [sg.Button('Exit',key="exit",font=("Helvetica", 20))]
                    ]

    # Create the Window
    window = sg.Window('DP GUI', layout,size=(700,450))
    
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        # Continuesly reading the window
        event, values = window.read()
        # If user closes window or clicks cancel
        if event == sg.WIN_CLOSED or event == "exit": 
            break
        # If the user presses predetermined values
        if event == "pd": 
            print("You choose predetermind values")
            parameters = read_parameters_from_file("textfiles/tuningparameters.txt")
            kp = parameters[0] # values are read from tuningparameters
            ki = parameters[1] 
            kd = parameters[2]
            t = parameters[3]
            ref = parameters[4]
            window["run"].Update(visible = True) # the run buttom becomes visible
        # If the user presses your own value
        if event == "yov": 
            print("You want to choose your own values")
            window["pd"].Update(visible = False)
            window["yov"].Update(visible = False)

            state = True # makes all the input cells visible
            window["kp"].Update(visible = state)
            window["input_kp"].Update(visible = state)
            window["ki"].Update(visible = state)
            window["input_ki"].Update(visible = state)
            window["kd"].Update(visible = state)
            window["input_kd"].Update(visible = state)
            window["time"].Update(visible = state)
            window["input_time"].Update(visible = state)
            window["ref"].Update(visible = state)
            window["input_ref"].Update(visible = state)
            window["confirm"].Update(visible = state)
        # Have to press confirm to save the input values
        if event  == "confirm": 
            kp = (values['input_kp'])
            ki = (values['input_ki'])
            kd = (values['input_kd'])
            t = (values['input_time'])
            ref = (values['input_ref'])
            # Needs to check that the input values are valid
            if len(kp)<1 or len(ki)<1 or len(kd)<1 or len(t)<1 or len(ref)<1:
                print("Error")
                window["error"].Update(visible = True)
            else:
                window["error"].Update(visible = False)
                kp = float(kp)
                ki = float(ki)
                kd = float(kd)
                t = float(t)
                ref = float(ref)
                window["run"].Update(visible = state)
    
        if event == "run":  
            # Need to save the parameters, to make the aviable for main
            file = "textfiles/parameters.txt"
            write_parameters_to_file(file,kp,ki,kd,t,ref)  
            # Main and live_plot runs
            subprocess_call()  
            # Launch a windows which gives the possiblity to see the results
            GUI_plots()         
            
    window.close()

#---------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    GUI_startup()