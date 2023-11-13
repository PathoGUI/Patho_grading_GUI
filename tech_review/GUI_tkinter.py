import tkinter as tk
from tkinter import Label, Entry, StringVar, OptionMenu
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def clear_all():
    # Add code to clear the canvas or perform any other clearing actions
    pass

def save_and_next():
    # Add code to save data and move to the next step
    pass

# Create the main window
root = tk.Tk()

# Set the window title
root.title("PathoGUI")

# Set the window size
root.geometry("800x400")

# Create left and right frames
left_frame = tk.Frame(root)
right_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=10, pady=10)
right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

# Create a Matplotlib figure and canvas
fig = Figure(figsize=(5, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=left_frame)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Add a subplot to the Matplotlib figure
ax = fig.add_subplot(111)
ax.set_title('Pathology image')

# Remove axis labels
ax.set_xticks([])
ax.set_yticks([])

# Create Label-Entry pairs
label1 = Label(right_frame, text="x-coordinate:")
entry1 = Entry(right_frame)
label2 = Label(right_frame, text="y-coordinate:")
entry2 = Entry(right_frame)
label3 = Label(right_frame, text="annotation:")
entry3 = Entry(right_frame)

# Pack Label-Entry pairs
label1.grid(row=0, column=0, padx=10, pady=5)
entry1.grid(row=0, column=1, padx=10, pady=5)
label2.grid(row=1, column=0, padx=10, pady=5)
entry2.grid(row=1, column=1, padx=10, pady=5)
label3.grid(row=2, column=0, padx=10, pady=5)
entry3.grid(row=2, column=1, padx=10, pady=5)

# Create Label-OptionMenu pairs
label4 = Label(right_frame, text="Primary grade:")
var4 = StringVar()
options4 = ["3", "4", "5"]
option_menu4 = OptionMenu(right_frame, var4, *options4)

label5 = Label(right_frame, text="Secondary grade:")
var5 = StringVar()
options5 = ["3", "4", "5"]
option_menu5 = OptionMenu(right_frame, var5, *options5)

# Pack Label-OptionMenu pairs
label4.grid(row=3, column=0, padx=10, pady=5)
option_menu4.grid(row=3, column=1, padx=10, pady=5)
label5.grid(row=4, column=0, padx=10, pady=5)
option_menu5.grid(row=4, column=1, padx=10, pady=5)

# Create buttons in the right frame
clear_button = tk.Button(right_frame, text="Clear All", command=clear_all)
clear_button.grid(row=5, column=0, columnspan=2, pady=10)

save_next_button = tk.Button(right_frame, text="Save and Next", command=save_and_next)
save_next_button.grid(row=6, column=0, columnspan=2, pady=10)

# Run the Tkinter event loop
root.mainloop()
