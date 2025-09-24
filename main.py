import sys
import tkinter as tk
from app import DualColormapApp
import matplotlib.pyplot as plt

root = tk.Tk()
root.state('zoomed')
app = DualColormapApp(root)

def on_close():
    plt.close('all')
    root.destroy()
    sys.exit()

root.protocol("WM_DELETE_WINDOW", on_close)
root.bind("<Escape>", lambda event: root.state('normal'))
root.mainloop()

