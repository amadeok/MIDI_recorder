import os
import signal
import time

# Replace with the actual PID of the process you want to send the signal to
pid = int(input("Enter the PID of the process to send the signal to: "))

# Wait for a few seconds to give you time to start the signal handler script
print("Waiting for 5 seconds before sending the signal...")
time.sleep(1)

# Send the SIGINT signal to the process
os.kill(pid, signal.SIGTERM)

print(f"Sent SIGINT to process {pid}")