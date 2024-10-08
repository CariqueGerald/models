import serial
import time

# Set up serial communication with the Arduino
try:
    arduino = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust the port if necessary (e.g., ttyACM0)
    print("Connection established with Arduino.")
except Exception as e:
    print(f"Error connecting to Arduino: {e}")
    exit()

# Give time to establish the serial connection
time.sleep(2)

# Display available commands
print("Manual Control Commands:")
print("'F' - Move Forward")
print("'B' - Move Backward")
print("'L' - Turn Left")
print("'R' - Turn Right")
print("'S' - Stop")
print("'Q' - Quit the program")

# Function to send commands to the Arduino
def send_command(command):
    try:
        arduino.write(command.encode())  # Encode and send command to Arduino
        print(f"Sent command: {command}")
    except Exception as e:
        print(f"Error sending command: {e}")

# Manual control loop
try:
    while True:
        # Take user input
        command = input("Enter command: ").upper()  # Convert input to uppercase for consistency

        if command in ['F', 'B', 'L', 'R', 'S']:  # Valid commands
            send_command(command)  # Send to Arduino
        elif command == 'Q':  # Quit command
            print("Exiting manual control.")
            send_command('S')  # Stop the robot before quitting
            break
        else:
            print("Invalid command. Please use 'F', 'B', 'L', 'R', 'S', or 'Q'.")
except KeyboardInterrupt:
    print("Manual control interrupted.")

# Close the serial connection
arduino.close()
print("Serial connection closed.")
