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

#   Initial version was built in June 2025                                       #
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
#   1. Adding headers and checksum   --- on going 2025.07.23 - v00.05.01         #
#   2. Released the final version    --- on going 2025.07.23 - v01.00.00         #
#   3. Added Parameter Configuration --- 2025.07.24 - v01.01.00                  #
#   4. Fixed "Fixed Value" entry issue - 2025.07.24 - v01.02.00                  #
#   5. Embedded icon into single file  - 2025.08.04 - v01.02.01                  #
#   6. Updated the icon                - 2025.09.03 - v01.02.02                  #
#                                                                                #
# _______________________________________________________________________________#
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import serial
import serial.tools.list_ports
import random
import time
import threading
import binascii
import base64
import crcmod.predefined # For CRC-8 and CRC-16
import json # Import json for configuration saving/loading

# === Paste your Base64 encoded PNG string here ===
ICON_PNG_BASE64 = """
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cGUvUmVzb3VyY2VFdmVudCMiCiAgICB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iCiAgICB4bWxuczpleGlmPSJodHRwOi8vbnMuYWRvYmUuY29tL2V4aWYvMS4wLyIKICAgIHhtbG5zOkdJTVA9Imh0dHA6Ly93d3cuZ2ltcC5vcmcveG1wLyIKICAgIHhtbG5zOmlwdGNFeHQ9Imh0dHA6Ly9pcHRjLm9yZy9zdGQvSXB0YzR4bXBFeHQvMjAwOC0wMi0yOS8iCiAgICB4bWxuczpwaG90b3Nob3A9Imh0dHA6Ly9ucy5hZG9iZS5jb20vcGhvdG9zaG9wLzEuMC8iCiAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyIKICAgIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIKICAgeG1wTU06RG9jdW1lbnRJRD0iZ2ltcDpkb2NpZDpnaW1wOmE4MzRhNmI1LWQyMDAtNGEzZC05NWZmLTI2ODlkNzIzOTlkMCIKICAgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDphNDczZjIyNy02MTAwLTQ3NTAtOGI4OC00NDUyMzkyOWQxOWMiCiAgIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDoxZTkwM2UyNy1jZmMwLTQ4NzAtYjE0Mi1mZTI4MjczMTQ3YTAiCiAgIGRjOkZvcm1hdD0iaW1hZ2UvcG5nIgogICBleGlmOkRhdGVUaW1lT3JpZ2luYWw9IjIwMjUtMDktMDNUMDY6Mzk6MTArMDA6MDAiCiAgIEdJTVA6QVBJPSIyLjAiCiAgIEdJTVA6UGxhdGZvcm09IldpbmRvd3MiCiAgIEdJTVA6VGltZVN0YW1wPSIxNzU2ODgxODY3NzE2MTExIgogICBHSU1QOlZlcnNpb249IjIuMTAuMzAiCiAgIGlwdGNFeHQ6RGlnaXRhbFNvdXJjZUZpbGVUeXBlPSJodHRwOi8vY3YuaXB0Yy5vcmcvbmV3c2NvZGVzL2RpZ2l0YWxzb3VyY2V0eXBlL2NvbXBvc2l0ZVdpdGhUcmFpbmVkQWxnb3JpdGhtaWNNZWRpYSIKICAgaXB0Y0V4dDpEaWdpdGFsU291cmNlVHlwZT0iaHR0cDovL2N2LmlwdGMub3JnL25ld3Njb2Rlcy9kaWdpdGFsc291cmNldHlwZS9jb21wb3NpdGVXaXRoVHJhaW5lZEFsZ29yaXRobWljTWVkaWEiCiAgIHBob3Rvc2hvcDpDcmVkaXQ9IkVkaXRlZCB3aXRoIEdvb2dsZSBBSSIKICAgcGhvdG9zaG9wOkRhdGVDcmVhdGVkPSIyMDI1LTA5LTAzVDA2OjM5OjEwKzAwOjAwIgogICB0aWZmOk9yaWVudGF0aW9uPSIxIgogICB4bXA6Q3JlYXRvclRvb2w9IkdJTVAgMi4xMCI+CiAgIDx4bXBNTTpIaXN0b3J5PgogICAgPHJkZjpTZXE+CiAgICAgPHJkZjpsaQogICAgICBzdEV2dDphY3Rpb249InNhdmVkIgogICAgICBzdEV2dDpjaGFuZ2VkPSIvIgogICAgICBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOjllMmQxYTUwLTcyMWEtNDU1MC05Y2RkLTA2ZmM0ZDJiYTQ3OCIKICAgICAgc3RFdnQ6c29mdHdhcmVBZ2VudD0iR2ltcCAyLjEwIChXaW5kb3dzKSIKICAgICAgc3RFdnQ6d2hlbj0iMjAyNS0wOS0wM1QxNjo0MjoyNCIvPgogICAgIDxyZGY6bGkKICAgICAgc3RFdnQ6YWN0aW9uPSJzYXZlZCIKICAgICAgc3RFdnQ6Y2hhbmdlZD0iLyIKICAgICAgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDpkZmMxZjVmOC00NTIxLTQ5YzMtODA0YS03ODMzYzY4NThhMTkiCiAgICAgIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkdpbXAgMi4xMCAoV2luZG93cykiCiAgICAgIHN0RXZ0OndoZW49IjIwMjUtMDktMDNUMTY6NDQ6MjciLz4KICAgIDwvcmRmOlNlcT4KICAgPC94bXBNTTpIaXN0b3J5PgogIDwvcmRmOkRlc2NyaXB0aW9uPgogPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg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
"""

