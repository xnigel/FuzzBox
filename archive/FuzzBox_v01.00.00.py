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
# _______________________________________________________________________________#
#   0. Fuzzer was created in June 2025 - 00.00.01 - 00.04.01                     #
#   1. Adding headers and checksum --- on going 2025.07.23 - v00.05.01           #
#   2. Released the final version  --- on going 2025.07.23 - v01.00.00           #
#                                                                                #
# _______________________________________________________________________________#

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import serial
import serial.tools.list_ports
import random
import time
import threading
import binascii
import crcmod.predefined # For CRC-8 and CRC-16


class SerialFuzzTool:
    def __init__(self, master):
        self.master = master
        Fuzz_ver = "01.00.00"
        Fuzz_yr = "2025.07.23"
        master.title("FuzzBox" + " (v" + Fuzz_ver +")" + " - " + Fuzz_yr + " - nigel.zhai@ul.com")
        master.geometry("560x750+200+200") # Set initial window size
        master.minsize(560, 750) # Set minimum window size
        master.maxsize(560, 750) # Set maximum window size

        self.ser = None # Serial port object
        self.fuzzing_active = False
        self.fuzz_thread = None

        # --- Character Ranges for Fuzzing ---
        self.CHAR_RANGES = {
            "Random Hex (0x00-0xFF)": list(range(0x00, 0x100)),
            "Numbers (0-9)": list(range(0x30, 0x3A)), # ASCII 0-9
            "Uppercase Letters (A-Z)": list(range(0x41, 0x5B)), # ASCII A-Z
            "Lowercase Letters (a-z)": list(range(0x61, 0x7B)), # ASCII a-z
            "Symbols (!-/ :@)": list(range(0x21, 0x30)) + list(range(0x3A, 0x41)), # ASCII !-/ and :@
            "Invisible Chars (0x00-0x20)": list(range(0x00, 0x21)) # ASCII NUL-SPACE
        }

        # --- GUI Setup ---
        self.create_widgets()

    def create_widgets(self):
        # --- Top Section Container Frame (Serial Port and Fuzzing Controls) ---
        top_section_frame = ttk.Frame(self.master)
        top_section_frame.pack(padx=10, pady=2, fill="x")

        # --- Serial Port Configuration Frame ---
        serial_frame = ttk.LabelFrame(top_section_frame, text="Serial Port Configuration")
        serial_frame.grid(row=0, column=0, padx=5, pady=2, sticky="nsew")

        ttk.Label(serial_frame, text="Port:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.port_combobox = ttk.Combobox(serial_frame, width=10) # Adjusted width
        self.port_combobox.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        self.refresh_ports()
        ttk.Button(serial_frame, text="Refresh Ports", width=15, command=self.refresh_ports).grid(row=0, column=2, padx=5, pady=2)

        ttk.Label(serial_frame, text="Baud Rate:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.baudrate_combobox = ttk.Combobox(serial_frame, values=[
            "9600", "19200", "38400", "57600", "115200", "230400", "460800", "921600"
        ], width=10) # Adjusted width
        self.baudrate_combobox.set("115200")
        self.baudrate_combobox.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(serial_frame, text="Data Bits:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.databits_combobox = ttk.Combobox(serial_frame, values=["5", "6", "7", "8"], width=5)
        self.databits_combobox.set("8")
        self.databits_combobox.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(serial_frame, text="Parity:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
        self.parity_combobox = ttk.Combobox(serial_frame, values=["N", "E", "O", "M", "S"], width=5)
        self.parity_combobox.set("N")
        self.parity_combobox.grid(row=3, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(serial_frame, text="Stop Bits:").grid(row=4, column=0, padx=5, pady=2, sticky="w")
        self.stopbits_combobox = ttk.Combobox(serial_frame, values=["1", "1.5", "2"], width=5)
        self.stopbits_combobox.set("1")
        self.stopbits_combobox.grid(row=4, column=1, padx=5, pady=2, sticky="ew")

        self.connect_button = ttk.Button(serial_frame, text="Connect", width=15, command=self.connect_serial)
        self.connect_button.grid(row=1, column=2, rowspan=2, padx=10, pady=2, sticky="ns")
        self.disconnect_button = ttk.Button(serial_frame, text="Disconnect", width=15, command=self.disconnect_serial, state=tk.DISABLED)
        self.disconnect_button.grid(row=3, column=2, rowspan=2, padx=10, pady=2, sticky="ns")

        serial_frame.grid_columnconfigure(1, weight=1) # Allow port/baudrate combobox to expand
        serial_frame.grid_columnconfigure(2, weight=0) # Keep Refresh button fixed
        serial_frame.grid_columnconfigure(3, weight=0) # Keep Connect/Disconnect buttons fixed


        # --- Fuzzing Controls Frame ---
        control_frame = ttk.LabelFrame(top_section_frame, text="Fuzzing Controls")
        control_frame.grid(row=0, column=1, padx=5, pady=2, sticky="nsew")

        ttk.Label(control_frame, text="Interval (ms):").grid(row=0, column=0, padx=10, pady=2, sticky="w")
        self.interval_entry = ttk.Entry(control_frame, width=8) # Adjusted width
        self.interval_entry.insert(0, "10")
        vcmd_float = (self.master.register(self.validate_float), '%P')
        self.interval_entry.config(validate="key", validatecommand=vcmd_float)
        self.interval_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=2, sticky="ew")

        ttk.Label(control_frame, text="Loops (0=infinite):").grid(row=1, column=0, padx=10, pady=2, sticky="w")
        self.iterations_entry = ttk.Entry(control_frame, width=8) # Adjusted width
        self.iterations_entry.insert(0, "0")
        vcmd_int = (self.master.register(self.validate_int), '%P')
        self.iterations_entry.config(validate="key", validatecommand=vcmd_int)
        self.iterations_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=2, sticky="ew")

        # Define a style for the stop button
        style = ttk.Style()
        style.configure("Green.TButton", background="green") # Set background and text color
        style.configure("Yellow.TButton", background="yellow") # Set background and text color
        style.configure("Red.TButton", background="red") # Set background and text color
        # You might need to map the style to a specific theme element if "background" doesn't work directly on some OS/themes
        # style.map("Red.TButton", background=[('active', 'darkred'), ('!disabled', 'red')])

        self.send_single_button = ttk.Button(control_frame, text="Try 1 Packet", width=15, command=self.send_single_packet, style="Yellow.TButton")
        self.send_single_button.grid(row=2, column=0, padx=5, pady=2, sticky="wns") # Spans two columns

        self.start_fuzz_button = ttk.Button(control_frame, text="Go! Fuzzing", width=15, command=self.start_fuzzing, style="Green.TButton")
        self.start_fuzz_button.grid(row=2, column=1, rowspan=2, columnspan=2, padx=5, pady=5, sticky="ns") # Spans two columns
        self.stop_fuzz_button = ttk.Button(control_frame, text="Stop!", width=15, command=self.stop_fuzzing, state=tk.DISABLED, style="Red.TButton")
        self.stop_fuzz_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="wns") # Spans two columns

        control_frame.grid_columnconfigure(1, weight=1) # Allow entry fields to expand

        # Configure top_section_frame columns to expand
        top_section_frame.grid_columnconfigure(0, weight=1)
        top_section_frame.grid_columnconfigure(1, weight=1)


        # --- Middle Section Container Frame (Field Config and Checksum) ---
        middle_section_frame = ttk.Frame(self.master)
        middle_section_frame.pack(padx=10, pady=2, fill="both", expand=True)

        # --- Field Configuration Frame ---
        fields_frame = ttk.LabelFrame(middle_section_frame, text="Field Configuration (Up to 10 Fields)")
        fields_frame.grid(row=0, column=0, padx=5, pady=2, sticky="nsew")

        self.field_types = []
        self.field_lengths = []
        self.field_checkboxes = []

        # Header row for fields
        ttk.Label(fields_frame, text="Enable").grid(row=0, column=0, padx=2, pady=2)
        ttk.Label(fields_frame, text="Field #").grid(row=0, column=1, padx=2, pady=2)
        ttk.Label(fields_frame, text="Type").grid(row=0, column=2, padx=2, pady=2)
        ttk.Label(fields_frame, text="Length (bytes)").grid(row=0, column=3, padx=2, pady=2)

        for i in range(10):
            row_num = i + 1
            var_disable = tk.BooleanVar(value=None)
            var_enable = tk.BooleanVar(value=True) # Default enabled
            chk = ttk.Checkbutton(fields_frame, variable=var_disable)
            chk.grid(row=row_num, column=0, padx=2, pady=2)
            self.field_checkboxes.append(var_disable)

            ttk.Label(fields_frame, text=f"Field {i+1}:").grid(row=row_num, column=1, padx=2, pady=2, sticky="w")

            type_combo = ttk.Combobox(fields_frame, values=list(self.CHAR_RANGES.keys()), state="readonly", width=25) # Adjusted width
            type_combo.set("Random Hex (0x00-0xFF)")
            type_combo.grid(row=row_num, column=2, padx=2, pady=2, sticky="ew")
            self.field_types.append(type_combo)

            length_entry = ttk.Entry(fields_frame, width=5) # Adjusted width
            length_entry.insert(0, "1") # Default length 1
            length_entry.grid(row=row_num, column=3, padx=2, pady=2, sticky="ew")
            # Add validation for length entry
            vcmd = (self.master.register(self.validate_length), '%P')
            length_entry.config(validate="key", validatecommand=vcmd)
            self.field_lengths.append(length_entry)

        fields_frame.grid_columnconfigure(2, weight=1) # Allow type combobox to expand


        # --- Last Field (Checksum) Configuration Frame ---
        checksum_frame = ttk.LabelFrame(middle_section_frame, text="Last Field (Checksum/Empty)")
        checksum_frame.grid(row=0, column=1, padx=5, pady=2, sticky="nsew")

        self.checksum_mode = tk.StringVar(value="Empty") # Default to Empty
        ttk.Radiobutton(checksum_frame, text="Empty", variable=self.checksum_mode, value="Empty", command=self.toggle_checksum_options).grid(row=0, column=0, columnspan=2, padx=5, pady=2, sticky="w")
        ttk.Radiobutton(checksum_frame, text="Checksum", variable=self.checksum_mode, value="Checksum", command=self.toggle_checksum_options).grid(row=1, column=0, columnspan=2, padx=5, pady=2, sticky="w")

        ttk.Label(checksum_frame, text="Algorithm:").grid(row=2, column=0, padx=2, pady=2, sticky="w")
        # Updated values to include LRC
        self.checksum_algo_combobox = ttk.Combobox(checksum_frame, values=["LRC", "CRC-8", "CRC-16"], state="readonly", width=10)
        self.checksum_algo_combobox.set("LRC") # Default to LRC
        self.checksum_algo_combobox.grid(row=2, column=1, padx=2, pady=2, sticky="w")
        self.checksum_algo_combobox.bind("<<ComboboxSelected>>", self.update_checksum_length_label)

        ttk.Label(checksum_frame, text="Length:").grid(row=3, column=0, padx=2, pady=2, sticky="w")
        self.checksum_length_label = ttk.Label(checksum_frame, text="1 byte") # Default for LRC
        self.checksum_length_label.grid(row=3, column=1, padx=2, pady=2, sticky="w")

        self.toggle_checksum_options() # Initialize state

        # Configure middle_section_frame columns to expand
        middle_section_frame.grid_columnconfigure(0, weight=1)
        middle_section_frame.grid_columnconfigure(1, weight=1)

        # --- Log Area ---
        log_frame = ttk.LabelFrame(self.master, text="Log Output")
        log_frame.pack(padx=5, pady=2, fill="both", expand=True)

        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, width=80, height=20, font=("Courier", 8, "normal"))
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_text.config(state=tk.DISABLED) # Make it read-only

    def refresh_ports(self):
        ports = serial.tools.list_ports.comports()
        self.port_combobox['values'] = [port.device for port in ports]
        if ports:
            self.port_combobox.set(ports[0].device)
        else:
            self.port_combobox.set("")

    def validate_length(self, P):
        if P == "": return True # Allow empty during deletion
        try:
            value = int(P)
            return 1 <= value <= 100
        except ValueError:
            return False

    def validate_float(self, P):
        if P == "": return True
        try:
            value = float(P)
            return value > 0
        except ValueError:
            return False

    def validate_int(self, P):
        if P == "": return True
        try:
            value = int(P)
            return value >= 0
        except ValueError:
            return False

    def toggle_checksum_options(self):
        is_checksum = (self.checksum_mode.get() == "Checksum")
        self.checksum_algo_combobox.config(state="readonly" if is_checksum else "disabled")
        self.update_checksum_length_label()

    def update_checksum_length_label(self, event=None):
        if self.checksum_mode.get() == "Checksum":
            algo = self.checksum_algo_combobox.get()
            if algo == "LRC" or algo == "CRC-8":
                self.checksum_length_label.config(text="1 byte")
            elif algo == "CRC-16":
                self.checksum_length_label.config(text="2 bytes")
        else:
            self.checksum_length_label.config(text="")

    def log_message(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END) # Scroll to the end
        self.log_text.config(state=tk.DISABLED)

    def connect_serial(self):
        if self.ser and self.ser.is_open:
            self.log_message("Already connected.")
            return

        port = self.port_combobox.get()
        try:
            baudrate = int(self.baudrate_combobox.get())
            bytesize = int(self.databits_combobox.get())
            parity = self.parity_combobox.get()
            stopbits = float(self.stopbits_combobox.get())

            self.ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                bytesize=bytesize,
                parity=parity,
                stopbits=stopbits,
                timeout=0.1 # Small timeout for reading
            )
            self.log_message(f"Connected to {port} at {baudrate} baud.")
            self.connect_button.config(state=tk.DISABLED)
            self.disconnect_button.config(state=tk.NORMAL)
            self.send_single_button.config(state=tk.NORMAL)
            self.start_fuzz_button.config(state=tk.NORMAL)
        except serial.SerialException as e:
            messagebox.showerror("Serial Error", f"Could not open serial port: {e}")
            self.log_message(f"Failed to connect: {e}")
        except ValueError as e:
            messagebox.showerror("Configuration Error", f"Invalid serial setting: {e}")
            # self.log_message(f"Configuration error: {e}")
        # except KeyError as e:
            # messagebox.showerror("Configuration Error", f"Invalid parity or stop bits value: {e}")
            self.log_message(f"Configuration error: {e}")

    def disconnect_serial(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.ser = None
            self.log_message("Disconnected from serial port.")
            self.connect_button.config(state=tk.NORMAL)
            self.disconnect_button.config(state=tk.DISABLED)
            self.send_single_button.config(state=tk.DISABLED)
            self.start_fuzz_button.config(state=tk.DISABLED)
            self.stop_fuzz_button.config(state=tk.DISABLED)
            self.stop_fuzzing() # Ensure fuzzing thread stops

    def generate_field_bytes(self, field_type, field_length):
        if field_type not in self.CHAR_RANGES:
            raise ValueError(f"Unknown field type: {field_type}")

        char_pool = self.CHAR_RANGES[field_type]
        generated_bytes = bytes([random.choice(char_pool) for _ in range(field_length)])
        return generated_bytes

    def calculate_checksum(self, data_bytes, algo):
        if algo == "LRC":
            lrc = 0
            for byte_val in data_bytes:
                lrc ^= byte_val
            return lrc.to_bytes(1, 'big') # LRC is 1 byte
        elif algo == "CRC-8":
            crc8_func = crcmod.predefined.mkCrcFun('crc-8')
            checksum = crc8_func(data_bytes)
            return checksum.to_bytes(1, 'big') # CRC-8 is 1 byte
        elif algo == "CRC-16":
            crc16_func = crcmod.predefined.mkCrcFun('crc-16')
            checksum = crc16_func(data_bytes)
            return checksum.to_bytes(2, 'big') # CRC-16 is 2 bytes
        else:
            raise ValueError(f"Unsupported checksum algorithm: {algo}")

    def generate_packet(self):
        packet_data = bytearray()
        for i in range(10): # Iterate through 10 configurable fields
            if self.field_checkboxes[i].get(): # Check if field is enabled
                try:
                    field_type = self.field_types[i].get()
                    field_length = int(self.field_lengths[i].get())
                    packet_data.extend(self.generate_field_bytes(field_type, field_length))
                except ValueError as e:
                    messagebox.showerror("Input Error", f"Field {i+1} configuration error: {e}")
                    return None
            else:
                # self.log_message(f"Field {i+1} is disabled.") # Nigel: too verbose for continuous fuzzing
                pass

        # Handle last field (checksum or empty)
        if self.checksum_mode.get() == "Checksum":
            try:
                algo = self.checksum_algo_combobox.get()
                checksum_bytes = self.calculate_checksum(packet_data, algo)
                packet_data.extend(checksum_bytes)
            except ValueError as e:
                messagebox.showerror("Checksum Error", f"Checksum calculation error: {e}")
                return None
        else:
            # self.log_message("Last field is empty (no checksum).") # Nigle: too verbose
            pass

        return bytes(packet_data)

    def send_single_packet(self):
        if not self.ser or not self.ser.is_open:
            messagebox.showwarning("Not Connected", "Please connect to a serial port first.")
            return

        packet = self.generate_packet()
        if packet is None:
            return # Error during packet generation

        try:
            self.ser.write(packet)
            self.log_message(f"SENT: {binascii.hexlify(packet).decode('utf-8').upper()}")

            # Try to read response
            response = self.ser.read_all()
            if response:
                self.log_message(f"RECV: {binascii.hexlify(response).decode('utf-8').upper()}")
        except serial.SerialException as e:
            messagebox.showerror("Serial Error", f"Error sending data: {e}")
            self.log_message(f"Send error: {e}")
            self.disconnect_serial() # Disconnect on error
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            self.log_message(f"Unexpected error: {e}")

    def fuzz_loop(self, iterations, interval):
        count = 0
        while self.fuzzing_active and (iterations == 0 or count < iterations):
            self.send_single_packet()
            count += 1
            if iterations != 0:
                self.log_message(f"Fuzzing iteration: {count}/{iterations}")
            else:
                self.log_message(f"Fuzzing iteration: {count} (infinite)")
            time.sleep(interval/1000) # Interval is in milliseconds, convert to seconds
        self.fuzzing_active = False # Ensure state is reset if loop finishes
        self.master.after(0, self.update_fuzzing_buttons) # Update GUI from main thread

    def start_fuzzing(self):
        if not self.ser or not self.ser.is_open:
            messagebox.showwarning("Not Connected", "Please connect to a serial port first.")
            return

        if self.fuzzing_active:
            self.log_message("Fuzzing is already active.")
            return

        try:
            interval = float(self.interval_entry.get())
            iterations = int(self.iterations_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for interval and iterations.")
            return

        self.fuzzing_active = True
        self.fuzz_thread = threading.Thread(target=self.fuzz_loop, args=(iterations, interval))
        self.fuzz_thread.daemon = True # Allow main program to exit even if thread is running
        self.fuzz_thread.start()
        self.log_message("Fuzzing started...")
        self.update_fuzzing_buttons()

    def stop_fuzzing(self):
        if self.fuzzing_active:
            self.fuzzing_active = False
            self.log_message("Stopping fuzzing...")
            # Give the thread a moment to finish, but don't block GUI
            if self.fuzz_thread and self.fuzz_thread.is_alive():
                # In a real app, you might add a small delay and then check if it joined,
                # but for simple GUI, just setting the flag is usually enough.
                pass
            self.update_fuzzing_buttons()
        else:
            self.log_message("Fuzzing is not active.")

    def update_fuzzing_buttons(self):
        if self.fuzzing_active:
            self.start_fuzz_button.config(state=tk.DISABLED)
            self.stop_fuzz_button.config(state=tk.NORMAL)
            self.send_single_button.config(state=tk.DISABLED)
        else:
            self.start_fuzz_button.config(state=tk.NORMAL)
            self.stop_fuzz_button.config(state=tk.DISABLED)
			# self.send_single_button.config(state=tk.NORMAL)
            # Re-enable if connected
            if self.ser and self.ser.is_open:
                self.send_single_button.config(state=tk.NORMAL)
                self.start_fuzz_button.config(state=tk.NORMAL)
            else:
                self.send_single_button.config(state=tk.DISABLED)
                self.start_fuzz_button.config(state=tk.DISABLED)

# --- Main Application ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SerialFuzzTool(root)
    root.iconbitmap('logo.ico')  # adding proper icon
    root.mainloop()
