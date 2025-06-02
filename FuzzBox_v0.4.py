import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import random
import threading
import time

# Globals for controlling the sending loop
sending = False
send_thread = None

# Get available COM ports
def list_serial_ports():
    return [port.device for port in serial.tools.list_ports.comports()]

# Generate random hex bytes as a byte string and display string
def generate_random_hex_bytes(length):
    byte_list = [random.randint(0, 255) for _ in range(length)]
    hex_display = ' '.join(f"{b:02X}" for b in byte_list[:16]) + (' ...' if length > 16 else '')  # Limit display
    return bytes(byte_list), hex_display

# Sending loop function
def sending_loop():
    global sending
    port = com_port_var.get()
    baud = int(baud_rate_var.get())

    try:
        length = int(random_length_var.get())
        num_packets = int(package_number_var.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for byte length and package number.")
        sending = False
        return

    if not port:
        messagebox.showerror("Error", "Please select a COM port.")
        sending = False
        return

    try:
        with serial.Serial(port, baud, timeout=1) as ser:
            for i in range(num_packets):
                if not sending:
                    break
                data_bytes, display = generate_random_hex_bytes(length)
                ser.write(data_bytes)

                log_text.insert(tk.END, f"Packet {i+1}/{num_packets}: {display}\n")
                log_text.see(tk.END)

                time.sleep(1)  # Delay between sends
    except Exception as e:
        messagebox.showerror("Serial Error", str(e))
    finally:
        sending = False
        start_button.config(state="normal")
        stop_button.config(state="disabled")

# Start loop in background thread
def start_sending():
    global sending, send_thread
    if sending:
        return

    sending = True
    send_thread = threading.Thread(target=sending_loop, daemon=True)
    send_thread.start()
    start_button.config(state="disabled")
    stop_button.config(state="normal")

# Stop the loop
def stop_sending():
    global sending
    sending = False

# GUI setup
root = tk.Tk()
root.title("Auto Hex Sender via Serial")

# COM port selector
tk.Label(root, text="COM Port:").grid(row=0, column=0, sticky="e")
com_port_var = tk.StringVar()
com_ports = list_serial_ports()
com_port_menu = ttk.Combobox(root, textvariable=com_port_var, values=com_ports, state="readonly")
com_port_menu.grid(row=0, column=1)

# Baud rate selector
tk.Label(root, text="Baud Rate:").grid(row=1, column=0, sticky="e")
baud_rate_var = tk.StringVar(value="9600")
baud_rate_menu = ttk.Combobox(root, textvariable=baud_rate_var, values=["9600", "115200"], state="readonly")
baud_rate_menu.grid(row=1, column=1)

# Random byte length
tk.Label(root, text="Random Byte Length:").grid(row=2, column=0, sticky="e")
random_length_var = tk.StringVar(value="8")
random_length_entry = ttk.Entry(root, textvariable=random_length_var, width=10)
random_length_entry.grid(row=2, column=1)

# Package number
tk.Label(root, text="Package Number:").grid(row=3, column=0, sticky="e")
package_number_var = tk.StringVar(value="10")
package_number_entry = ttk.Entry(root, textvariable=package_number_var, width=10)
package_number_entry.grid(row=3, column=1)

# Start/Stop buttons
start_button = ttk.Button(root, text="Start Sending", command=start_sending)
start_button.grid(row=4, column=0, pady=10)

stop_button = ttk.Button(root, text="Stop Sending", command=stop_sending, state="disabled")
stop_button.grid(row=4, column=1, pady=10)

# Log display
log_text = tk.Text(root, height=15, width=60, state="normal")
log_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
