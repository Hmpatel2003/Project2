#Huzaifa Patel
#100866869

import socket
import json
import time
import subprocess

# Create a socket
sock = socket.socket()
print("Socket created ...")

# Set the port and bind the socket to a specific IP address and port
port = 5000
sock.bind(('192.168.0.141', port))
sock.listen(5)

print('Socket is listening...')
c, addr = sock.accept()
print('Got connection from', addr)  # Locks to client IP

# Function to run a vcgencmd command and return its output
def get_vcgen_cmd_output(cmd):
    result = subprocess.run(["vcgencmd", cmd], capture_output=True, text=True)
    return result.stdout.strip()

# Main function to gather system information and send it to the client
def main():
    for iteration in range(50):  # Repeat the process 50 times
        # Get GPU temperature using vcgencmd
        gpu_temp = get_vcgen_cmd_output("measure_temp")
        
        # Get CPU temperature using vcgencmd
        cpu_temp = get_vcgen_cmd_output("measure_temp")

        # Get voltage using vcgencmd
        volts = get_vcgen_cmd_output("measure_volts")

        # Get CPU frequency using vcgencmd
        cpu_freq = get_vcgen_cmd_output("measure_clock arm")

        # Get memory usage using vcgencmd
        mem_usage = get_vcgen_cmd_output("get_mem arm")

        # Get disk space using df command
        disk_space = subprocess.check_output(["df", "/"]).decode("utf-8")
        
        # Get CPU clock speed using vcgencmd
        clock_speed = get_vcgen_cmd_output("measure_clock arm")

        # Get CPU speed using vcgencmd
        cpu_speed = get_vcgen_cmd_output("get_config arm_freq")

        # Prepare the data in a dictionary
        data = {
            "thing": [{"temp": cpu_temp}],
            "volts": volts,
            "temp-core": gpu_temp,
            "cpu-freq": cpu_freq,
            "memory-usage": mem_usage,
            "clock_speed": clock_speed,
            "cpu_speed": cpu_speed,
            "disk-space": disk_space
        }

        # Convert the dictionary to a JSON-formatted string with indentation
        json_data = json.dumps(data, indent=4)

        # Send the JSON data to the client
        c.send(json_data.encode())

        # Pause for 2 seconds before the next iteration
        time.sleep(2)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Bye....")
        exit()

