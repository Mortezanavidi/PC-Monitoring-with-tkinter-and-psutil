"""
Example script for testing the Azure theme
Author: rdbende
License: GNU GPLv2.1
"""

# Importing the libraries
import psutil
import time
import platform
import tkinter as tk
from tkinter import ttk
from threading import *
import socket

# Create the window
root = tk.Tk()
root.title('Personal Computer Monitoring')
root.resizable(False, False)

# Place the window in the center of the screen
windowWidth = 800
windowHeight = 530
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
xCordinate = int((screenWidth/2) - (windowWidth/2))
yCordinate = int((screenHeight/2) - (windowHeight/2))
root.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, xCordinate, yCordinate))

# Create a style
style = ttk.Style(root)

# Import the tcl file
root.tk.call('source', 'azure-dark.tcl')

# Set the theme with the theme_use method
style.theme_use('azure-dark')


# Threads
def resource_threading():
    a1 = Thread(target=cpu_usage)
    a1.start()

    a2 = Thread(target=ram_usage)
    a2.start()

    a3 = Thread(target=hd_usage)
    a3.start()

    a4 = Thread(target=os_version)
    a4.start()

    a5 = Thread(target=project_version)
    a5.start()

    a6 = Thread(target=pc_status)
    a6.start()

    a7 = Thread(target=open_processes)
    a7.start()


# Functions
def homepage():
    homepage_frame.place(x=165, y=12)
    server_frame.place_forget()


def server():
    server_frame.place(x=165, y=12)
    homepage_frame.place_forget()
    resource_threading()


def cpu_usage():
    while True:
        cpu_percent_label['text'] = str(psutil.cpu_percent()) + "%"
        cpu_progress['value'] = psutil.cpu_percent()
        time.sleep(0.5)


def ram_usage():
    while True:
        ram_percent_label['text'] = str(psutil.virtual_memory()[2]) + "%"
        ram_progress['value'] = psutil.virtual_memory()[2]
        time.sleep(0.5)


def hd_usage():
    while True:
        hd_percent_label['text'] = str(psutil.disk_usage('/')).rsplit(',', 1)[1].strip(' percent=)') + "%"
        hd_progress['value'] = str(psutil.disk_usage('/')).rsplit(',', 1)[1].strip(' percent=)')
        time.sleep(0.5)


def os_version():
    os_label_txt['text'] = str(platform.uname()).rsplit(',', 4)[0].strip("uname_result(system=") + " " + str(platform.uname()).rsplit(',', 3)[1].strip(" release=)")


def project_version():
    project_version_txt['text'] = "1.0.0"


def pc_status():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        sock = socket.create_connection(("www.google.com", 80))
        if sock is not None:
            global status
            status = "online"
            project_status_label_txt['text'] = "online"
            project_status_label_txt['foreground'] = "green"
        return True
    except OSError:
        status = "offline"
        project_status_label_txt['text'] = "offline"
        project_status_label_txt['foreground'] = "red"
    return False


def open_processes():
    for proc in psutil.process_iter():
        open_processes_list.insert(0, f" {proc.name()}")
        open_processes_list.insert(1, "─────────")


def refresher():
    for proc_delete in psutil.process_iter():
        open_processes_list.delete(0, "end")
        open_processes()
        pc_status()


def printer():
    file = open("../output.txt", "w+")
    file.write("Monitor Project Output \n   -----------------")
    file.write("\n" "OS: " + str(platform.uname()).rsplit(',', 4)[0].strip("uname_result(system=") + " " + str(platform.uname()).rsplit(',', 3)[1].strip(" release=)"))
    file.write("\nProject version: 1.0.0")
    file.write(f"\nInternet Connection Status: {status}")
    file.write("\n   -----------------")
    file.write(f"\nCpu usage was: {psutil.cpu_percent(1)} %")
    file.write(f"\nRam usage was: {psutil.virtual_memory()[2]} %")
    file.write("\nDisk usage was: " + str(psutil.disk_usage('/')).rsplit(',', 1)[1].strip(' percent=)') + " %")
    file.write("\n   -----------------")
    file.write("\nOpen Processes: ")
    for proc in psutil.process_iter():
        file.write(f"\n   {proc.name()}")
        file.write("\n   -----------------")




