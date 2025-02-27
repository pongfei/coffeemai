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

    <p v-if="errorMessage">{{ errorMessage }}</p>
  </div>
</template>

<script>
import { getAuth, onAuthStateChanged } from "firebase/auth";
import { ref, onMounted } from "vue";
import { getFirestore, doc, getDoc, collection, addDoc } from "firebase/firestore";
import { db } from "../main";
import axios from "axios";

export default {
  name: "Recommendation",
  data() {
    return {
      userEmail: "",
      errorMessage: "",
      coffee: {
        menu: "",
        shots: 1,
        sweetness: 100,
        milk: 0
      },
    };
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

    async placeOrder() {
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

      try {
        if (!confirm("Do you wish to proceed?")) {
          console.log("User canceled.");
          return;
        }

        //pi code here
        const response = await axios.post('http://192.168.58.32:5000/control', {
          milk: order.milk,
          sugar: order.sweetness,
          shots: order.shots,
        });
        
        if (!response.data.success) {
          throw new Error(response.data.message);
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

        await addDoc(collection(db, "orders"), order);
        console.log("Order placed successfully.");
        this.$router.replace("/WaitingPage");

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
  },
};
</script>

<style>
.slider-container {
  margin: 10px 0;
}


</style>
