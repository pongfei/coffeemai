<template>
  <!-- <p> the drink id is {{ $route.params.id }}</p> -->
  <div v-if="isLoggedIn" class="customize-page">
    <h1>Customize Your Drink</h1>
    <img :src="imgUrl" alt="Menu Item Image" class="menu-item-image">
    <p>{{ id }}</p>

    <!-- Slider part -->
    <div class="slider-container">
      <label for="sweetness">Sweetness Level: {{ sweetness }}</label>
      <input type="range" id="sweetness" v-model="sweetness" min="0" max="5" step="1"/>

      <label for="shots">Coffee Shots: {{ shots }}</label>
      <input type="range" id="shots" v-model="shots" min="0" max="5" step="1"/>

      <label for="milk">Milk Level: {{ milk }}</label>
      <input type="range" id="milk" v-model="milk" min="0" max="5" step="1"/>

      <label for="water">Water Level: {{ water }}</label>
      <input type="range" id="water" v-model="water" min="0" max="5" step="1"/>
    </div>

    <div class="order"><button @click="placeOrder"> Order </button> </div>
  </div>
  <div v-else>
    <p>You need to log in to access this page.</p>
  </div>
</template>

<script>
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { useRouter } from 'vue-router';
import { collection, onSnapshot, doc, setDoc, updateDoc, deleteDoc, getFirestore, addDoc } from "firebase/firestore";
import { db } from '../main'; // Adjust the path if necessary


export default {
  name: 'Customize',
  data() {
    return {
      id: this.$route.params.id,
      imgUrl: this.$route.query.img,
      sweetness: parseInt(this.$route.query.sweetness),
      shots: parseInt(this.$route.query.shots),
      milk: parseInt(this.$route.query.milk),
      water: parseInt(this.$route.query.water),
      isLoggedIn: false,
      auth: getAuth(),
    };
  },

  created() {
    const router = useRouter();
    onAuthStateChanged(this.auth, (user) => {
      if (user) {
        this.isLoggedIn = true;
      } else {
        this.isLoggedIn = false;
        router.push('/login'); // Redirect to login page if not logged in
      }
    });
  },
  methods: {
    async placeOrder() {
    const order = { // creates order obj
      id: this.id,
      sweetness: this.sweetness,
      shots: this.shots,
      milk: this.milk,
      water: this.water,
      imgUrl: this.imgUrl,
      timestamp: new Date() // Optional: Add timestamp for order time
    };

    try {
      // Add the order to the Firestore "orders" collection
      const docRef = await addDoc(collection(db, 'orders'), order);
      console.log('Document written with ID: ', docRef.id);

      // Show success message or perform further actions
      alert(`Order placed with ${this.id}. Sweetness: ${this.sweetness}, Shots: ${this.shots}, Milk: ${this.milk}, Water: ${this.water}`);

      // Navigate to the waiting page or another route
      this.$router.push({
        name: 'WaitingPage',
        params: { id: this.id },
        query: {
          sweetness: this.sweetness,
          shots: this.shots,
          milk: this.milk,
          water: this.water,
        }
      });

      console.log("Order details:", order);
    } catch (e) {
      console.error('Error adding document: ', e);
    }
  }
  }
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