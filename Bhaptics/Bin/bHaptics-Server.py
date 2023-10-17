import socket
import os
from tendo import singleton
from bHaptics__data import better_haptic_player as bhaptics_player
import pystray
from PIL import Image
import threading
import psutil
import sys
import time

sys.stderr = open('nul', 'w')

me = singleton.SingleInstance()
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
bhaptics_player.initialize()

# Register Tact Patterns
print("register tact_Explosion")
bhaptics_player.register("tact_Explosion", "bHaptics__data//Tact Files//Explosion.tact")

print("register tact_Grenade")
bhaptics_player.register("tact_Grenade", "bHaptics__data//Tact Files//Grenade.tact")

# Define the function to be triggered
def tact_Explosion():
    print("submit tact_Explosion")
    bhaptics_player.submit_registered("tact_Explosion")

def tact_Grenade():
    print("submit tact_Grenade")
    bhaptics_player.submit_registered("tact_Grenade")

# Server Socket Connection
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 12345)
server_socket.bind(server_address)

server_socket.listen(1)
print("Server is listening for connections...")

def handle_connections():
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        data = client_socket.recv(1024).decode('utf-8')

        # Function Triggering Socket Messages
        if data == "Explosion":
            tact_Explosion()

        if data == "Grenade":
            tact_Grenade()

        if data == "Exit":
            Exit_App()

        client_socket.close()

socket_thread = threading.Thread(target=handle_connections)
socket_thread.daemon = True
socket_thread.start()

# System Tray Icon
def on_tray_click(icon, item):
    if item.text == 'Exit':
        Exit_App()

def Exit_App():
    icon.stop()
    os._exit(0)

# Check if the 'BhapticsPlayer.exe' process is running
def is_process_running(process_name):
    for process in psutil.process_iter(attrs=['name']):
        if process.info['name'] == process_name:
            return True
    return False

def process_check_thread():
    process_name = "BhapticsPlayer.exe"
    while True:
        if not is_process_running(process_name):
            os.system('cls' if os.name == 'nt' else 'clear')
            sys.stderr = open('nul', 'w')
            Exit_App()

        time.sleep(1)   # Check Process Loop

# Create the system tray icon
image = Image.open("bhaptics.png") 
menu = pystray.Menu(pystray.MenuItem('Exit', on_tray_click))
icon = pystray.Icon("name", image, menu=menu)

# Create a thread for the process check
process_check_thread = threading.Thread(target=process_check_thread)
process_check_thread.daemon = True

process_check_thread.start()
icon.run()
