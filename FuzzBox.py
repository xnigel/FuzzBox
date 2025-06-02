# ___/\\\\\\\\\\\\\\\____________________________________________/\\\\\\\\\\\\\_______________________________
#  __\/\\\///////////____________________________________________\/\\\/////////\\\_____________________________
#   __\/\\\_______________________________________________________\/\\\_______\/\\\_____________________________
#    __\/\\\\\\\\\\\______/\\\____/\\\__/\\\\\\\\\\\__/\\\\\\\\\\\_\/\\\\\\\\\\\\\\______/\\\\\_____/\\\____/\\\_
#     __\/\\\///////______\/\\\___\/\\\_\///////\\\/__\///////\\\/__\/\\\/////////\\\___/\\\///\\\__\///\\\/\\\/__
#      __\/\\\_____________\/\\\___\/\\\______/\\\/_________/\\\/____\/\\\_______\/\\\__/\\\__\//\\\___\///\\\/____
#       __\/\\\_____________\/\\\___\/\\\____/\\\/_________/\\\/______\/\\\_______\/\\\_\//\\\__/\\\_____/\\\/\\\___
#        __\/\\\_____________\//\\\\\\\\\___/\\\\\\\\\\\__/\\\\\\\\\\\_\/\\\\\\\\\\\\\/___\///\\\\\/____/\\\/\///\\\_
#         __\///_______________\/////////___\///////////__\///////////__\/////////////_______\/////_____\///____\///__
#          ___/\\\\\_____/\\\____________________________________/\\\\\\_______________________________________________
#           __\/\\\\\\___\/\\\___________________________________\////\\\_______________________________________________
#            __\/\\\/\\\__\/\\\__/\\\___/\\\\\\\\____________________\/\\\_______________________________________________
#             __\/\\\//\\\_\/\\\_\///___/\\\////\\\_____/\\\\\\\\_____\/\\\_______________________________________________
#              __\/\\\\//\\\\/\\\__/\\\_\//\\\\\\\\\___/\\\/////\\\____\/\\\_______________________________________________
#               __\/\\\_\//\\\/\\\_\/\\\__\///////\\\__/\\\\\\\\\\\_____\/\\\_______________________________________________
#                __\/\\\__\//\\\\\\_\/\\\__/\\_____\\\_\//\\///////______\/\\\_______________________________________________
#                 __\/\\\___\//\\\\\_\/\\\_\//\\\\\\\\___\//\\\\\\\\\\__/\\\\\\\\\____________________________________________
#                  __\///_____\/////__\///___\////////_____\//////////__\/////////_____________________________________________
# _______________________________________________________________________________________________________________________________________________________________

#   Initial version was built in July 2025                                       #
#                                                                                #
#   Version Number Defination:                                                   #
#   v00.00.01 2025.06.01                                                         #
#    -- -- --                                                                    #
#     |  |  |                                                                    #
#     |  |  +------     GUI Updates                                              #
#     |  +---------     Crypto Function Updates                                  #
#     +------------     Published Version (Major Change)                         #
#                                                                                #
# _______________________________________________________________________________#

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
Fuzz_ver = "00.04.01"
Fuzz_yr = "2025.06.02"
root.title('FuzzBox' + " (v" + Fuzz_ver +")")
root.geometry("496x480+200+200")
root.minsize(496, 480)
root.maxsize(496, 480)

# COM port selector
tk.Label(root, text="COM Port:").grid(row=0, column=0, sticky="W")
com_port_var = tk.StringVar()
com_ports = list_serial_ports()
com_port_menu = ttk.Combobox(root, textvariable=com_port_var, values=com_ports, state="readonly", width=10)
com_port_menu.grid(row=0, column=1, sticky="W")

# Baud rate selector
tk.Label(root, text="Baud Rate:").grid(row=1, column=0, sticky="W")
baud_rate_var = tk.StringVar(value="9600")
baud_rate_menu = ttk.Combobox(root, textvariable=baud_rate_var, values=["9600", "115200"], state="readonly", width=10)
baud_rate_menu.grid(row=1, column=1, sticky="W")

# Random byte length
tk.Label(root, text="RNG Length:").grid(row=2, column=0, sticky="W")
random_length_var = tk.StringVar(value="8")
random_length_entry = ttk.Entry(root, textvariable=random_length_var, width=13)
random_length_entry.grid(row=2, column=1, sticky="W")

# Package number
tk.Label(root, text="Package Number:").grid(row=3, column=0, sticky="W")
package_number_var = tk.StringVar(value="10")
package_number_entry = ttk.Entry(root, textvariable=package_number_var, width=13)
package_number_entry.grid(row=3, column=1, sticky="W")


# Start/Stop buttons
start_button = ttk.Button(root, text="Start Sending", command=start_sending)
start_button.grid(row=4, column=2, pady=2, sticky="e")

stop_button = ttk.Button(root, text="Stop Sending", command=stop_sending, state="disabled")
stop_button.grid(row=4, column=3, pady=2, sticky="e")

# Log display
log_text = tk.Text(root, height=22, width=60, state="normal")
log_text.grid(row=5, column=0, columnspan=4, padx=5, pady=2)

root.iconbitmap('NZ.ico') # adding NZ icon
root.mainloop()
