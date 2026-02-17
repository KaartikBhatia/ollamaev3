# ev3_robot.py

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.tools import wait
import socket

# -------------------
# SETUP
# -------------------

ev3 = EV3Brick()

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
ultra = UltrasonicSensor(Port.S4)

SAFE_DISTANCE = 200  # mm
MODE = "remote"      # "remote" or "auto"

# -------------------
# MOVEMENT FUNCTIONS
# -------------------

def move_forward(speed=400):
    left_motor.run(speed)
    right_motor.run(speed)

def move_backward(speed=400):
    left_motor.run(-speed)
    right_motor.run(-speed)

def stop():
    left_motor.stop()
    right_motor.stop()

def turn_left():
    left_motor.run_time(-400, 800)
    right_motor.run_time(400, 800)

def turn_right():
    left_motor.run_time(400, 800)
    right_motor.run_time(-400, 800)

# -------------------
# SOCKET SERVER
# -------------------

HOST = ''
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Waiting for laptop...")
conn, addr = server.accept()
print("Connected:", addr)

conn.setblocking(False)

# -------------------
# MAIN LOOP
# -------------------

while True:

    # ---- RECEIVE COMMANDS ----
    try:
        data = conn.recv(1024)
        if data:
            command = data.decode("utf-8").lower()
            print("Command:", command)

            # Mode switching
            if "auto mode" in command:
                MODE = "auto"

            elif "remote mode" in command:
                MODE = "remote"
                stop()

            # Remote movement
            if MODE == "remote":
                if "forward" in command:
                    move_forward()
                elif "backward" in command:
                    move_backward()
                elif "left" in command:
                    turn_left()
                elif "right" in command:
                    turn_right()
                elif "stop" in command:
                    stop()

    except:
        pass

    # ---- AUTONOMOUS MODE ----
    if MODE == "auto":
        distance = ultra.distance()

        if distance < SAFE_DISTANCE:
            stop()
            turn_left()
        else:
            move_forward()

    wait(50)
