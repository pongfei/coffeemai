<template>
  <div v-if="isLoggedIn" class="customize-page">
    <h1>Customize Your Drink</h1>

    <p>{{ id }}</p>
    <img src="https://img.freepik.com/premium-vector/cup-coffee-with-words-i-love-you-it_1166763-8437.jpg?w=826" 
         alt="Description of the image" class="menu-item-image">

    <!-- Slider Controls -->
    <div class="slider-container">
      <label for="sweetness">Sweetness Level: {{ sweetness }}%</label>
      <input type="range" id="sweetness" v-model="sweetness" min="0" max="150" step="50"/>

      <label for="shots">Coffee Shots: {{ shots }}</label>
      <input type="range" id="shots" v-model="shots" min="1" max="3" step="1"/>

      <!-- <label for="milk">Milk Level: {{ milk }}</label>
      <input type="range" id="milk" v-model="milk" min="0" max="3" step="1"/> -->

      <!-- <label for="water">Water Level: {{ water }}</label>
      <input type="range" id="water" v-model="water" min="1" max="5" step="1"/> -->
    </div>

    <div class="order">
      <button @click="placeOrder">Order</button>
    </div>

    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { collection, addDoc } from "firebase/firestore";
import { db } from '../main';
import axios from 'axios';

export default {
  name: 'Customize',
  data() {
    return {
      id: this.$route.params.id,
      sweetness: this.$route.query.sweetness ? parseInt(this.$route.query.sweetness) : 50,
      shots: this.$route.query.shots ? parseInt(this.$route.query.shots) : 1,
      milk: this.$route.query.milk ? parseInt(this.$route.query.milk) : 0,
      water: this.$route.query.water ? parseInt(this.$route.query.water) : 1,
      isLoggedIn: false,
      auth: getAuth(),
      errorMessage: '',
    };
  },

  created() {
    onAuthStateChanged(this.auth, (user) => {
      if (user) {
        this.isLoggedIn = true;
      } else {
        this.isLoggedIn = false;
        this.$router.push('/login');
      }
    });
  },

  methods: {
    async placeOrder() {
      const user = this.auth.currentUser;
      if (!user) {
        this.errorMessage = 'You must be logged in to place an order.';
        return;
      }

      const order = {
        email: user.email,
        menu: this.id,
        sweetness: this.sweetness,
        shots: this.shots,
        milk: this.milk,
        water: this.water,
        timestamp: new Date(),
      };

      try {
        if (!confirm("Do you wish to proceed?")) {
          console.log("User canceled.");
          return;
        }

        const response = await axios.post('http://172.20.10.11:5000/control', {
          milk: order.milk,
          sugar: order.sweetness,  // Fix: Changed from sweetness to sugar
          shots: order.shots,
          water: order.water,
        });

        if (!response.data.success) {
          throw new Error(response.data.message);
        }

        await addDoc(collection(db, 'orders'), order);
        console.log('Order placed successfully.');

        this.$router.push({
          name: 'WaitingPage',
          params: { id: this.id },
          query: {
            sweetness: this.sweetness,
            shots: this.shots,
            milk: this.milk,
            water: this.water,
          },
        });

      } catch (error) {
        console.error('Error placing order:', error);
        this.errorMessage = 'Failed to place the order. Please try again.';
      }
    },
  },
};
</script>

<style>

body {
  background-size: cover;
  background-position: center;
  margin: 0;
  font-family: Arial, sans-serif;
}

.customize-page {
  background-color: rgba(255, 255, 255, 0.95);
  padding: 20px;
  margin: 50px auto;
  width: 100%;
  max-width: 600px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.menu-item-image {
  width: 100%;
  height: auto;
  max-height: 300px;
  object-fit: cover;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin: 20px 0;
}

.slider-container {
  margin-top: 20px;
}

.slider-container label {
  display: block;
  margin-bottom: 10px;
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

input[type="range"] {
  width: 100%;
  height: 10px;
  background: linear-gradient(90deg, #4CAF50 0%, #FF9800 100%);
  border-radius: 5px;
  outline: none;
  opacity: 0.8;
  transition: opacity .2s;
}

input[type="range"]:hover {
  opacity: 1;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 24px;
  height: 24px;
  background: #4CAF50;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s ease, transform 0.3s ease;
}

input[type="range"]::-webkit-slider-thumb:hover {
  background-color: #45a049;
  transform: scale(1.2);
}

input[type="range"]::-moz-range-thumb {
  width: 24px;
  height: 24px;
  background: #4CAF50;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s ease, transform 0.3s ease;
}

input[type="range"]::-moz-range-thumb:hover {
  background-color: #45a049;
  transform: scale(1.2);
}

.menu-item-image {
  width: 100%; /* Ensures the image takes up the full width of its container */
  height: auto; /* Maintains the aspect ratio */
  max-height: 300px; /* Limits the maximum height to prevent it from stretching */
  object-fit: cover; /* Ensures the image fills the container while cropping any overflow */
  border-radius: 15px; /* Keeps rounded corners */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Adds a subtle shadow */
  margin: 20px 0;
}

button {
  background-color: #763f00;
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 20px 0;
  cursor: pointer;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s, transform 0.3s;
}

button:hover {
  background-color: #45a049;
  transform: scale(1.05);
}
</style>