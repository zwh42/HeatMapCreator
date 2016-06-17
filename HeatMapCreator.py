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

  
        
def draw_heatmap(x, y, map_value):
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



    plt.pcolor(plt_x, plt_y, plt_z, cmap=plt.cm.gist_heat, vmin=z_min, vmax=z_max)
    plt.axis([plt_x.min(), plt_x.max(), plt_y.min(), plt_y.max()])
    plt.title('heatmap')
    plt.colorbar().set_label("color bar", rotation=270)   
    #plt.show()
    figure = plt.gcf()
    print figure
    return figure    
    




def quit_gui():
    root.quit()
    root.destroy()
    
    
def select_job_button_callback():
    #job_path = tkFileDialog.askdirectory()
    job_path = tkFileDialog.askopenfilename()
    job_path_entry.delete(0, tk.END)
    job_path_entry.insert(0, job_path)



def create_heatmap_button_callback():
    print "clicked create heat map button."
    job_path_string = job_path_entry.get()
    print "create heatmap from " + job_path_string    
    
    x, y, map_value = get_xyz_from_csv_file(job_path_string)
    figure = draw_heatmap(x, y, map_value)

    canvas = FigureCanvasTkAgg(figure, master = root)
    canvas.show()
    heatmap = canvas.get_tk_widget()
    heatmap.grid(row=1,column=1)



def gui_setup(root):
    
    '''
    f = figure
    canvas = FigureCanvasTkAgg(f, master = root)
    canvas.show()
    '''
    global job_path_entry
    job_path_entry = tk.Entry(master = root)
    job_path_entry.grid(row=1, column=0, sticky = tk.W)
    job_path_entry.insert(0, "input job path")
    
    select_job_button = tk.Button(master = root, text = "select job path", command = select_job_button_callback)
    select_job_button.grid(row = 2, column = 0, sticky = tk.W)
    create_heatmap_button = tk.Button(master = root, text = "create heat map", command = create_heatmap_button_callback)
    create_heatmap_button.grid(row = 3,column = 0, sticky = tk.W)
    
    runtime_ration_button = tk.Radiobutton(master = root, text = "run time")
    runtime_ration_button.grid(row = 2, column = 2)
    memory_radio_button = tk.Radiobutton(master = root, text = "memory")
    memory_radio_button.grid(row = 3, column = 2)
    

    
    

def main():
    global root
    root = tk.Tk()    
    gui_setup(root)    
    tk.mainloop()  


if __name__ == "__main__":
    main() 

 










