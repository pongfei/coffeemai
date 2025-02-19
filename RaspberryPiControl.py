from flask import Flask, request, jsonify
from flask_cors import CORS
import RPi.GPIO as GPIO
from time import sleep
import time

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS

# Set up GPIO
GPIO.setmode(GPIO.BOARD)
#GPIO.setWarnings(False)
LED_PIN = 3            # Define the GPIO pin connected to the LED
GPIO.setup(LED_PIN, GPIO.OUT)  # Set the LED pin as an output
GPIO.output(LED_PIN, GPIO.HIGH)
waterpin = 19
GPIO.setup(waterpin, GPIO.OUT) #water pump dc
GPIO.output(waterpin, GPIO.LOW)
pot = 29
GPIO.setup(pot,GPIO.OUT) #tack tack
u = GPIO.PWM(pot, 80)

dc = 21
GPIO.setup(dc, GPIO.OUT)
s = GPIO.PWM(dc, 80)
mix = 22
GPIO.setup(mix, GPIO.OUT)
GPIO.output(mix, GPIO.LOW)


cup = 23
GPIO.setup(cup, GPIO.OUT)
t = GPIO.PWM(cup, 80)
t.ChangeDutyCycle(18)
#servo
s_shot = 11
s_milk = 13
s_sugar = 15
GPIO.setup(s_shot,GPIO.OUT)
GPIO.setup(s_milk,GPIO.OUT)
GPIO.setup(s_sugar,GPIO.OUT)
p = GPIO.PWM(s_shot, 80)
q = GPIO.PWM(s_milk, 80)
r = GPIO.PWM(s_sugar, 80)

smin=3 #most right servo
smax=19 #most left servo

# Endpoint to handle POST requests
@app.route('/control', methods=['POST'])
def control():
    try:
        data = request.json  # Parse JSON body
        milk = int(data.get('milk'))
        water = 5
        shots = int(data.get('shots'))
        sugar = int(data.get('sugar'))

        if None in (milk, shots, sugar):
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        print(f"Order received -> Milk: {milk}, Shots: {shots}, Water: {water}, Sugar: {sugar}")
        t.start(0)
        t.ChangeDutyCycle(smin)
        u.start(0)
        u.ChangeDutyCycle(smin+1)
        ts = time.time()
        
        i=0
        q.start(0)

        for i in range(milk):
            print("start")
#             q.start(0)
            q.ChangeDutyCycle(smin)
            sleep(2)
            q.ChangeDutyCycle(smax)
            sleep(2)
            q.ChangeDutyCycle(smin)            
            sleep(2)
            print("milk")
#             q.stop()
        q.stop()
        t.ChangeDutyCycle(8)
        print("station 2")

        i=0
        p.start(0)
        
        for i in range(shots):
            print("start shot")
#             p.start(0)
            p.ChangeDutyCycle(smin)
            sleep(2)
            p.ChangeDutyCycle(smax)
            sleep(2)
            p.ChangeDutyCycle(smin)
            sleep(2)
            print("shots")
#             p.stop()
        p.stop()
        t.ChangeDutyCycle(12)
        print("station 3")
        
        sugar = int(sugar/50)
        i=0
        r.start(0)

        for i in range(sugar):
            print("start")
#             r.start(0)
            r.ChangeDutyCycle(smin)
            sleep(2)
            r.ChangeDutyCycle(smax)
            sleep(2)
            r.ChangeDutyCycle(smin)            
            sleep(2)
            print("sugar")
#             r.stop()
        t.ChangeDutyCycle(18)
        sleep(2)
        r.stop()
        t.stop()

        while(time.time()-ts<30):
            sleep(1)
        u.ChangeDutyCycle(smin)
        GPIO.output(waterpin, GPIO.HIGH)
        sleep(water)
        GPIO.output(waterpin, GPIO.LOW)
        print("water")
    
        s.start(0)
        s.ChangeDutyCycle(smin)
        sleep(2)
        s.ChangeDutyCycle(smin+8)
        GPIO.output(mix, GPIO.HIGH)
        sleep(water)
        GPIO.output(mix, GPIO.LOW)
        sleep(2)
        s.ChangeDutyCycle(smin)            
        sleep(2)
        print("mix")
        s.stop()
        u.stop()
        #return jsonify({"success": True, "message": "mix done"})
        GPIO.output(LED_PIN, GPIO.LOW)
        
        print("all done")
        # response back to pi if success
        
        return jsonify({
            "success": True,
            "message": f"Order received successfully: Milk={milk}, Shots={shots}, Water={water}, Sweetness={sweetness}"
        })
    
    


    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500

# Clean up GPIO when the app stops
@app.route('/cleanup', methods=['POST'])
def cleanup():
    GPIO.cleanup()  # Reset GPIO settings
    return jsonify({"success": True, "message": "GPIO cleaned up"})

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)  # Accessible on all network interfaces
    except KeyboardInterrupt:
        GPIO.cleanup()  # Clean up GPIO on exit
        
#def servo(s_name):
#    p = GPIO.PWM(s_name, 100)
#     p.start(0)
# 
#     p.ChangeDutyCycle(smin)
#     sleep(5)
#     p.ChangeDutyCycle(smax)
#     sleep(5)
#     p.ChangeDutyCycle(smin)
#     
#     print(s_name)
#     p.stop()
    

