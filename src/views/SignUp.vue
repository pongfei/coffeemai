<template>
    <div class="signup-container">
      <div class="image-side">
        <img src="https://img.freepik.com/free-photo/delicious-coffee-beans-cup_23-2150691429.jpg" alt="Coffee" class="background-image" />
        <p class="quote">"Espress Yourself."</p>
      </div>
      <div class="form-side">
        <h2>Create Account</h2>
        <br>
        <p>Sign up to start ordering your favorite coffee</p>
        <div class="input-group">
          <input type="email" class="form-control" placeholder="Email" v-model="formData.email" />
        </div>
        <div class="input-group">
          <input type="password" class="form-control" placeholder="Password" v-model="formData.password" />
        </div>
        <button class="btn btn-success" @click="signUp">Sign Up</button>
        <div class="login">
          <p>Already have an account? <router-link to="/login">Log In</router-link></p>
        </div>
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { getAuth, createUserWithEmailAndPassword } from 'firebase/auth';
  import { getFirestore, doc, setDoc } from 'firebase/firestore';
  
  export default {
    name: 'SignUp',
    data() {
      return {
        formData: {
          email: '',
          password: ''
        },
        errorMessage: ''
      };
    },
    methods: {
      async signUp() {
        const auth = getAuth();
        const db = getFirestore();
        try {
          const userCredential = await createUserWithEmailAndPassword(auth, this.formData.email, this.formData.password);
          const user = userCredential.user;
          const userDocRef = doc(db, 'users', user.uid);
          await setDoc(userDocRef, {  
            email: this.formData.email,
            password: this.formData.password
          });
          console.log('Successfully signed up');
          this.$router.replace('/mainpage');
        } catch (error) {
          this.errorMessage = error.code + '\n' + error.message;
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .signup-container {
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
    margin-bottom: 20px;
    color: #666;
  }
  
  .input-group {
    width: 100%;
    margin-bottom: 20px;
  }
  
  .input-group input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
  }
  
  .btn {
    width: 100%;
    padding: 10px;
    background: #28a745;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background 0.3s;
  }
  
  .btn:hover {
    background: #218838;
  }
  
  .login {
    margin-top: 20px;
  }
  
  .login p {
    color: #666;
  }
  
  .login a {
    color: #007bff;
    text-decoration: none;
  }
  
  .error-message {
    margin-top: 20px;
    color: red;
    text-align: center;
  }
  </style>