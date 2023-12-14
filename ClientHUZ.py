import socket
import json
import tkinter as tk
import PySimpleGUI as sg

# Function to update the GUI with the received values
def update_gui(volts, core_temp, cpu_freq, clock_speed, cpu_speed, iteration, mem_usage, disk_space):
    # Update labels with received values
    label_volts.config(text=f"Voltage: {volts}")
    label_core_temp.config(text=f"Core Temp: {core_temp}")
    label_cpu_freq.config(text=f"CPU Frequency: {cpu_freq}")
    label_clock_speed.config(text=f"Clock Speed: {clock_speed}")
    label_cpu_speed.config(text=f"CPU Speed: {cpu_speed}")
    label_iteration.config(text=f"Iteration: {iteration}")
    label_mem_usage.config(text=f"Memory Usage: {mem_usage}")
    label_disk_space.config(text=f"Disk Space: {disk_space}")

    # Toggle the LED every 2 seconds
    root.after(2000, toggle_led)

# Function to toggle the LED
def toggle_led():
    current_state = led_state.get()
    led_state.set(not current_state)

# Function to exit the application
def exit_application():
    try:
        # Close the socket
        sock.close()
    except:
        pass  # Ignore socket errors if already closed
    
    # Destroy the Tkinter window
    root.destroy()

# Server address and port
server_address = '192.168.0.141'
server_port = 5000

# Set PySimpleGUI theme
sg.theme('LightBrown4')

# Create the Tkinter window
root = tk.Tk()
root.title("Server Data")

# Create labels to display the values
label_volts = tk.Label(root, text="Voltage: N/A")
label_core_temp = tk.Label(root, text="Core Temp: N/A")
label_cpu_freq = tk.Label(root, text="CPU Frequency: N/A")
label_clock_speed = tk.Label(root, text="Clock Speed: N/A")
label_cpu_speed = tk.Label(root, text="CPU Speed: N/A")
label_iteration = tk.Label(root, text="Iteration: N/A")
label_mem_usage = tk.Label(root, text="Memory Usage: N/A")
label_disk_space = tk.Label(root, text="Disk Space: N/A")

# Variable to store LED state
led_state = tk.BooleanVar()
led_state.set(False)

# Create LED label with circular outline
led_label = tk.Label(root, text="○", font=("Arial", 20), background="red", textvariable=led_state)
led_label.pack()

# Create Exit button
exit_button = tk.Button(root, text="Exit", command=exit_application)
exit_button.pack()

# Place the labels in the window
label_volts.pack()
label_core_temp.pack()
label_cpu_freq.pack()
label_clock_speed.pack()
label_cpu_speed.pack()
label_iteration.pack()
label_mem_usage.pack()
label_disk_space.pack()

try:
    # Create a socket and connect to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_address, server_port))
    print("Connected to the server")

    iteration_count = 0  # Initialize iteration count

    while True:
        # Receive data from the server
        json_received = sock.recv(1024)
        if not json_received:
            break

        # Decode JSON data
        data = json.loads(json_received.decode('utf-8'))

        # Extract values from the received data
        volts = data.get("volts", "N/A")
        core_temp = data.get("temp-core", "N/A")
        cpu_freq = data.get("cpu-freq", "N/A")
        clock_speed = data.get("clock_speed", "N/A")
        cpu_speed = data.get("cpu_speed", "N/A")
        iteration = data.get("it", "N/A")
        mem_usage = data.get("memory-usage", "N/A")
        disk_space = data.get("disk-space", "N/A")

        # Print received values to console
        print("Received values - Voltage:", volts, "Core Temp:", core_temp, "CPU Frequency:", cpu_freq, "Clock Speed:", clock_speed, "CPU Speed:", cpu_speed, "Iteration:", iteration, "Memory Usage:", mem_usage, "Disk Space:", disk_space)

        # Update the GUI with the received values
        update_gui(volts, core_temp, cpu_freq, clock_speed, cpu_speed, iteration, mem_usage, disk_space)

        # Update iteration count
        iteration_count += 1
        label_iteration.config(text=f"Iteration: {iteration_count}")

        # Update the Tkinter window
        root.update()

except socket.error as err:
    print('Socket error because of %s' % (err))
finally:
    print("Lost connection with the server")
    # Close the socket (in case it's not closed)
    try:
        sock.close()
    except:
        pass
    # Destroy the Tkinter window
    root.destroy()

# Start the Tkinter event loop
root.mainloop()

