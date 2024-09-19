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
        this.$router.replace('/menu');
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
  .login-container {
    display: flex;
    height: 100vh;
  }
  
  .image-side {
    flex: 1;
    position: relative;
    background: url('https://img.freepik.com/free-photo/delicious-coffee-beans-cup_23-2150691429.jpg') no-repeat center center;
    background-size: cover;
  }
  
  .background-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .quote {
    position: absolute;
    bottom: 20px;
    left: 20px;
    color: white;
    font-size: 24px;
  }
  
  .form-side {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 40px;
    padding-top: 100px;
    background: white;
  }
  
  .form-side h2 {
    margin-bottom: 10px;
  }
  
  .form-side p {
    margin-left: 20%;
    margin-right: 15%;
    margin-bottom: 20px;
    color: #666;
  }
  
  .input-group {
    width: 100%;
    margin-bottom: 20px;
  }
  
  .input-group label {
    display: block;
    margin-bottom: 5px;
    color: #333;
  }
  
  .input-group input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
  }
  
  .forgot-password {
    width: 100%;
    text-align: right;
    margin-bottom: 20px;
  }
  
  .forgot-password a {
    color: #007bff;
    text-decoration: none;
  }
  
  .login-button {
    width: 100%;
    padding: 10px;
    background: #28a745;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background 0.3s;
  }
  
  .login-button:hover {
    background: #218838;
  }
  
  .social-login {
    margin-top: 20px;
    text-align: center;
  }
  
  .social-login p {
    margin-bottom: 10px;
  }
  
  .social-button {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background 0.3s;
  }
  
  .google-button {
    background: #db4437;
    color: white;
  }
  
  .social-button:hover {
    opacity: 0.8;
  }
  
  .signup {
    margin-top: 20px;
  }
  
  .signup p {
    color: #666;
  }
  
  .signup a {
    color: #007bff;
    text-decoration: none;
  }
  
  .error-message {
    margin-top: 20px;
    color: red;
    text-align: center;
  }
  </style>
  