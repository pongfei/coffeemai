from flask import Flask, request, jsonify
from flask_cors import CORS
import RPi.GPIO as GPIO
from time import sleep
import time
import smbus

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins="*")  # Enable CORS

# Set up GPIO
GPIO.setmode(GPIO.BOARD)
#GPIO.setWarnings(False)
LED_PIN = 3            # Define the GPIO pin connected to the LED
GPIO.setup(LED_PIN, GPIO.OUT)  # Set the LED pin as an output
GPIO.output(LED_PIN, GPIO.HIGH)
waterpin = 40
GPIO.setup(waterpin, GPIO.OUT) #water pump dc
GPIO.output(waterpin, GPIO.LOW)
pot = 29
GPIO.setup(pot,GPIO.OUT) #tack tack
u = GPIO.PWM(pot, 80)

dc = 21 #servo for dc
GPIO.setup(dc, GPIO.OUT)
s = GPIO.PWM(dc, 80)
mix = 35
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

TRIG = 16
ECHO = 18
GPIO.setup(TRIG, GPIO.OUT)
GPIO.output(TRIG, GPIO.LOW)
GPIO.setup(ECHO, GPIO.IN)

#for temp
ADS1115_ADDRESS = 0x48
CONFIG_REG = 0x01
CONVERSION_REG = 0x00
GAIN = 1
bus = smbus.SMBus(1)

def read_adc(channel):
    config = [0xC0 | (channel << 4), 0x83]
    bus.write_i2c_block_data(ADS1115_ADDRESS, CONFIG_REG, config)
    time.sleep(0.1)
    result = bus.read_i2c_block_data(ADS1115_ADDRESS, CONVERSION_REG, 2)
    raw_adc = (result[0] << 8) | result[1]
    return raw_adc

def get_temp(adc_val):
    voltage = adc_val * (3.3 / 32767)
    temp = voltage * 200
    return temp

#adc_val = read_adc(0)
#temp = get_temp(adc_val)
#print("Temp: {:.2f} C".format(temp))
        
def setUp():
    GPIO.setmode(GPIO.BOARD)
    LED_PIN = 3            # Define the GPIO pin connected to the LED
    GPIO.setup(LED_PIN, GPIO.OUT)  # Set the LED pin as an output
    GPIO.output(LED_PIN, GPIO.HIGH)
    waterpin = 40
    GPIO.setup(waterpin, GPIO.OUT) #water pump dc
    GPIO.output(waterpin, GPIO.LOW)
    pot = 29
    GPIO.setup(pot,GPIO.OUT) #tack tack
    
#     u = GPIO.PWM(pot, 80)

    dc = 21
    GPIO.setup(dc, GPIO.OUT)
    s.ChangeDutyCycle(3)            

#     s = GPIO.PWM(dc, 80)
    mix = 35
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

@app.route('/checkcup', methods=['POST'])
def checkcup():
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)
    
    pulse_start = time.time()
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        
    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 34300)/2
    distance = round(distance, 2)
    print(distance)
    
    if distance > 20:
        return jsonify({"success": False, "message": "No cup at the station"})
    return jsonify({"success": True})
    

# Endpoint to handle POST requests
@app.route('/control', methods=['POST'])
def control():
    setUp()
    #if checkcup() > 20:
       # return jsonify({"success": False, "message": "No cup at the station"}), 600
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
        t.ChangeDutyCycle(6)
        sleep(2)
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
        t.ChangeDutyCycle(10)
        sleep(2)
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
        t.ChangeDutyCycle(14)
        sleep(2)
        t.ChangeDutyCycle(17.5)
        sleep(2)
        t.stop()

        while(time.time()-ts<35):
            sleep(1)
            print(time.time()-ts)
        u.ChangeDutyCycle(smin)
        #read temp
        adc_val = read_adc(0)
        temp = get_temp(adc_val)
        #print("Temp: {:.2f} C".format(temp))
        
        #GPIO.output(waterpin, GPIO.HIGH)
        print("start water")
        sleep(30)
        GPIO.output(waterpin, GPIO.LOW)
        print("water")
        u.stop()

        s.start(0)
        s.ChangeDutyCycle(smin)
        sleep(2)
        s.ChangeDutyCycle(smin+4)
        sleep(2)
        s.ChangeDutyCycle(smin+5.5)
        print("down")
        a.start(0)
        print("start mix")
        a.ChangeDutyCycle(80)
        sleep(10)
        s.ChangeDutyCycle(smin+7)
        print("up")
#         a.start(0)
        print("start mix2")
#         a.ChangeDutyCycle(80)
        sleep(10)
#         a.stop()
#         print("stop mix")
#         sleep(2)
       
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





