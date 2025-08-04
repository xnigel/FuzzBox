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
#   5. Embedded icon into single file  - 2025.08.04 - v01.02.01
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
iVBORw0KGgoAAAANSUhEUgAAAEAAAAA/CAYAAABQHc7KAAABhGlDQ1BJQ0MgcHJvZmlsZQAAKM+VkT1Iw0AYhl/TSotUHOwg4pChOtlFRRxLFItgobQVWnUwufQPmjQkKS6OgmvBwZ/FqoOLs64OroIg+APiLjgpukiJ3yWFFKGCHxz38N697919BwitGtOsYALQdNvMJCUxX1gVQ68IIwigD0GZWUYqu5hDz/q6p31Ud3Gehf/VoFq0GB0kEieYYdrEG8Szm7bBeZ84yiqySnxOPGnSBYkfua54/Ma57LLAM6NmLjNPHCUWy12sdDGrmBrxDHFM1XTKF/Ieq5y3OGu1Buvck78wUtRXslynMYYklpBCGiIUNFBFDTbiNOukWMjQutTDP+r60+RSyFUFI8cC6tAgu37wP/jdW6s0PeUlRSSg/8VxPsaB0C7QbjrO97HjtE+AwDNwpfv+eguY+yS96WuxI2BoG7i49jVlD7jcAUaeDNmUXSlAQyiVgPcz+qYCMHwLDKx5feus4/QByFGvlm+Ag0NgokzZ6z3eHe7u25973P5B+gHq23JwCVDD0AAAAAlwSFlzAAALEQAACxEBf2RfkQAAAAZiS0dEAP8A/wD/oL2nkwAAAAd0SU1FB+kIBAABM+RGbCsAAA2qSURBVHhe5VtbiFZHEu7/nxlvRGVCfFDUIAbJSlbwsiA+uOJbUIPOzCqOq+Jo3AQhrq6ayCY+aLygK4JZFS/ouiSDYjSMIAq+RPBJUDCCCCtmEQwal8RRE2//ZeurOtWnzznd5//HuCzrfqbmdFdXV3VXd/XlnD+FxsbGaqFQMF5E7EIVfwqmiqfhP5SVwirnKU2FBTw5KTKow9B8AiLrL6sDXFeSXtQqJ6A43wH/g9A+19Mj+L4Ypf9vkZoBBfPs2dMo/XKiqakpSmEGUNg2NTYheBnlctm8+eabZubMmZyWWE4FEznLnV4QsaFeqZimXr1M33794ioq7KgAbB15xNA1IScsUaJi0QIljEAdcMvlkvn8805z/fo/TENDA/O5f+SRqhJ4CxYsIP7LiVmzZnEftb+Y/Zk1oFQqRSljKhXI14dyuULyFXnS7KnQE7MoJvArPEtqIVlPiHVSXehgQjpNbDPLUzx9mg3v4CJIDiOqmGdPn5mffvrJ/Pzzz15CGYDZhzoAuzkzucGpmgrJ+PSAHj58SGvQM9KFSavTWdKsE22K/glDH0ggJZJIMj+Sz0PuLoBYOXHihBkzZowZN26cGTd+vBDSEaFs/fr1plgsMolpF9qZAuu7ePGSGU86xo4dy7qQVp3QtWfPHtYj4axOUJ2qizgc+0T0H5KSwz8qhwgYhOSK5UF6DWhvn0eOo7Gn+Q/s3r1bdNcgchTLl0plolKKwCtz+dmzZ731lT766COWo2lfLYE8elwbZaYUj+uVmY9yxbRp09hG7hqQXkhJyD6pkpeAP7z3nrl69SqNsqr0ex6zAIRR9unpRbsIEM1ogqtHmbZQUmlTxFRWLOlHMARqTh0HaPzd77838+fPN93d3dxBmIYO1kJzNLBDeSCC+IupzU/8cxQgneDbXjJHKwmnhuGcNaCW75Kg84S5dOmSWbFiBecxE8JLkCxqfkQlnnYnOoO0ZjVJf6rKA9x0AEEH9Kz7BDKGkT906JDZu3cvM2yDSRmFoKQZ9WsXSXJktLRn+hSpYlfr8i8M9xFExgHJhsaopQiQXcCY1atX02p/McrzpMy0PNMRD1J94adtB2dsjgGd7HNmh+efi7odUC+wHjx48MB0LOowP/zwQxQKhIDaPGsIlKSjRDoeaCqNOgw306Um9gnziat5By4r4wCcnnxINiQfcMI3V74xy5Yt4zxCoyf1AemkrBXoHOqLDmm+uxxEBTGQ58WAZNNlBJcVDY8PnpopYLbg5OYDOn3kyBGzZcsWzheKSX1qtrYVkdW5wK5wK0XTgfWp0gS8TAs6ckWpDPIrovO4+b3++uvshHToyGmuYD5Z94k5c+YMpZOTLdxx7WhMMeLdIzaXliCgjBKhLdBtaWYG1LsGyEWjbDZu3GgmTpyYuEQpcHgqPSuZJUuWmBs3bjAvpN/HTS5icS52Q4xEV6OMSPmdoCjKmToLibp8PHnyxAwdOpS3vgEDBthwcDViPbh165bpWNzBTuvTpw87wW8VkBKR0K6qtARCNYpvlrGdhUzEQ4qzlKsxoME1QBXVQnf3fX6JsnPnTs7j6pp2HWbCua/PmQ2ffmr69u1rj9cusu6OFr5EgWTA4zLOCeJlEjuBOEpCwJUSuJxiIEx6AHHUwoULzfI/LudRTnsdDQFt3rTJHKTZ0q9fP0+zUiABGc9YF+YD56x+FmIec3g2Sxmn2BGSD6EYniE998ymjZvMpEmTgusBXkj89bPP+O4v94UsECJAAy2ikGkoyuUJVOQnXbujdJHTkIvIkRVeA3U/vx+Jl6KI4dmzZ5ujR4+yk8Hev3+/Wbp0KXfAXVX5LQ2NdlfXSfPOOzM4D4PXrl0zkydPNnfv3rU3PBeoU8AOEeVdwP6iRYtMR0cHpyGTP375wPuF5uZXaUcSa9OnTzenTp2y7eKZCgcQw74PIAcQP34fsG/fPua7ciDa5ph/susky9Go8x0cOHbsGJzKMpBtjMit75KW4UlOlDTZayDCUymdF15DRHEadmH/zOnT3B5FXe8DYvjGqDbIjmlrazOrVq3KrAdxKguUqUWEEOrWQ9UKrQtMksZ7TObrFK6BoAPSG1AQCRtiHFi/foP57ZQpdj2AWKg5Lh8HKBoZDqdGG89Cbl7WgyQpTw9hQYMOcmaAoA4dDrAZFXg96NOntzl08KAZNnw4HYb8x2UXPbMThqsncMRJIHVClxEQ1NkkO8VlJ0YOKbyOHjFihPkbbXu9e/e2h6QXBW2d20e1r7xaOwCgr18t3JW+PqTl4yYhHKZOnWq2bt1q87UAR9Uid11xrTOX/oAHmVKpttODIRCbqAHbgvjIgifnqBFoyAcffMBbKULDbXwacNCECb8x77//vnn33SW8Jc6bNy+i33O+vX0uvzhVZ4otAZqC8UMZTpyDBw+WgjzolgCibHXu3LnURkK92+BJdxvMkr6Wvn//fnXChAlcx9Wj1IhvlFS2edNmlg9hxYoVbBvbHdeLSPVg+0NZZ2cny5PT+QkEt0FwXyx4LDgF3Rj5/v37m8OHD5vXXnuNp3EIj5484ie2M2pzYsasWbPG7Nixg8O0SNfrdLtL0Qzb/pfthgYyU9+HnBCQDtAo2qcbhzoFy6UyP3OBaUmL4ujRo82uXbuY5eoCabw+fRJ9v6OGu2sG1pFt27bxqQ4nyXS3IIuzwMo/rTTLly/ncpwLXGB7TYMdIF1NQyo3v9rMLz3eeOONBI0cOZJX+Vf6v8JySbB5Zx5EHOoUjtrr1q3z6hw2bLgZMmSIVKCKGGkQrtsffvghpxsapBOubgCzbM6cOWbb1m2cx7sK6QFJRX7wOSBnDZDPXHSBqXZ3d3MMu0TXYOajXD5LxZ+mXJLPVk4+islY5wOr89490SeftETuNB1n6YLEbeO4ddqr8Y+yKVOmsE5AP4npZzNZzarV1tZWlm1skvUMa0BNB9jaAdDUS3TQdjSR1+904gxdYENgGcLFixergwYNSnQ+TSj79VtvVW/dusV12B45WW259tQB2l+7CLqQ4wwgU7hc0W/08u1d0s53e45TdzLGUC6esCx/6aSI8zrpElLd8hsApHGcvX79umlrbbO3SqkpwBOEE+ZwOml+efw4hw50xFL1IbsI2vqUUEt4IGvLQkgK6EIqnQfEvVaKM4hzSUIe9/jvvvvOtLS0mG//+a29umodfWLhbG5u5qv7qFGjyKm6YJI1/k/XINxqtFYWwV0AgBL8F2XidAaukEBSLp+12RT/wxYVbVXgo/M//vgjL2ZXrlyxnU8Dncfx+vDfD/MLWf4VCHRZSFpt5YFOM34B5ieKRF39SHsd+awOzWHa440RTnvnz59PrNhuLXQe2E3b6YzpMygE0dKkzjTC448ZEKyLyaNV6WljIE+dr1x5mIhalpRD5wF8Serq6uLOY8tzgZzEuDHbt283HYsXy8yp6tSPdUrLY2t5yA0BFzwK7Kw8b7tlWTnluA3Duz9g7dq15sCBA+wMX+ex2IL+/PHHZuXKlcyXBZjKrXw62iWXbombz9wGXcRTi57c+7QqH9IyWg92pEz/4jgL+zje4hMaTnh6HddaAEYao493hZ9u2MA8nQ3aSboC8FPrSWCohjDoYBkSAh/KXQeFnVUbYkc18BQl6/gR1qrVq7gAb3wUahm1aC83b7/9tj1Gx50HEAYklehG0lYaLj8nBNS8gBvENbNqJdpcvpuXaJRc/Bevs/EbAnw2wyqOX5j4gL0er9qx3dlX5uSoNPlekcn3SLXtB+ZglPTBLUvK+WtFXDw4KXl3PJBG52/evGnmtrfzthfa7jDyw4cP4xBB+vbt20x3bt8xd+7c4UPSvXv3+PcIdJRO0QM+xMGiHcaoeS4KOBJGad5i2qlRX3zxBYc8bldSaEV6CNei6ECMo+EzZswwFy5cyJzyXGBq4xo9cOBA8+iRXJMBWfToSkwh1KupFzuUtaPRVIZ2YwZg1uB3iNCDOm2/azPHvzxuHc6hAwcogUcOIL7vjB++8GRJ5bJ1ANrn2RY1ytoOEU1tln0eOnfuHNtDX4DWtjbmq27vXSAE8bnAjeqYC7hpQNsCxDWwz+MkVw+wTVJjM0QXIS8fhNHGU3cU2yqMeApBB8Rd1OpuZySFklhG5YC40/LXLUtrej5AY891JNsBBB0gjfSbcTnJvTbcpLSmbFN6jnp12OORp0JOCEi15FRXkq7EHUJKcyqvcE8aUoZFCj+uoLDkhfdFk+pNnhfEbho5u4B8Z5PuQkQ7HjugNlxnSF3c+C5fvswvLXH50TitBdVkLbuqAadJaDt2gc7OTv4VOvJYF1pbW+jg9RWvDyqXuw1WeB+tB/U6ReYTHPr48WO2wTvafwjuwQlobSEHfJV0ADJ2WwBv3jz5ufzLiJaWFu6j9te7DbpTkuoECeGB2xhePXOerqVpXk3SugF55nOZfO7mNOmHDbZjeWI3RKpPDlBJJEIAi8bgIUPM6NG/YqU+QNHzgI2jKrdBEqyL+AU0EOGRbh/zpUraqu0QFYiU8LJA2IkE/n+Gf9EpFPcGgHW4DgCwDrysgMMSb5p8DvhvQBugI60TweXXgltP4eMByocDKODVzC9HSFMtC24j02lfB/Lg2grVdfm84mFqcDw5Fjmrkg4/DyGR3KpUqKZ/CbS+qyfRfriGRhyjDqLrES34RfNvzFxo0rI2s3MAAAAASUVORK5CYII=
"""

class SerialFuzzTool:
    def __init__(self, master):
        self.master = master
        Fuzz_ver = "01.02.01"
        Fuzz_yr = "2025.08.04"
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