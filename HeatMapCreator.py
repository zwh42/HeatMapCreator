import Tkinter as tk
import Tkconstants, tkFileDialog
import numpy as np
import re, os, subprocess 
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import LogNorm
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



def get_xyz_from_csv_file(csv_file_path):
    '''
    get x, y, z value from csv file
    csv file format: x0,y0,z0
    '''
    x = []
    y = []
    z = []
    map_value = {}

    for line in open(csv_file_path):
        list = line.split(",")
        temp_x = float(list[0])
        temp_y = float(list[1])
        temp_z = float(list[2])
        x.append(temp_x)
        y.append(temp_y)
        z.append(temp_z)
        map_value[(temp_x, temp_y)] = temp_z

    return x, y, map_value    

  
        
def draw_heatmap(x, y, map_value, settings):
    """        
    draw heat map from input
    input: 
           x: list of X coordinate
           y: list of Y coordinate
    output:
          map_value: dict,  key is tuple (x,y), value is the value that will be displayed on the heat map    
    """    
    
    plt_x = np.asarray(list(set(x))) # for x y z format, x, y have duplicate, need to get unique value to create the x * y matrix  
    plt_y = np.asarray(list(set(y)))  
    plt_z = np.zeros(shape = (len(plt_x), len(plt_y)))
    
    for i in range(len(plt_x)):
        for j in range(len(plt_y)):
            if map_value.has_key((plt_x.item(i), plt_y.item(j))): 
                plt_z[i][j] = map_value[(plt_x.item(i), plt_y.item(j))]    
   
    z_min = plt_z.min()
    z_max = plt_z.max()
    plt_z = np.transpose(plt_z)    

    plot_name = settings.get("plot_name")
    

    color_map = plt.cm.gist_heat #plt.cm.rainbow #plt.cm.hot #plt.cm.gist_heat
    plt.pcolor(plt_x, plt_y, plt_z, cmap=color_map, vmin=z_min, vmax=z_max)
    plt.axis([plt_x.min(), plt_x.max(), plt_y.min(), plt_y.max()])
    plt.title(plot_name)
    plt.colorbar().set_label(plot_name, rotation=270)   
    ax = plt.gca()
    ax.set_aspect('equal')
    figure = plt.gcf()
    print figure
    return figure    
    




def quit_gui():
    root.quit()
    root.destroy()    


class HeatMapCreator:
    def __init__(self, master):
        self.master = master
        self.create_layout() 

    def create_layout(self):
        self.frame_left = tk.Frame(self.master)
        self.frame_right = tk.Frame(self.master)

        self.job_path_entry = tk.Entry(master = self.frame_left)
        self.job_path_entry.grid(row=1, column=0, sticky = tk.W)
        self.job_path_entry.insert(0, "input job path...")

        self.select_job_button = tk.Button(master = self.frame_left, text = "select job path", command = self.select_job_button_callback)
        self.select_job_button.grid(row = 2, column = 0, sticky = tk.W)

        self.create_heatmap_button = tk.Button(master = self.frame_left, text = "create heat map", command = self.create_heatmap_button_callback)
        self.create_heatmap_button.grid(row = 10,column = 0, sticky = tk.W)

        
        self.plot_name = tk.IntVar()
        self.runtime_ration_button = tk.Radiobutton(master = self.frame_left, text = "run time (seconds)", value = 1, variable = self.plot_name)
        self.runtime_ration_button.grid(row = 4, column = 0)
        
        self.memory_radio_button = tk.Radiobutton(master = self.frame_left, text = "memory usage (MB)", value = 2, variable = self.plot_name)
        self.memory_radio_button.grid(row = 5, column = 0)

        self.user_defined_radio_button = tk.Radiobutton(master = self.frame_left, text = "user define:", value = 3, variable = self.plot_name)
        self.user_defined_radio_button.grid(row = 6, column = 0)
        self.user_defined_input_entry = tk.Entry(master = self.frame_left)
        self.user_defined_input_entry.grid(row = 7, column = 0)




        

        self.frame_left.grid(row = 0, column = 0)
        self.frame_right.grid(row = 0, column = 1)

    def select_job_button_callback(self):
        #job_path = tkFileDialog.askdirectory()
        self.job_path = tkFileDialog.askopenfilename()
        self.job_path_entry.delete(0, tk.END)
        self.job_path_entry.insert(0, self.job_path)    
    
    def create_heatmap_button_callback(self):
        print "clicked create heat map button."
        self.job_path_string = self.job_path_entry.get()
        print "create heatmap from " + self.job_path_string       
        x, y, map_value = get_xyz_from_csv_file(self.job_path_string)

        settings = {}    
        if self.plot_name.get() == 1:
            settings["plot_name"] = "run time (seconds)"
        elif self.plot_name.get() == 2:
            settings["plot_name"] = "memory usage (MB)"
        elif self.plot_name.get() == 3:
            settings["plot_name"] = self.user_defined_input_entry.get()

        figure = draw_heatmap(x, y, map_value, settings)    
        canvas = FigureCanvasTkAgg(figure, master = self.frame_right)
        canvas.show()
        heatmap = canvas.get_tk_widget()
        heatmap.grid(row=1,column=1)

    

def main():
    global root
    root = tk.Tk()
    #root.title("Heat Map Creator ver0.12")    
    #gui_setup(root)    
    HeatMapCreator(root)
    
    tk.mainloop()  


if __name__ == "__main__":
    main() 

 










