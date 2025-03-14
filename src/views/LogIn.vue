<template>
    <div class="login-container">
      <div class="image-side">
        <img src="https://img.freepik.com/free-photo/delicious-coffee-beans-cup_23-2150691429.jpg" alt="Coffee" class="background-image" />
        <p class="quote">"Espress Yourself."</p>
      </div>
      <div class="form-side">
        <h2> Welcome Back </h2>
        <br>
        <p>Enter your account credentials to view your orders</p>
        <form @submit.prevent="login"> <!-- this calls login method--> 
          <div class="input-group">
            <label for="email">Email</label>
            <input type="email" id="email" v-model="formData.email" placeholder = "email " required />
            <!-- <input type ="something" id="something" v-model="formData" placeholder="something"> -->
          </div>
          <div class="input-group">
            <label for="password">Password</label>
            <input type="password" id="password" v-model="formData.password" placeholder = "password "required />
          </div>
          <button type="submit" class="login-button">Log In</button>
        </form>
        <div class="social-login">
          <!-- <button class="social-button google-button" @click="loginGoogle">Sign in with Google</button> -->
        </div>
        <div class="signup">
          <p>Don't have an account? <router-link to="/signup">Sign Up</router-link></p>
        </div>
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
      </div>
    </div>
  </template>

  <script>
import { getAuth, signInWithEmailAndPassword, signOut } from 'firebase/auth';
import { getFirestore, doc, getDoc, setDoc, onSnapshot } from 'firebase/firestore';
// const auth = getAuth();

// router.beforeEach((to, from, next) => {
//   const user = auth.currentUser;
//   if(to.path == '/Login' && user){
//     this.$router.replace('/menu')
//   }
// });

export default {
  name: 'LogIn',
  data() {
    return {
      formData: {
        email: '',
        password: ''
      },
      errorMessage: '',
      xhrRequest: false,
      globalSessionActive: false, // Track session status locally
    };
  },
  methods: {
    async login() {
      this.errorMessage = '';
      const auth = getAuth();
      const db = getFirestore();
      const globalSessionRef = doc(db, 'globalSession', 'currentSession');

      try {
        // Check if any user is currently logged in
        const sessionSnap = await getDoc(globalSessionRef);
        if (sessionSnap.exists() && sessionSnap.data().isLoggedIn) {
          this.errorMessage = 'Another user is currently logged in. Please wait for them to log out before you can log in.';
          return;
        }

        // Sign in the user
        this.xhrRequest = true;
        const userCredential = await signInWithEmailAndPassword(auth, this.formData.email, this.formData.password);

        // Update global session tracker
        await setDoc(globalSessionRef, { isLoggedIn: true, email: this.formData.email }, { merge: true });
        
        // Redirect to the menu page
        this.$router.replace('/Recommend');
      } catch (error) {
        this.errorMessage = error.message;
      } finally {
        this.xhrRequest = false;
      }
    },
    async logout() {
      const auth = getAuth();
      const user = auth.currentUser;
      const db = getFirestore();
      const globalSessionRef = doc(db, 'globalSession', 'currentSession');

      if (user) {
        // Clear the global session tracker
        await setDoc(globalSessionRef, { isLoggedIn: false }, { merge: true });

        // Sign out the user
        await signOut(auth);
        console.log('User signed out');
      }
    },
    monitorGlobalSession() {
      const db = getFirestore();
      const globalSessionRef = doc(db, 'globalSession', 'currentSession');

      // Listen for changes to the global session
      onSnapshot(globalSessionRef, (doc) => {
        if (doc.exists()) {
          this.globalSessionActive = doc.data().isLoggedIn;
        }
      });
    }
  },
  created() {
    // Listen for global session changes when the component is created
    this.monitorGlobalSession();
  }
};
</script>


  
  <style scoped>

  </style>
  