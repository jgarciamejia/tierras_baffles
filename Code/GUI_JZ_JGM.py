"""
Sep 21 2021 

GUI Tkinter Program to Display Load Sensor Data on the screen

"""
import tkinter as tk
from tkinter import ttk
import tkinter.ttk

# Define global variables 
global Upper_North
global Upper_South
global Upper_East
global Upper_West
global Lower_North
global Lower_South
global Lower_East
global Lower_West

# Configure GUI 

root = tk.Tk()
root.geometry("630x400")
root.title("TIERRAS OBSERVATORY")
stl = ttk.Style()

stl.configure('.', font=('Helvetica',12), background='antique white')
stl.map('C.TButton', foreground=[('pressed','red'),('active','blue')])

stl.configure('T1.TLabel', foreground='green')
stl.configure('T2.TLabel', foreground='blue')

#stl.configure('C.TButton', foreground=[('pressed','red'),('active','blue')])
stl.configure('C2.TEntry', foreground='red', background='teal', font=('Helvetica',18))

mainframe = tk.ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

Upper_North = tk.DoubleVar()
Upper_South = tk.DoubleVar()
Upper_East = tk.DoubleVar()
Upper_West = tk.DoubleVar()
Lower_North = tk.DoubleVar()
Lower_South = tk.DoubleVar()
Lower_East = tk.DoubleVar()
Lower_West = tk.DoubleVar()


tk.ttk.Label(mainframe, text="TIERRAS OBSERVATORY", style="T1.TLabel", font=('Helvetica', 50, 'bold'), foreground='darkslategrey').grid(columnspan=10, row=1)

cablefont = ('Helvetica', 40)
cabletxtcolor = 'darkslategrey'
tk.ttk.Label(mainframe, text="Upper Cables", style="T1.TLabel", font=cablefont, foreground=cabletxtcolor).grid(column=2, row=2)
tk.ttk.Label(mainframe, text="Lower Cables", style="T1.TLabel", font=cablefont, foreground=cabletxtcolor).grid(column=3, row=2)

tk.ttk.Separator(mainframe, orient=tk.HORIZONTAL).grid(row=3,columnspan=15,ipadx=0, sticky=tk.NSEW)

cardinalfont = ('Helvetica', 40)
cardinaltxtcolor = 'darkslategrey'
tk.ttk.Label(mainframe, text="N", style="T1.TLabel", font=cardinalfont, foreground=cardinaltxtcolor).grid(column=1, row=4)
tk.ttk.Label(mainframe, text="S", style="T1.TLabel", font=cardinalfont, foreground=cardinaltxtcolor).grid(column=1, row=5)
tk.ttk.Label(mainframe, text="E", style="T1.TLabel", font=cardinalfont, foreground=cardinaltxtcolor).grid(column=1, row=6)
tk.ttk.Label(mainframe, text="W", style="T1.TLabel", font=cardinalfont, foreground=cardinaltxtcolor).grid(column=1, row=7)
#tk.ttk.Button(mainframe, text="QUIT",style='C.TButton',command=exit).grid(column=3, row=10, sticky=tk.W)

loadreadingfont = ('Helvetica', 40)
loadreadingtxtcolor = 'white'
loadrdngbgcolor = 'white'
Upper_North_Entry = tk.ttk.Entry(mainframe, width=3, textvariable=Upper_North, style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Upper_South_Entry = tk.ttk.Entry(mainframe, width=3, textvariable=Upper_South, style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Upper_East_Entry =  tk.ttk.Entry(mainframe, width=3, textvariable=Upper_East,  style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Upper_West_Entry =  tk.ttk.Entry(mainframe, width=3, textvariable=Upper_West,  style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Lower_North_Entry = tk.ttk.Entry(mainframe, width=3, textvariable=Lower_North, style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Lower_South_Entry = tk.ttk.Entry(mainframe, width=3, textvariable=Lower_South, style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Lower_East_Entry =  tk.ttk.Entry(mainframe, width=3, textvariable=Lower_East,  style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Lower_West_Entry =  tk.ttk.Entry(mainframe, width=3, textvariable=Lower_West,  style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)

Upper_North_Entry.grid(column=2, row=4, sticky=(tk.W, tk.E))
Upper_South_Entry.grid(column=2, row=5, sticky=(tk.W, tk.E))
Upper_East_Entry.grid( column=2, row=6, sticky=(tk.W, tk.E))
Upper_West_Entry.grid( column=2, row=7, sticky=(tk.W, tk.E))
Lower_North_Entry.grid(column=3, row=4, sticky=(tk.W, tk.E))
Lower_South_Entry.grid(column=3, row=5, sticky=(tk.W, tk.E))
Lower_East_Entry.grid( column=3, row=6, sticky=(tk.W, tk.E))
Lower_West_Entry.grid( column=3, row=7, sticky=(tk.W, tk.E))