class SerialFuzzTool:
    def __init__(self, master):
        self.master = master
        Fuzz_ver = "01.02.02"
        Fuzz_yr = "2025.09.03"
        master.title("FuzzBox" + " (v" + Fuzz_ver +")" + " - " + Fuzz_yr + " - Nigel Zhai")
        master.geometry("600x750+50+50") # Set initial window size
        master.minsize(600, 750) # Set minimum window size
        master.maxsize(600, 750) # Set maximum window size

        # Set the window icon
        self.set_window_icon()

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
        self.interval_entry = ttk.Entry(control_frame, width=5) # Adjusted width
        self.interval_entry.insert(0, "10")
        vcmd_float = (self.master.register(self.validate_float), '%P')
        self.interval_entry.config(validate="key", validatecommand=vcmd_float)
        self.interval_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=2, sticky="news")

        ttk.Label(control_frame, text="Loops (0=infinite):").grid(row=1, column=0, padx=10, pady=2, sticky="w")
        self.iterations_entry = ttk.Entry(control_frame, width=5) # Adjusted width
        self.iterations_entry.insert(0, "0")
        vcmd_int = (self.master.register(self.validate_int), '%P')
        self.iterations_entry.config(validate="key", validatecommand=vcmd_int)
        self.iterations_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=2, sticky="news")

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
        self.start_fuzz_button.grid(row=2, column=1, rowspan=2, columnspan=2, padx=5, pady=5, sticky="news") # Spans two columns
        self.stop_fuzz_button = ttk.Button(control_frame, text="Stop!", width=15, command=self.stop_fuzzing, state=tk.DISABLED, style="Red.TButton")
        self.stop_fuzz_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="wns") # Spans two columns

        control_frame.grid_columnconfigure(1, weight=1) # Allow entry fields to expand

        # Configure top_section_frame columns to expand
        top_section_frame.grid_columnconfigure(0, weight=1)
        top_section_frame.grid_columnconfigure(1, weight=1)


        # --- Middle Section Container Frame (Field Config, Checksum, and Parameter Config) ---
        middle_section_frame = ttk.Frame(self.master)
        middle_section_frame.pack(padx=10, pady=2, fill="both", expand=True)

        # --- Field Configuration Frame ---
        fields_frame = ttk.LabelFrame(middle_section_frame, width=25, text="Field Configuration")
        fields_frame.grid(row=0, rowspan=2, column=0, padx=5, pady=2, sticky="nsew")

        self.field_types = []
        self.field_lengths = []
        self.field_checkboxes = []
        self.fixed_value_stringvars = [] # New list for fixed value StringVars
        self.fixed_value_entries = [] # New list for fixed value Entry widgets

        # Header row for fields
        ttk.Label(fields_frame, text="Check").grid(row=0, column=0, padx=2, pady=2)
        ttk.Label(fields_frame, text="Fields").grid(row=0, column=1, padx=2, pady=2)
        ttk.Label(fields_frame, text="Type").grid(row=0, column=2, padx=2, pady=2)
        ttk.Label(fields_frame, text="Length").grid(row=0, column=3, padx=2, pady=2)
        ttk.Label(fields_frame, text="Fixed Value").grid(row=0, column=4, padx=2, pady=2) # New header

        for i in range(10):
            row_num = i + 1
            var_enable = tk.BooleanVar(value=True) # Default enabled
            var_disable = tk.BooleanVar(value=False) # Default disabled
            chk = ttk.Checkbutton(fields_frame, variable=var_disable)
            chk.grid(row=row_num, column=0, padx=2, pady=2)
            self.field_checkboxes.append(var_disable)

            ttk.Label(fields_frame, text=f"Field {i+1}:").grid(row=row_num, column=1, padx=2, pady=2, sticky="w")

            # Add "Fixed value" to the list of types
            type_combo = ttk.Combobox(fields_frame, values=list(self.CHAR_RANGES.keys()) + ["Fixed value"], state="readonly", width=20) # Adjusted width
            type_combo.set("Random Hex (0x00-0xFF)")
            type_combo.grid(row=row_num, column=2, padx=2, pady=2, sticky="ew")
            self.field_types.append(type_combo)
            type_combo.bind("<<ComboboxSelected>>", lambda event, idx=i: self._on_field_type_selected(event, idx))

            length_entry = ttk.Entry(fields_frame, width=5) # Adjusted width
            length_entry.insert(0, "1") # Default length 1
            length_entry.grid(row=row_num, column=3, padx=2, pady=2, sticky="ew")
            # Add validation for length entry
            vcmd = (self.master.register(self.validate_length), '%P')
            length_entry.config(validate="key", validatecommand=vcmd)
            self.field_lengths.append(length_entry)

            # New: Fixed Value Entry
            fixed_val_sv = tk.StringVar()
            fixed_val_entry = ttk.Entry(fields_frame, textvariable=fixed_val_sv, width=6) # Adjusted width
            # Validate hex input for fixed value
            vcmd_hex = (self.master.register(self.validate_hex_input), '%P', row_num - 1) # Pass field index for validation. Nigel "row_num - 1" was "idx"
            fixed_val_entry.config(validate="key", validatecommand=vcmd_hex)
            fixed_val_entry.grid(row=row_num, column=4, padx=2, pady=2, sticky="ew")
            fixed_val_entry.grid_remove() # Initially hide it
            self.fixed_value_stringvars.append(fixed_val_sv)
            self.fixed_value_entries.append(fixed_val_entry)

        fields_frame.grid_columnconfigure(2, weight=1) # Allow type combobox to expand
        fields_frame.grid_columnconfigure(4, weight=1) # Allow fixed value entry to expand


        # --- Last Field (Checksum) Configuration Frame ---
        checksum_frame = ttk.LabelFrame(middle_section_frame, text="Last Field (Checksum)")
        checksum_frame.grid(row=0, column=1, padx=5, pady=2, sticky="news")

        self.checksum_mode = tk.StringVar(value="Empty") # Default to Empty
        ttk.Radiobutton(checksum_frame, text="Empty", variable=self.checksum_mode, value="Empty", command=self.toggle_checksum_options).grid(row=0, column=0, columnspan=2, padx=5, pady=2, sticky="w")
        ttk.Radiobutton(checksum_frame, text="Checksum", variable=self.checksum_mode, value="Checksum", command=self.toggle_checksum_options).grid(row=1, column=0, columnspan=2, padx=5, pady=2, sticky="w")

        ttk.Label(checksum_frame, text="Algorithm:").grid(row=2, column=0, padx=2, pady=2, sticky="w")
        # Updated values to include LRC
        self.checksum_algo_combobox = ttk.Combobox(checksum_frame, values=["LRC", "CRC-8", "CRC-16"], state="readonly", width=9)
        self.checksum_algo_combobox.set("LRC") # Default to LRC
        self.checksum_algo_combobox.grid(row=2, column=1, padx=2, pady=2, sticky="w")
        self.checksum_algo_combobox.bind("<<ComboboxSelected>>", self.update_checksum_length_label)

        ttk.Label(checksum_frame, text="Length:").grid(row=3, column=0, padx=2, pady=2, sticky="w")
        self.checksum_length_label = ttk.Label(checksum_frame, text="1 byte") # Default for LRC
        self.checksum_length_label.grid(row=3, column=1, padx=2, pady=2, sticky="w")

        self.toggle_checksum_options() # Initialize state



        # --- New: Parameter Configuration Frame ---
        param_config_frame = ttk.LabelFrame(middle_section_frame, text="Parameter Configuration")
        # Positioned right of fields_frame (column 1) and below checksum_frame (row 1)
        param_config_frame.grid(row=1, column=1, padx=5, pady=2, sticky="news")

        ttk.Button(param_config_frame, text="Export Config", width=10, command=self.export_config).pack(side=tk.TOP, padx=5, pady=10, fill="x")
        ttk.Button(param_config_frame, text="Import Config", width=10, command=self.import_config).pack(side=tk.TOP, padx=5, pady=10, fill="x")


        # Configure middle_section_frame columns and rows to expand
        middle_section_frame.grid_columnconfigure(0, weight=1) # fields_frame
        middle_section_frame.grid_columnconfigure(1, weight=1) # checksum_frame and param_config_frame
        middle_section_frame.grid_rowconfigure(0, weight=1) # Row for fields_frame and checksum_frame
        middle_section_frame.grid_rowconfigure(1, weight=0) # Row for param_config_frame


        # --- Log Area ---
        log_frame = ttk.LabelFrame(self.master, text="Log Output")
        log_frame.pack(padx=5, pady=2, fill="both", expand=True)

        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, width=80, height=20, font=("Courier", 8, "normal"))
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_text.config(state=tk.DISABLED) # Make it read-only

    def set_window_icon(self):
        try:
            # Decode the Base64 string
            icon_data = base64.b64decode(ICON_PNG_BASE64)

            # Attempt to use PhotoImage directly
            try:
                photo_image = tk.PhotoImage(data=icon_data)
                self.master.iconphoto(True, photo_image)
            except tk.TclError:
                # Fallback to .ico if PhotoImage fails (e.g., if the data isn't a valid PNG or Tkinter version issues)
                # This requires writing to a temporary .ico file.
                print("PhotoImage failed, attempting .ico fallback...")
                temp_ico_path = os.path.join(tempfile.gettempdir(), "temp_icon.ico")
                with open(temp_ico_path, "wb") as f:
                    f.write(icon_data) # Assuming the base64 could also be an ICO
                self.master.iconbitmap(temp_ico_path)
                os.remove(temp_ico_path) # Clean up the temporary file

        except Exception as e:
            print(f"Error setting PNG icon from Base64 or ICO fallback: \n{e}")
            print("Ensure the Base64 string is correct and represents a valid PNG or ICO image.")
            # Fallback to a default Tkinter icon if all else fails
            self.master.iconbitmap(default="::tk::icons::question")

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

    def validate_hex_input(self, P, field_idx):
        print(f"Type of field_idx: {type(field_idx)}")
        print(f"Value of field_idx: {field_idx}")
        
        int_field_idx = int(field_idx) if isinstance(field_idx, str) else field_idx

        # Allow empty string for deletion
        if P == "":
            self.field_lengths[int_field_idx].config(state=tk.NORMAL) # Enable length entry
            self.field_lengths[int_field_idx].delete(0, tk.END)
            self.field_lengths[int_field_idx].insert(0, "")
            self.field_lengths[int_field_idx].config(state=tk.DISABLED) # Disable it again
            return True
        
        # Check if it's a valid hex string
        if not all(c in '0123456789abcdefABCDEF' for c in P):
            return False
        
        # Update length based on hex string
        byte_length = len(P) // 2
        self.field_lengths[int_field_idx].config(state=tk.NORMAL) # Temporarily enable to update
        self.field_lengths[int_field_idx].delete(0, tk.END)
        self.field_lengths[int_field_idx].insert(0, str(byte_length))
        self.field_lengths[int_field_idx].config(state=tk.DISABLED) # Disable it again
        
        return True

    def _on_field_type_selected(self, event, field_index):
        selected_type = self.field_types[field_index].get()
        if selected_type == "Fixed value":
            self.fixed_value_entries[field_index].grid() # Show the fixed value entry
            self.field_lengths[field_index].config(state=tk.DISABLED) # Disable length entry
            # Trigger validation to update length based on current fixed value
            self.validate_hex_input(self.fixed_value_stringvars[field_index].get(), field_index)
        else:
            self.fixed_value_entries[field_index].grid_remove() # Hide the fixed value entry
            self.field_lengths[field_index].config(state=tk.NORMAL) # Enable length entry
            # Reset length to 1 if it was a fixed value field and now changed
            if not self.field_lengths[field_index].get(): # If it's empty
                 self.field_lengths[field_index].insert(0, "1")


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
            self.log_message(f"Configuration error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            self.log_message(f"Unexpected error: {e}")

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

    def generate_field_bytes(self, field_type, field_length, fixed_value_hex=None):
        if field_type == "Fixed value":
            if not fixed_value_hex:
                raise ValueError("Fixed value cannot be empty for 'Fixed value' type.")
            try:
                # Ensure fixed_value_hex has an even number of characters
                if len(fixed_value_hex) % 2 != 0:
                    raise ValueError("Fixed hex value must have an even number of characters.")
                return binascii.unhexlify(fixed_value_hex)
            except binascii.Error:
                raise ValueError(f"Invalid hexadecimal string: {fixed_value_hex}")
        
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
                    field_length = int(self.field_lengths[i].get()) # This will be auto-updated for fixed value
                    fixed_value_hex = self.fixed_value_stringvars[i].get() if field_type == "Fixed value" else None

                    # If fixed value, use its actual byte length, not the user-entered one
                    if field_type == "Fixed value":
                        if not fixed_value_hex:
                            messagebox.showerror("Input Error", f"Field {i+1} (Fixed value) cannot be empty.")
                            return None
                        # Length is derived from hex string, not user input
                        actual_length = len(binascii.unhexlify(fixed_value_hex))
                        if actual_length != field_length: # This should ideally not happen if validate_hex_input works
                            self.log_message(f"Warning: Field {i+1} fixed value length mismatch. Using derived length {actual_length}.")
                            field_length = actual_length

                    packet_data.extend(self.generate_field_bytes(field_type, field_length, fixed_value_hex))
                except ValueError as e:
                    messagebox.showerror("Input Error", f"Field {i+1} configuration error: {e}")
                    return None
            else:
                pass # Field is disabled

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
            pass # Last field is empty (no checksum).

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
            packet = self.generate_packet() # Regenerate packet for each iteration
            if packet is None:
                self.log_message("Fuzzing stopped due to packet generation error.")
                self.fuzzing_active = False
                break # Exit loop if packet generation fails

            try:
                self.ser.write(packet)
                self.log_message(f"SENT ({count+1}/{iterations if iterations != 0 else 'Inf'}): {binascii.hexlify(packet).decode('utf-8').upper()}")

                # Try to read response
                response = self.ser.read_all()
                if response:
                    self.log_message(f"RECV: {binascii.hexlify(response).decode('utf-8').upper()}")
            except serial.SerialException as e:
                messagebox.showerror("Serial Error", f"Error sending data during fuzzing: {e}")
                self.log_message(f"Fuzzing send error: {e}")
                self.fuzzing_active = False # Stop fuzzing on serial error
                self.disconnect_serial() # Disconnect on error
                break # Exit loop
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred during fuzzing: {e}")
                self.log_message(f"Fuzzing unexpected error: {e}")
                self.fuzzing_active = False # Stop fuzzing on unexpected error
                break # Exit loop

            count += 1
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
            # Re-enable if connected
            if self.ser and self.ser.is_open:
                self.send_single_button.config(state=tk.NORMAL)
                self.start_fuzz_button.config(state=tk.NORMAL)
            else:
                self.send_single_button.config(state=tk.DISABLED)
                self.start_fuzz_button.config(state=tk.DISABLED)

    def export_config(self):
        config = {
            "serial_port": {
                "port": self.port_combobox.get(),
                "baudrate": self.baudrate_combobox.get(),
                "databits": self.databits_combobox.get(),
                "parity": self.parity_combobox.get(),
                "stopbits": self.stopbits_combobox.get()
            },
            "fuzzing_controls": {
                "interval": self.interval_entry.get(),
                "iterations": self.iterations_entry.get()
            },
            "field_configurations": [],
            "checksum_config": {
                "mode": self.checksum_mode.get(),
                "algorithm": self.checksum_algo_combobox.get()
            }
        }

        for i in range(10):
            field_type = self.field_types[i].get()
            field_config_data = {
                "enabled": self.field_checkboxes[i].get(),
                "type": field_type,
                "length": self.field_lengths[i].get() # This will be the auto-updated length for fixed value
            }
            if field_type == "Fixed value":
                field_config_data["fixed_value"] = self.fixed_value_stringvars[i].get()
            config["field_configurations"].append(field_config_data)

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Export Configuration"
        )
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(config, f, indent=4)
                messagebox.showinfo("Export Config", f"Configuration exported successfully to {file_path}")
                self.log_message(f"Configuration exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export configuration: {e}")
                self.log_message(f"Failed to export configuration: {e}")

    def import_config(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Import Configuration"
        )
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    config = json.load(f)

                # Set Serial Port Configuration
                self.port_combobox.set(config["serial_port"]["port"])
                self.baudrate_combobox.set(config["serial_port"]["baudrate"])
                self.databits_combobox.set(config["serial_port"]["databits"])
                self.parity_combobox.set(config["serial_port"]["parity"])
                self.stopbits_combobox.set(config["serial_port"]["stopbits"])

                # Set Fuzzing Controls
                self.interval_entry.delete(0, tk.END)
                self.interval_entry.insert(0, config["fuzzing_controls"]["interval"])
                self.iterations_entry.delete(0, tk.END)
                self.iterations_entry.insert(0, config["fuzzing_controls"]["iterations"])

                # Set Field Configurations
                for i, field_config in enumerate(config["field_configurations"]):
                    if i < 10: # Ensure we don't go out of bounds
                        self.field_checkboxes[i].set(field_config["enabled"])
                        self.field_types[i].set(field_config["type"])
                        
                        # Handle fixed value specific logic
                        if field_config["type"] == "Fixed value":
                            self.fixed_value_stringvars[i].set(field_config.get("fixed_value", ""))
                            self.fixed_value_entries[i].grid() # Show the entry
                            self.field_lengths[i].config(state=tk.DISABLED) # Disable length entry
                            # Trigger validation to update length based on imported fixed value
                            self.validate_hex_input(self.fixed_value_stringvars[i].get(), i)
                        else:
                            self.fixed_value_entries[i].grid_remove() # Hide the entry
                            self.fixed_value_stringvars[i].set("") # Clear fixed value
                            self.field_lengths[i].config(state=tk.NORMAL) # Enable length entry
                            self.field_lengths[i].delete(0, tk.END)
                            self.field_lengths[i].insert(0, field_config["length"])


                # Set Checksum Config
                self.checksum_mode.set(config["checksum_config"]["mode"])
                self.checksum_algo_combobox.set(config["checksum_config"]["algorithm"])
                self.toggle_checksum_options() # Update display based on new mode/algo

                messagebox.showinfo("Import Config", f"Configuration imported successfully from {file_path}")
                self.log_message(f"Configuration imported from {file_path}")
            except FileNotFoundError:
                messagebox.showerror("Import Error", "Selected file not found.")
                self.log_message("Import error: Selected file not found.")
            except json.JSONDecodeError:
                messagebox.showerror("Import Error", "Invalid JSON format in selected file.")
                self.log_message("Import error: Invalid JSON format.")
            except KeyError as e:
                messagebox.showerror("Import Error", f"Missing key in configuration file: {e}. Please ensure the file is valid.")
                self.log_message(f"Import error: Missing key {e} in configuration file.")
            except Exception as e:
                messagebox.showerror("Import Error", f"Failed to import configuration: {e}")
                self.log_message(f"Failed to import configuration: {e}")


# --- Main Application ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SerialFuzzTool(root)
    root.mainloop()