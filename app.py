from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# GPIO pin setup
motor_left_forward = 17
motor_left_backward = 18
motor_right_forward = 22
motor_right_backward = 23
pump_pin = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_left_forward, GPIO.OUT)
GPIO.setup(motor_left_backward, GPIO.OUT)
GPIO.setup(motor_right_forward, GPIO.OUT)
GPIO.setup(motor_right_backward, GPIO.OUT)
GPIO.setup(pump_pin, GPIO.OUT)

def stop():
    GPIO.output(motor_left_forward, False)
    GPIO.output(motor_left_backward, False)
    GPIO.output(motor_right_forward, False)
    GPIO.output(motor_right_backward, False)

def forward():
    GPIO.output(motor_left_forward, True)
    GPIO.output(motor_right_forward, True)
    GPIO.output(motor_left_backward, False)
    GPIO.output(motor_right_backward, False)

def backward():
    GPIO.output(motor_left_forward, False)
    GPIO.output(motor_right_forward, False)
    GPIO.output(motor_left_backward, True)
    GPIO.output(motor_right_backward, True)

def left():
    GPIO.output(motor_left_forward, False)
    GPIO.output(motor_right_forward, True)
    GPIO.output(motor_left_backward, True)
    GPIO.output(motor_right_backward, False)

def right():
    GPIO.output(motor_left_forward, True)
    GPIO.output(motor_right_forward, False)
    GPIO.output(motor_left_backward, False)
    GPIO.output(motor_right_backward, True)

def spray_on():
    GPIO.output(pump_pin, True)

def spray_off():
    GPIO.output(pump_pin, False)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/action', methods=['POST'])
def action():
    command = request.form['command']
    if command == 'forward':
        forward()
    elif command == 'backward':
        backward()
    elif command == 'left':
        left()
    elif command == 'right':
        right()
    elif command == 'stop':
        stop()
    elif command == 'spray_on':
        spray_on()
    elif command == 'spray_off':
        spray_off()
    return ('', 204)

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        GPIO.cleanup()
