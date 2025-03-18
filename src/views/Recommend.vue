<template>
  <div class="customize-page mt-5 container row">
    <h1 class="mt-4">Recommend</h1>

    <h2>{{coffee.menu}}</h2> 
    <img
      src="/coffeecup.jpg"
      alt="Coffee"
      class="menu-item-image"
    />

    <div class="slider-container">
      <label for="shots">Coffee Shots: {{ coffee.shots }}</label>
    </div>

    <div class="slider-container">
      <label for="sweetness">Sweetness Level: {{ coffee.sweetness }}</label>
    </div>

    <button @click="placeOrder" class="order-button">Order</button>
    <button @click="toMenu" class="button" >Main Menu</button>

    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<script>
import { getAuth, onAuthStateChanged } from "firebase/auth";
import { getFirestore, doc, getDoc, collection, addDoc, writeBatch } from "firebase/firestore";
import { db } from "../main";
import axios from "axios";
import Swal from "sweetalert2";


export default {
  name: "Recommendation",
  data() {
    return {
      userEmail: "",
      errorMessage: "",
      coffee: {
        menu: "Espresso",
        shots: 1,
        sweetness: 100,
        milk: 0
      },
      stocks: {
        coffee: 0,
        sugar: 0,
        cream: 0,
        water: 0
      }
    }
  },

  methods: {
    async fetchUser() {
      const auth = getAuth();
      const user = auth.currentUser;

      if (user) {
        this.userEmail = user.email;
        console.log("User email: ", this.userEmail);

        const userDoc = await getDoc(doc(db, "recommendations", this.userEmail));
        if (userDoc.exists()) {
          this.coffee = userDoc.data() || {};
        }
      } else {
        console.log("No user found in recommend page");
      }
    },
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
      // checkcup
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

      const auth = getAuth();
      const user = auth.currentUser;

      if (!user) {
        this.errorMessage = "You must be logged in to place an order.";
        return;
      }

      const order = {
        email: user.email,
        menu: this.coffee.menu,
        sweetness: this.coffee.sweetness,
        shots: this.coffee.shots,
        timestamp: new Date(),
        milk: this.coffee.milk || 0
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
        const { isConfirmed } = await Swal.fire({
          title: "Do you wish to proceed?",
          icon: "warning",
          showCancelButton: true,
          confirmButtonText: "Yes, proceed",
          cancelButtonText: "Cancel",
        });

        if (!isConfirmed) {
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

        await addDoc(collection(db, "orders"), order);
        console.log("Order placed successfully.");
        this.$router.replace("/DonePage");

      } catch (error) {
        console.error("Error placing order:", error);
        this.errorMessage = "Failed to place the order. Please try again.";
      }
    },

    toMenu() {
      this.$router.replace("/menu");
    },
  },
  created() {
    this.fetchUser();
    this.fetchStocks();
  },

};
</script>

<style>
.slider-container {
  margin: 10px 0;
}


</style>
