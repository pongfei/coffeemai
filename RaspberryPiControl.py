from flask import Flask, request, jsonify
from flask_cors import CORS
import RPi.GPIO as GPIO
from time import sleep
import time

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins="*")  # Enable CORS

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
mix = 24
GPIO.setup(mix, GPIO.OUT)
a =GPIO.PWM(mix, 50)

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
        
def setUp():
    GPIO.setmode(GPIO.BOARD)
    LED_PIN = 3            # Define the GPIO pin connected to the LED
    GPIO.setup(LED_PIN, GPIO.OUT)  # Set the LED pin as an output
    GPIO.output(LED_PIN, GPIO.HIGH)
    waterpin = 19
    GPIO.setup(waterpin, GPIO.OUT) #water pump dc
    GPIO.output(waterpin, GPIO.LOW)
    pot = 29
    GPIO.setup(pot,GPIO.OUT) #tack tack
    
#     u = GPIO.PWM(pot, 80)

    dc = 21
    GPIO.setup(dc, GPIO.OUT)
    s.ChangeDutyCycle(3)            

#     s = GPIO.PWM(dc, 80)
    mix = 24
    GPIO.setup(mix, GPIO.OUT)


    cup = 23
    GPIO.setup(cup, GPIO.OUT)
#     t = GPIO.PWM(cup, 80)
    t.ChangeDutyCycle(17)
    #servo
    s_shot = 11
    s_milk = 13
    s_sugar = 15
    GPIO.setup(s_shot,GPIO.OUT)
    GPIO.setup(s_milk,GPIO.OUT)
    GPIO.setup(s_sugar,GPIO.OUT)
#     p = GPIO.PWM(s_shot, 80)
#     q = GPIO.PWM(s_milk, 80)
#     r = GPIO.PWM(s_sugar, 80)

    smin=3 #most right servo
    smax=19 #most left servo


# Endpoint to handle POST requests
@app.route('/control', methods=['POST'])
def control():
    setUp()
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
        u.ChangeDutyCycle(smin+2)
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
        q.stop()
        t.ChangeDutyCycle(8.5)
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
        p.stop()
        t.ChangeDutyCycle(11.75)
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
        r.stop()
        t.ChangeDutyCycle(17.5)
        sleep(2)
        t.stop()

        while(time.time()-ts<30):
            sleep(1)
            print(time.time()-ts)
        u.ChangeDutyCycle(smin)
        GPIO.output(waterpin, GPIO.HIGH)
        print("start water")
        sleep(50)
        GPIO.output(waterpin, GPIO.LOW)
        print("water")
        u.stop()

        s.start(0)
        s.ChangeDutyCycle(smin)
        sleep(2)
        s.ChangeDutyCycle(smin+4)
        sleep(2)
        s.ChangeDutyCycle(smin+8)
        print("down")
        a.start(0)
        print("start mix")
        a.ChangeDutyCycle(80)
        sleep(5)
        a.stop()
        print("stop mix")
        sleep(2)
        s.ChangeDutyCycle(smin+4)            
        sleep(2)
        s.ChangeDutyCycle(smin+2)            
        sleep(2)
        s.ChangeDutyCycle(smin)            
        sleep(2)
        s.stop()
        print("up")
        #return jsonify({"success": True, "message": "mix done"})
        GPIO.output(LED_PIN, GPIO.LOW)
        
        print("all done")
        # response back to pi if success
        
        return jsonify({
            "success": True,
            "message": f"Order received successfully: Milk={milk}, Shots={shots}, Water={water}, Sweetness={sugar}"
        })
    
    


    except Exception as e:
#         cleanup()
#         setUp()
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500

# # Clean up GPIO when the app stops
# @app.route('/cleanup', methods=['POST'])
# def cleanup():
   #     t.stop()

#     GPIO.cleanup()  # Reset GPIO settings
#     setUp()
#     return jsonify({"success": True, "message": "GPIO cleaned up"})

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)  # Accessible on all network interfaces
    except KeyboardInterrupt:
        p.stop()
        q.stop()
        r.stop()
        s.stop()
        t.stop()
        u.stop()
        GPIO.cleanup()  # Clean up GPIO on exit





