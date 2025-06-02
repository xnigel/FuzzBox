import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import random
import string

# Function to get available COM ports
def list_serial_ports():
    return [port.device for port in serial.tools.list_ports.comports()]

# Send data to serial port
def send_to_serial(data):
    port = com_port_var.get()
    baud = int(baud_rate_var.get())
    if not port:
        messagebox.showerror("Error", "Please select a COM port.")
        return

    try:
        with serial.Serial(port, baud, timeout=1) as ser:
            ser.write(data.encode('ascii'))
            messagebox.showinfo("Success", f"Sent: {data}")
    except Exception as e:
        messagebox.showerror("Serial Error", str(e))

# Generate random ASCII characters
def generate_random_ascii():
    length = int(random_length_var.get())
    result = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))
    message_entry.delete(0, tk.END)
    message_entry.insert(0, result)

# GUI Setup
root = tk.Tk()
root.title("ASCII Sender via Serial")

# COM port selector
tk.Label(root, text="COM Port:").grid(row=0, column=0, sticky="e")
com_port_var = tk.StringVar()
com_ports = list_serial_ports()
com_port_menu = ttk.Combobox(root, textvariable=com_port_var, values=com_ports)
com_port_menu.grid(row=0, column=1)

# Baud rate selector
tk.Label(root, text="Baud Rate:").grid(row=1, column=0, sticky="e")
baud_rate_var = tk.StringVar(value="9600")
baud_rate_entry = ttk.Entry(root, textvariable=baud_rate_var)
baud_rate_entry.grid(row=1, column=1)

# Message entry
tk.Label(root, text="ASCII Message:").grid(row=2, column=0, sticky="e")
message_entry = ttk.Entry(root, width=40)
message_entry.grid(row=2, column=1, columnspan=2)

# Random ASCII generation
tk.Label(root, text="Random Length:").grid(row=3, column=0, sticky="e")
random_length_var = tk.StringVar(value="8")
random_length_entry = ttk.Entry(root, textvariable=random_length_var, width=5)
random_length_entry.grid(row=3, column=1, sticky="w")
generate_button = ttk.Button(root, text="Generate Random", command=generate_random_ascii)
generate_button.grid(row=3, column=2, sticky="w")

# Send button
send_button = ttk.Button(root, text="Send to Serial", command=lambda: send_to_serial(message_entry.get()))
send_button.grid(row=4, column=1, pady=10)

root.mainloop()
