import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def redraw_contour(ax, Z, X, Y, cmap, vmin, vmax, label):
    if hasattr(ax,'contourf_obj'):
        ax.contourf_obj.set_array(Z.values.ravel())
        ax.contourf_obj.set_clim(vmin,vmax)
        ax.contourf_obj.set_cmap(cmap)
        ax.colorbar.update_normal(ax.contourf_obj)
        ax.figure.canvas.draw_idle()
        return ax.contourf_obj
    else:
        contour = ax.contourf(X,Y,Z,levels=100,cmap=cmap,vmin=vmin,vmax=vmax)
        cbar = ax.figure.colorbar(contour, ax=ax, label=label)
        ax.contourf_obj = contour
        ax.colorbar = cbar
        ax.figure.canvas.draw_idle()
        return contour

def create_tab(df, column, label, filename, cmap, flip_x, flip_y):
    x_unique = np.sort(df['X'].unique())
    y_unique = np.sort(df['Y'].unique())
    Z = df.pivot_table(index='Y',columns='X',values=column)
    Z = Z.reindex(index=y_unique, columns=x_unique)
    X,Y = np.meshgrid(x_unique, y_unique)
    fig, ax = plt.subplots()
    z_min, z_max = np.nanmin(Z.values), np.nanmax(Z.values)
    from utils import redraw_contour
    contour = redraw_contour(ax,Z,X,Y,cmap,z_min,z_max,label)
    ax.set_title(f"{label} - {filename} ({cmap})")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    if flip_x: ax.invert_xaxis()
    if flip_y: ax.invert_yaxis()

    tab = tk.Frame()
    canvas = FigureCanvasTkAgg(fig, master=tab)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

    slider_frame = tk.Frame(tab)
    slider_frame.pack(fill='x')
    min_var = tk.DoubleVar(value=z_min)
    max_var = tk.DoubleVar(value=z_max)

    # resolutionを0.001にして細かく調整可能
    def update_colorbar_range(*args):
        ax.contourf_obj.set_clim(min_var.get(), max_var.get())
        ax.colorbar.update_normal(ax.contourf_obj)
        ax.figure.canvas.draw_idle()

    tk.Label(slider_frame, text="最小値").pack(side='left')
    tk.Scale(slider_frame, from_=z_min, to=z_max, resolution=0.001,
             orient='horizontal', variable=min_var, command=update_colorbar_range).pack(side='left', fill='x', expand=True)
    tk.Label(slider_frame, text="最大値").pack(side='left')
    tk.Scale(slider_frame, from_=z_min, to=z_max, resolution=0.001,
             orient='horizontal', variable=max_var, command=update_colorbar_range).pack(side='left', fill='x', expand=True)

    tab.slider_vars = (min_var, max_var, Z, X, Y, canvas)
    return tab, ax, contour
