import tkinter as tk
import serial
import serial.tools.list_ports

# Create the main window FIRST
root = tk.Tk()
root.title("Blinking Blue Square")

# Helper to get available serial ports
available_ports = [port.device for port in serial.tools.list_ports.comports()]
if not available_ports:
    available_ports = ['COM1']  # fallback

baudrates = [9600, 19200, 38400, 57600, 115200]

selected_port = tk.StringVar(value=available_ports[0])
selected_baud = tk.IntVar(value=baudrates[0])
ser = None

# Function to connect to serial port
def connect_serial():
    global ser
    port = selected_port.get()
    baud = selected_baud.get()
    try:
        ser = serial.Serial(port, baud, timeout=1)
        status_label.config(text=f"Connected to {port} @ {baud} baud", fg="green")
    except serial.SerialException:
        ser = None
        status_label.config(text=f"Could not open serial port {port}", fg="red")

# Serial port selection frame
serial_frame = tk.Frame(root)
serial_frame.pack(side=tk.TOP, pady=5)

# Port dropdown
port_label = tk.Label(serial_frame, text="Port:")
port_label.pack(side=tk.LEFT)
port_menu = tk.OptionMenu(serial_frame, selected_port, *available_ports)
port_menu.pack(side=tk.LEFT, padx=5)

# Baudrate dropdown
baud_label = tk.Label(serial_frame, text="Baudrate:")
baud_label.pack(side=tk.LEFT)
baud_menu = tk.OptionMenu(serial_frame, selected_baud, *baudrates)
baud_menu.pack(side=tk.LEFT, padx=5)

# Connect button
connect_button = tk.Button(serial_frame, text="Connect", command=connect_serial)
connect_button.pack(side=tk.LEFT, padx=10)

def disconnect_serial():
    global ser
    if ser and ser.is_open:
        ser.close()
        ser = None
        status_label.config(text="Disconnected", fg="red")

disconnect_button = tk.Button(serial_frame, text="Disconnect", command=disconnect_serial)
disconnect_button.pack(side=tk.LEFT, padx=10)

# Status label
status_label = tk.Label(serial_frame, text="Not connected", fg="red")
status_label.pack(side=tk.LEFT, padx=10)

# Create a canvas widget
canvas = tk.Canvas(root, width=300, height=300)
canvas.pack()

# Draw a blue square outline (x1, y1, x2, y2)
square = canvas.create_rectangle(50, 50, 250, 250, outline="blue", width=3)

blinking = False
blink_job = None

# Function to handle blinking
def blink():
    global blink_job
    if not blinking:
        return
    current_fill = canvas.itemcget(square, 'fill')
    if current_fill == "blue":
        canvas.itemconfig(square, fill="")
    else:
        canvas.itemconfig(square, fill="blue")
    blink_job = root.after(500, blink)

def start_blink():
    global blinking, blink_job
    blinking = True
    if ser and ser.is_open:
        try:
            ser.write(b'blink\n')
        except serial.SerialException:
            status_label.config(text="Serial write failed.", fg="red")
    if blink_job is None:
        blink()

def stop_blink():
    global blinking, blink_job
    blinking = False
    if blink_job is not None:
        root.after_cancel(blink_job)
        blink_job = None
    canvas.itemconfig(square, fill="")  # Just outline

# Frame for buttons
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, pady=10)

blink_button = tk.Button(button_frame, text="Blink", command=start_blink)
blink_button.pack(side=tk.LEFT, padx=10)

solid_button = tk.Button(button_frame, text="Solid", command=stop_blink)
solid_button.pack(side=tk.LEFT, padx=10)

# Start with just outline
stop_blink()

# Start the GUI event loop
root.mainloop()

# Close serial port on exit
if ser and ser.is_open:
    ser.close()
