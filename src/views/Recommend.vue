<template>
  <div>
    <h1>Menu Recommendation</h1>
    
    <!-- User enters their email -->
    <input v-model="userEmail" placeholder="Enter your email" />

    <!-- Button to trigger recommendation fetch -->
    <button @click="getRecommendation">Get Recommendation</button>

    <!-- Display the recommendation from Flask -->
    <p v-if="recommendation">Recommended Menu: {{ recommendation }}</p>

    <!-- Error message if something goes wrong -->
    <p v-if="errorMessage">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios';
import { getAuth } from 'firebase/auth';
import { onMounted } from "vue";

export default {
  data() {
    return {
      userEmail: '',          // User's input for the email
      recommendation: '',     // Recommendation from the backend
      errorMessage: ''        // Error message if the API call fails
    };
  },
  methods: {
    async fetchUser() {
      const auth = getAuth();
      const user = auth.currentUser;

      if (user) {
        this.userEmail = user.email;  // Correctly assign userEmail using 'this'
        console.log("User email: ", this.userEmail);

      } else {
        console.log("No user found in recommend page");
      }
    }
  },
  created() {
    this.fetchUser();  // Use 'created' lifecycle hook to call fetchUser
  }
};
</script>