# Left Sidebar Frame
left_sidebar_frame = ttk.LabelFrame(root, text='Menu', width=140, height=505)
left_sidebar_frame.place(x=15, y=12)

# Left Sidebar  Buttons
homepage = ttk.Button(root, text='Home Page', style='AccentButton', command=homepage)
homepage.place(x=40, y=40)

server = ttk.Button(root, text='Server', style='AccentButton', command=server)
server.place(x=40, y=90)

# Server Window
server_frame = ttk.LabelFrame(root, text='Server', width=620, height=505)
server_frame.place(x=165, y=12)

# CPU Label
cpu_label = ttk.Label(server_frame, text='CPU Usage: ')
cpu_label.place(x=30, y=25)

# CPU Label Percent
cpu_percent_label = ttk.Label(server_frame, text='')
cpu_percent_label.place(x=210, y=25)

# CPU Progressbar
cpu_progress = ttk.Progressbar(server_frame, length=100, mode='determinate')
cpu_progress.place(x=100, y=25)

# RAM Label
ram_label = ttk.Label(server_frame, text='RAM Usage: ')
ram_label.place(x=30, y=55)

# RAM Label Percent
ram_percent_label = ttk.Label(server_frame, text='')
ram_percent_label.place(x=210, y=55)

# RAM Progressbar
ram_progress = ttk.Progressbar(server_frame, length=100, mode='determinate')
ram_progress.place(x=100, y=55)

# Hard Disk Label
hd_label = ttk.Label(server_frame, text='DISK Usage: ')
hd_label.place(x=30, y=85)

# Hard Disk Label Percent
hd_percent_label = ttk.Label(server_frame, text='')
hd_percent_label.place(x=210, y=85)

# Hard Disk Progressbar
hd_progress = ttk.Progressbar(server_frame, length=100, mode='determinate')
hd_progress.place(x=100, y=85)

# Separators
separator = ttk.Separator(server_frame, orient='horizontal')
separator.place(x=30, y=130, width=560)

separator1 = ttk.Separator(server_frame, orient='vertical')
separator1.place(x=280, y=15, height=100)

separator2 = ttk.Separator(server_frame, orient='vertical')
separator2.place(x=280, y=150, height=323)

# OS
os_label = ttk.Label(server_frame, text='OS: ')
os_label.place(x=300, y=25)

os_label_txt = ttk.Label(server_frame)
os_label_txt.place(x=325, y=25)

# Project Version
project_version_label = ttk.Label(server_frame, text='Version: ')
project_version_label.place(x=300, y=55)

project_version_txt = ttk.Label(server_frame)
project_version_txt.place(x=345, y=55)

# Project Status
project_status_label = ttk.Label(server_frame, text='Internet Status: ')
project_status_label.place(x=300, y=85)

project_status_label_txt = ttk.Label(server_frame)
project_status_label_txt.place(x=385, y=85)

# Open Processes
open_processes_list = tk.Listbox(server_frame, height=20, width=35, selectmode='extended')
open_processes_list.place(x=30, y=150)

# Open Processes Button
open_processes_list_button = ttk.Button(server_frame, text='Refresh', style='AccentButton', command=refresher)
open_processes_list_button.place(x=300, y=150)

# Print Button
print_button = ttk.Button(server_frame, text='Print', style='AccentButton', command=printer)
print_button.place(x=300, y=200)

# Homepage Window
homepage_frame = ttk.LabelFrame(root, text='Home', width=620, height=505)
homepage_frame.place(x=165, y=12)

root.mainloop()