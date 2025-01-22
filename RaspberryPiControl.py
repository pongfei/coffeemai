from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from the Vue.js frontend

@app.route('/control', methods=['POST'])
def control():
    try:
        #json into python dictionary
        data = request.json
        milk = data.get('milk')
        shots = data.get('shots')
        water = data.get('water')
        sweetness = data.get('sweetness')

        # validate the data
        if milk is None or sweetness is None or shots is None or water is None:
            return jsonify({
                "success": False,
                "message": "Missing one or more required fields: milk, shots, water, sweetness"
            }), 400

        # logging order details in console
        print(f"Order received -> Milk: {milk}, Shots: {shots}, Water: {water}, Sweetness: {sweetness}")

        # response back to pi if success
        return jsonify({
            "success": True,
            "message": f"Order received successfully: Milk={milk}, Shots={shots}, Water={water}, Sweetness={sweetness}"
        })

    except Exception as e:
        # Handle any unexpected errors
        print(f"Error: {e}")
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run Flask server on all network interfaces
