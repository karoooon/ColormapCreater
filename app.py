import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils import create_tab  # ヘルパー関数
matplotlib.rcParams['font.family'] = 'MS Gothic'

class DualColormapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("カラーマップ表示（大きさと偏角）")
        self.colormaps = ['viridis', 'plasma', 'cividis', 'inferno', 'magma', 'jet']
        self.selected_colormap = tk.StringVar(value=self.colormaps[0])
        self.flip_x = False
        self.flip_y = False
        self.figures = {}
        self.axes = {}
        self.contours = {}
        self.slider_vars = {}
        self.create_controls()
        self.create_notebook()

    def create_controls(self):
        frame = tk.Frame(self.root)
        frame.pack(fill='x')
        tk.Label(frame, text="カラースケール:").pack(side='left')
        tk.OptionMenu(frame, self.selected_colormap, *self.colormaps,
                      command=self.update_colormap).pack(side='left')
        tk.Button(frame, text="上下反転", command=self.toggle_flip_y).pack(side='left', padx=5)
        tk.Button(frame, text="左右反転", command=self.toggle_flip_x).pack(side='left', padx=5)
        tk.Button(frame, text="ファイルを選択", command=self.load_files).pack(side='left', padx=5)
        tk.Button(frame, text="保存", command=self.save_current_plot).pack(side='left', padx=5)

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill='both')

    def load_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Excel files", "*.xlsx")])
        for file_path in file_paths:
            self.process_file(file_path)

    def process_file(self, file_path):
        df = pd.read_excel(file_path, engine='openpyxl')
        df.columns = ['X','Y','X_comp','Y_comp','Extra']
        df['Magnitude'] = np.sqrt(df['X_comp']**2 + df['Y_comp']**2)
        df['Arg'] = np.arctan2(df['Y_comp'], df['X_comp'])
        filename = file_path.split('/')[-1]
        for col,label in [('Magnitude','ベクトルの大きさ'), ('Arg','ベクトルの偏角')]:
            tab, ax, contour = create_tab(df, col, label, filename,
                                          self.selected_colormap.get(),
                                          self.flip_x, self.flip_y)
            self.notebook.add(tab, text=f"{filename} - {label}")
            min_var, max_var, Z, X, Y, canvas = tab.slider_vars
            self.figures[tab] = ax.figure
            self.axes[tab] = ax
            self.contours[tab] = contour
            self.slider_vars[tab] = (min_var, max_var, Z, X, Y, label, canvas)

    def update_colormap(self, cmap_name):
        for tab in self.axes:
            ax = self.axes[tab]
            min_var, max_var, Z, X, Y, label, canvas = self.slider_vars[tab]
            ax.contourf_obj.set_cmap(cmap_name)
            ax.colorbar.update_normal(ax.contourf_obj)
            ax.set_title(f"{label} ({cmap_name})")
            ax.figure.canvas.draw_idle()

    def toggle_flip_x(self):
        self.flip_x = not self.flip_x
        for ax in self.axes.values():
            ax.invert_xaxis()
            ax.figure.canvas.draw_idle()

    def toggle_flip_y(self):
        self.flip_y = not self.flip_y
        for ax in self.axes.values():
            ax.invert_yaxis()
            ax.figure.canvas.draw_idle()

    def save_current_plot(self):
        current_tab = self.notebook.select()
        fig = self.figures.get(self.root.nametowidget(current_tab))
        if fig:
            save_path = filedialog.asksaveasfilename(defaultextension='.png',
                                                     filetypes=[("PNG files","*.png")])
            if save_path:
                fig.savefig(save_path)
