import psutil
import time
import subprocess
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


# Target program's title
TARGET_PROGRAM = "League of Legends"
NOT_TARGET_PROGRAM = "Riot Client"
PROGRAM_DIRECTORY = os.getenv('PROGRAM_DIRECTORY')

def log(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

# Function to check if the target program is running
def is_target_running(target_title,not_target):
    not_target_open = False
    for proc in psutil.process_iter(['name', 'cmdline']):
        if proc.info.get('cmdline', []) != None:
            if target_title in " ".join(proc.info.get('cmdline', [])):
                return 1
            elif not_target in " ".join(proc.info.get('cmdline', [])):
                not_target_open = True
    if not_target_open:
        return 0
    else:
        return 2


# Main loop
log("Monitoring for the target program...")
while True:
    result = is_target_running(TARGET_PROGRAM,NOT_TARGET_PROGRAM)
    if result == 1:
        log(f"Target program '{TARGET_PROGRAM}' detected! Launching overlay...")
        subprocess.Popen(["python", PROGRAM_DIRECTORY+r"\target.py"],cwd=PROGRAM_DIRECTORY)  
        break
    elif result == 2:
        log(f"Current Program '{NOT_TARGET_PROGRAM}' closed! Stopping...")
        break
    
    time.sleep(1)  # Check every second