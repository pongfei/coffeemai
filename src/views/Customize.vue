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
import { getFirestore, doc, getDoc, collection, addDoc, writeBatch } from "firebase/firestore";
import { db } from '../main';
import axios from 'axios';
import Swal from 'sweetalert2';

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
      stocks: {
        coffee: 0,
        sugar: 0,
        cream: 0,
        water: 0
      }
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
    this.fetchStocks();
  },

  methods: {
    async fetchStocks() {
      let updatedStocks = { ...this.stocks }; // Clone to ensure reactivity

      for (const product of Object.keys(updatedStocks)) {
        const docRef = doc(db, "stocks", product);
        const docSnap = await getDoc(docRef);

        if (docSnap.exists()) {
          updatedStocks[product] = docSnap.data().stock; // Update cloned object
        } else {
          await setDoc(docRef, { stock: 0 });
          updatedStocks[product] = 0;
        }
      }
      this.stocks = updatedStocks; // Assign new object to trigger reactivity
      console.log("Updated stock data:", this.stocks);
  },
    async updateStocks(order) {
      const batch = writeBatch(db); // Create batch for multiple updates

      // Compute new stock values
      const newStockLevels = {
        coffee: Math.max(0, this.stocks.coffee - order.shots),
        sugar: Math.max(0, this.stocks.sugar - order.sweetness / 50),
        cream: Math.max(0, this.stocks.cream - order.milk),
        water: Math.max(0, this.stocks.water - 1) // Assuming 1 unit of water per cup
      };

      // Update Firestore stock documents
      for (const [product, newStock] of Object.entries(newStockLevels)) {
        const docRef = doc(db, "stocks", product);
        batch.update(docRef, { stock: newStock });
      }

      // Commit batch update
      await batch.commit();

      // Update local state
      this.stocks = { ...newStockLevels };
    },

    async placeOrder() {
      //checkcup
      const response = await axios.post('http://192.168.58.32:5000/checkcup')
      if (!response.data.success) {
        Swal.fire({
            title: "Cup Warning!",
            text: "Please place a cup!",
            icon: "warning",
            confirmButtonText: "OK",
          });
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

      // Check if stock is sufficient before order
      await this.fetchStocks();
      if(this.stocks.coffee < order.shots){
          Swal.fire({
            title: "Warning!",
            text: "Not enough coffee stock!",
            icon: "warning",
            confirmButtonText: "OK",
          });
          return;
      }
      if (this.stocks.sugar < order.sweetness / 50) {
        Swal.fire({
            title: "Warning!",
            text: "Not enough coffee stock!",
            icon: "warning",
            confirmButtonText: "OK",
          });        
          return;
      }
      if (this.stocks.cream < order.milk) {
        Swal.fire({
            title: "Warning!",
            text: "Not enough cream stock!",
            icon: "warning",
            confirmButtonText: "OK",
          });        
          return;
      }
      if (this.stocks.water < 1) {
        Swal.fire({
            title: "Warning!",
            text: "Not enough water stock!",
            icon: "warning",
            confirmButtonText: "OK",
          });        
          return;
      } 

      try {
        await Swal.fire({
          title: "Do you wish to proceed?",
          icon: "warning",
          showCancelButton: true,
          confirmButtonText: "Yes, proceed",
          cancelButtonText: "Cancel",
        });

        if (result.isConfirmed) {
          console.log("User confirmed.");
          // Proceed with your action
        } else {
          console.log("User canceled.");
          return;
        }
        // Deduct ingredients from stock
        await this.updateStocks(order);

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

        // await addDoc(collection(db, 'orders'), order);
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