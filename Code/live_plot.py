import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

from utilities import file_to_list,read_bound, read_parameters_from_file, clear_file

# makes a live animation by using the animation class to matplotlib
def plot_ani(file1,file2):
    fig, ax = plt.subplots()

    clear_file(file1) # clears the files
    clear_file(file2)

    # need to have the duration of the simulation to know when to close the window
    parameters_list = read_parameters_from_file("textfiles/parameters.txt")
    t = parameters_list[3]
    start_time = time.time()
    
    # the function which updates the animation with new points added
    def animate(i):
        if time.time() > start_time + t + 20:
            exit()
        x_pos,y_pos = file_to_list(file1)
        x_ref,y_ref = file_to_list(file2)
        bound = read_bound()

        ax.clear()
        ax.plot(x_pos, y_pos,label="pos")
        ax.plot(x_ref,y_ref,label="ref")
        ax.set_ylim(bound[0] + 0.05, bound[1] - 0.05)
        ax.set_title("Live plot of vessel vs reference")
        ax.set_xlabel("Time")
        ax.set_ylabel("Position")
        ax.grid(True)
        ax.legend()

    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()



if __name__ == "__main__":
    file1 = "textfiles/pos.txt"
    file2 = "textfiles/ref.txt"
    plot_ani(file1,file2)




