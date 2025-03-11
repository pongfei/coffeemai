<template>
  <div v-if="isLoggedIn" class="customize-page container row">
    <h1 class="mt-4">Customization</h1>

    <h2>{{ id }}</h2>
    <img src="/coffeecup.jpg" 
         alt="Coffee" class="menu-item-image">

    <!-- Slider Controls -->
    <div class="slider-container">
      <label for="sweetness">Sweetness Level: {{ sweetness }}%</label>
      <input type="range" id="sweetness" v-model="sweetness" min="0" max="150" step="50" class="slider"/>

      <label for="shots">Coffee Shots: {{ shots }}</label>
      <input type="range" id="shots" v-model="shots" min="1" max="3" step="1" class="slider"/>

    </div>

    <div class="order">
      <button @click="placeOrder" class="order-button">Order</button>
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
      //checkcup
      const response = await axios.post('http://192.168.58.32:5000/checkcup')
      if (!response.data.success) {
        alert("Please place a cup");
        throw new Error(response.data.message);
      }

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

        const response = await axios.post('http://192.168.58.32:5000/control', {
          milk: order.milk,
          sugar: order.sweetness,  
          shots: order.shots,
        });

        if (!response.data.success) {
          throw new Error(response.data.message);
        }

        await addDoc(collection(db, 'orders'), order);
        console.log('Order placed successfully.');
        this.$router.replace("/DonePage");

      } catch (error) {
        console.error('Error placing order:', error);
        this.errorMessage = 'Failed to place the order. Please try again.';
      }
    },
  },
};
</script>

<style>


</style>