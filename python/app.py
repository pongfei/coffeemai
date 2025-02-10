# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import firebase_admin
# from firebase_admin import credentials, firestore

# # Initialize Flask app
# app = Flask(__name__)

# # Enable CORS to allow communication from the Vue.js frontend
# CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# # Initialize Firebase Admin SDK with your credentials
# cred = credentials.Certificate('/Users/pongfei/Desktop/MUIC/senior project/coffeemai/key.json')
# firebase_admin.initialize_app(cred)

# # Initialize Firestore
# db = firestore.client()

# # Routing for the recommendation system
# @app.route('/recommend', methods=['POST'])
# def recommend():
#     # Get the email from the POST request (sent from the Vue.js frontend)
#     data = request.get_json()
#     user_email = data.get('email')

#     if not user_email:
#         return jsonify({'error': 'No email provided'}), 400

#     try:
#         # Fetch the most recent order from Firestore for the given email
#         orders_ref = db.collection('orders').where('email', '==', user_email).order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1)
#         orders = orders_ref.stream()

#         # Extract the order data (assuming there's at least one order)
#         user_order = None
#         for order in orders:
#             user_order = order.to_dict()

#         if not user_order:
#             return jsonify({'error': 'No order found for this user'}), 404

#         # Extract relevant fields from the order
#         menu = user_order.get('menu', '')
        
#         # Mock AI logic based on the user's last ordered menu
#         if 'espresso' in menu.lower():  # Case-insensitive check for "espresso"
#             recommendation = 'Cappuccino'
#         else:
#             recommendation = 'Latte'

#         # Return the recommendation as a JSON response
#         return jsonify({'recommendation': recommendation})

#     except Exception as e:
#         print(f"Error fetching order: {e}")
#         return jsonify({'error': 'An error occurred while fetching recommendation'}), 500

# if __name__ == '__main__':
#     app.run(debug=True)