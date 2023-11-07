import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import csv

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("ROI Preview")

        self.figure = plt.figure()
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=3, rowspan=5, sticky="nsew")

        self.current_channel = "Cyto"

        # Buttons to switch between channels
        self.cyto_button = ttk.Button(root, text="Cyto", command=self.switch_channel("Cyto"))
        self.nuc_button = ttk.Button(root, text="Nuc", command=self.switch_channel("Nuc"))
        self.target_button = ttk.Button(root, text="Target", command=self.switch_channel("Target"))
        self.cyto_button.grid(row=5, column=0)
        self.nuc_button.grid(row=5, column=1)
        self.target_button.grid(row=5, column=2)

        # Entry widgets to display coordinates and array shape
        self.x_coordinate_textbox = ttk.Entry(root, state="readonly")
        self.y_coordinate_textbox = ttk.Entry(root, state="readonly")
        self.arrayshape_textbox = ttk.Entry(root, state="readonly")
        self.current_z_level_textbox = ttk.Entry(root, state="readonly")

        self.x_coordinate_textbox.grid(row=6, column=0, columnspan=3, sticky="ew")
        self.y_coordinate_textbox.grid(row=7, column=0, columnspan=3, sticky="ew")
        self.arrayshape_textbox.grid(row=8, column=0, columnspan=3, sticky="ew")
        self.current_z_level_textbox.grid(row=9, column=0, columnspan=3, sticky="ew")

        # Contrast enhancement settings
        self.ClipHighLim_cyto = ttk.Spinbox(root, from_=0, to=4500, increment=50, value=1200)
        self.ClipLowLim_cyto = ttk.Spinbox(root, from_=0, to=4500, increment=50, value=0)
        self.ClipHighLim_nuc = ttk.Spinbox(root, from_=0, to=4500, increment=50, value=2000)
        self.ClipLowLim_nuc = ttk.Spinbox(root, from_=0, to=4500, increment=50, value=0)
        self.ClipHighLim_pgp = ttk.Spinbox(root, from_=0, to=4500, increment=50, value=700)
        self.ClipLowLim_pgp = ttk.Spinbox(root, from_=0, to=4500, increment=50, value=0)

        self.ClipHighLim_cyto.grid(row=10, column=0)
        self.ClipLowLim_cyto.grid(row=11, column=0)
        self.ClipHighLim_nuc.grid(row=10, column=1)
        self.ClipLowLim_nuc.grid(row=11, column=1)
        self.ClipHighLim_pgp.grid(row=10, column=2)
        self.ClipLowLim_pgp.grid(row=11, column=2)

        self.dropdown1 = ttk.Combobox(root, values=["Rescale", "CLAHE"])
        self.dropdown1.set("Rescale")
        self.dropdown2 = ttk.Combobox(root, values=["Rescale", "CLAHE"])
        self.dropdown2.set("Rescale")
        self.dropdown3 = ttk.Combobox(root, values=["Rescale", "CLAHE"])
        self.dropdown3.set("Rescale")

        self.dropdown1.grid(row=12, column=0)
        self.dropdown2.grid(row=12, column=1)
        self.dropdown3.grid(row=12, column=2)

        # Buttons
        save_button = ttk.Button(root, text="Save Params", command=self.save_coords)
        home_button = ttk.Button(root, text="Home", command=self.show_entire_image)

        save_button.grid(row=13, column=0)
        home_button.grid(row=13, column=1)

    def switch_channel(self, channel):
        def callback():
            self.current_channel = channel
            # Add logic to update the display based on the selected channel

        return callback

    def save_coords(self):
        shape = self.arrayshape_textbox.get()
        currentZ = self.current_z_level_textbox.get()
        nuc_cliplow = self.ClipLowLim_nuc.get()
        nuc_ctehmt_method = self.dropdown1.get()
        filename = "ROI_coords_.csv"
        headers = ["Shape", "Current Z level", "nuc clip", "nuc CE method"]
        values = [shape, currentZ, nuc_cliplow, nuc_ctehmt_method]
        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(headers)
            writer.writerow(values)

    def show_entire_image(self):
        # Add logic to show the entire image
        pass

root = tk.Tk()
app = MainWindow(root)
root.mainloop()
