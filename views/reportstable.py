from .tables import createTable,createTableMatPlot
from tkinter import *

import tkinter as tk
from tkinter import ttk


class DoubleScrollbarFrame(ttk.Frame):

  def __init__(self, master, **kwargs):
    '''
      Initialisation. The DoubleScrollbarFrame consist of :
        - an horizontal scrollbar
        - a  vertical   scrollbar
        - a canvas in which the user can place sub-elements
    '''

    ttk.Frame.__init__(self,  master, **kwargs)

    # Canvas creation with double scrollbar
    self.hscrollbar = ttk.Scrollbar(self, orient = tk.HORIZONTAL)
    self.vscrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL)
    self.sizegrip = ttk.Sizegrip(self)
    self.canvas = tk.Canvas(self, bd=0, highlightthickness=0, 
                                  yscrollcommand = self.vscrollbar.set,
                                  xscrollcommand = self.hscrollbar.set)
    self.vscrollbar.config(command = self.canvas.yview)
    self.hscrollbar.config(command = self.canvas.xview)

  def pack(self, **kwargs):
    '''
      Pack the scrollbar and canvas correctly in order to recreate the same look as MFC's windows. 
    '''

    self.hscrollbar.pack(side=tk.BOTTOM, fill=tk.X, expand=tk.FALSE)
    self.vscrollbar.pack(side=tk.RIGHT, fill=tk.Y,  expand=tk.FALSE)
    self.sizegrip.pack(in_ = self.hscrollbar, side = tk.BOTTOM, anchor = "se")
    self.canvas.pack(side=tk.LEFT, padx=5, pady=5,
                                             fill=tk.BOTH, expand=tk.TRUE)

    ttk.Frame.pack(self, **kwargs)
    


  def get_frame(self):
    '''
      Return the "frame" useful to place inner controls.
    '''
    return self.canvas


class ReportsTable:
    def __init__(self, master,datalist):
        
        frame = createTable(master,datalist)
        frame.pack()
        

def renderTable(datalist):
    root = Tk()
    s = ReportsTable(root,datalist)
    root.mainloop()

def renderMatPlot(datalist):
    createTableMatPlot(datalist)