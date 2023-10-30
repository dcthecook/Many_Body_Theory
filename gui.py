# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 02:27:52 2023

@author: Enea
"""
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
plt.style.use('dark_background')
import tkinter as tk
import time
import numpy as np
from tkinter import scrolledtext
import tkinter.filedialog as filedialog
import config

def main():
    ###########
    ###########
    # Create the main window
    ###########
    ###########
    root = tk.Tk()
    root.title("Quantum Sail ver1.0")
    root.geometry("1880x1250")
    
    
    
    ############
    ############
    # Create the central plot from TkAgg and matplotlib's backend
    ############
    ############
    fig, ax = plt.subplots(figsize=(12,12))
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()
    canvas.get_tk_widget().place(x=200, y=0)
    
    
    ############
    ############
    # Area on the Right for Output Prompt. Uses tkinters Scrolledtext module
    ############
    ############
    text_area_frame = tk.Frame(root)
    text_area_frame.place(x=1401, y=0, width=470, height=1000)
    text_area = scrolledtext.ScrolledText(text_area_frame, wrap=tk.WORD)
    text_area.pack(expand=1, fill='both', anchor='nw')
    default_text = "Welcome!\n.    .    .    .    .    .    .    .    .    .    .    .\n.    .    .    .    .    .    .    .    .    .    .    .\n~~~~~~~~~~\n"
    text_area.insert(tk.INSERT, default_text)
    
    ############
    ############
    # Chose the Model you want to compute
    ############
    ############

    # Create a variable to store the selected model scheme
    model_var = tk.StringVar()
    model_var.set(config.model)  # Set the default model scheme which is model = 'Bose-Hubbard'

    # Create the OptionMenu widget
    model_option_menu = tk.OptionMenu(root, model_var, *config.models)
    model_option_menu.pack(anchor='nw')

    # Configure the width of the OptionMenu button
    model_option_menu.config(width=25)  # Adjust the width as needed

    # Attach a trace to update the model
    model_var.trace("w", update_model)