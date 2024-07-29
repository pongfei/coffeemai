<template>
    <div class="login-container">
      <div class="image-side">
        <img src="https://img.freepik.com/free-photo/delicious-coffee-beans-cup_23-2150691429.jpg" alt="Coffee" class="background-image" />
        <p class="quote">"Espress Yourself."</p>
      </div>
      <div class="form-side">
        <h2> Welcome Back</h2>
        <br>
        <p>Enter your account credentials to view your orders</p>
        <form @submit.prevent="login"> <!-- this calls login method--> 
          <div class="input-group">
            <label for="email">Email</label>
            <input type="email" id="email" v-model="formData.email" required />
          </div>
          <div class="input-group">
            <label for="password">Password</label>
            <input type="password" id="password" v-model="formData.password" required />
          </div>
          <div class="forgot-password">
            <a href="#">Forgot your password?</a>
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
  import { getAuth, signInWithEmailAndPassword } from 'firebase/auth';
  
  export default {
    name: 'LogIn',
    data() {
      return {
        formData: {
          email: '',
          password: ''
        },
        errorMessage: '',
        successMessage: '',
        xhrRequest: false
      };
    },
    methods: {
      login() {
        this.errorMessage = '';
        if (!this.isValidEmail(this.formData.email)) {
          this.errorMessage = 'Please enter a valid email address.';
          return;
        }
        const auth = getAuth();
        this.xhrRequest = true;
        signInWithEmailAndPassword(auth, this.formData.email, this.formData.password)
          .then(user => {
            this.$router.replace('/mainPage');
            this.xhrRequest = false;
          })
          .catch(error => {
            this.errorMessage = error.message;
            this.xhrRequest = false;
          });
      },
      isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
      },
      // loginGoogle() {
      //   // Implement Google sign-in logic here
      // }
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
  