<template>
  <div id="app">
    <nav>
      <div class="left">
        <button class="nav-button" @click="menu">Menu</button>
        <button class="nav-button" @click="myMenu">My Menu</button>
        <button class="nav-button" @click="recommend">Recommend</button>
        <button class="nav-button" @click="stock">Stocks</button>

      </div>
      <div class="center">
        <img src="/logo.png" alt="Coffee Mai logo" />
      </div>
      <div class="right">
        <!-- Timer -->

        <!-- <div class="timer" v-if="timerLogin">
          <p>Time Left: {{ timeLeft }} seconds</p>
        </div> -->

        <div v-if="isUserLoggedIn" class="profile-container" @click.stop="toggleProfileDropdown">
          <!-- <img src="https://via.placeholder.com/35" alt="Profile" class="profile-image" /> -->
          <img src="/profile.jpg" alt="Profile" class="profile-image" />
           <!-- <img src="profile.jpg" alt="Profile" class="profile-image"> -->

          <div v-if="showProfileDropdown" class="profile-dropdown">
            <p @click="viewProfile">Profile</p>
            <button class="logout-button" @click="logOut">Log Out</button>
          </div>
        </div>
        <button v-else class="nav-button join-now" @click="logIn">Log In</button>
      </div>
    </nav>
    <div class="content mt-4">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { getAuth, onAuthStateChanged, signOut } from 'firebase/auth';
import { useRouter } from 'vue-router';
import { getFirestore, doc, setDoc, onSnapshot } from 'firebase/firestore';
import Stocks from './views/Stocks.vue';


const isUserLoggedIn = ref(false);
const showProfileDropdown = ref(false);
const router = useRouter();

const timerLogin = ref(true);
const timeLeft = ref(120); // Set the timer to 10 seconds for testing
const timer = ref(null);

onMounted(() => {
  const auth = getAuth();
  onAuthStateChanged(auth, (user) => {
    if (user) {
      isUserLoggedIn.value = true;
      startTimer();
    } else {
      isUserLoggedIn.value = false
      stopTimer();
    }
  });


  // Reset time
  
  window.addEventListener('mousemove', resetIdleTimer);
  window.addEventListener('keydown', resetIdleTimer);
  window.addEventListener('click', resetIdleTimer);
  
  
});


// Clean up event listeners when the component is destroyed just before

onUnmounted(() => {
  window.removeEventListener('mousemove', resetIdleTimer);
  window.removeEventListener('keydown', resetIdleTimer);
  window.removeEventListener('click', resetIdleTimer);
  stopTimer();
});


// Timer logic

function startTimer() {
  stopTimer(); // Clear any existing timer
  timer.value = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--;
    } else {
      clearInterval(timer.value); // Stop the timer
      logOut(); // Automatically log out when time runs out
    }
  }, 1000); // Run every second
}


function stopTimer() {
  if (timer.value) {
    clearInterval(timer.value); // Stop the timer
    timer.value = null;
  }
  timeLeft.value = 600; // Reset the timer (can adjust the value)
}


function resetIdleTimer() {
  stopTimer(); // Reset the timer
  startTimer(); // Start a new timer
}

// Profile dropdown and logout functions

function toggleProfileDropdown() {
  showProfileDropdown.value = !showProfileDropdown.value;
}

function viewProfile() {
  showProfileDropdown.value = false;
  router.push({ name: 'UserProfile' });
}

function logOut() {
  const auth = getAuth();
  const db = getFirestore();
  const globalSessionRef = doc(db, 'globalSession', 'currentSession');

  signOut(auth)
    .then(() => {
      isUserLoggedIn.value = false;
      showProfileDropdown.value = false;
      router.push('/login');
      setDoc(globalSessionRef, { isLoggedIn: false }, { merge: true });
    })
    .catch((error) => {
      console.error('Sign out error', error);
    });
}

// Navigation functions
function logIn() {
  router.push('/login');
}

function menu() {
  router.push('/menu');
}

function myMenu(){
  router.push('/mymenu')
}

function recommend(){
  router.push('/Recommend')
}

function stock(){
  router.push('/Stocks')
}

// Monitor global session (if needed for your use case)
function monitorGlobalSession() {
  const db = getFirestore();
  const globalSessionRef = doc(db, 'globalSession', 'currentSession');

  // Listen for changes to the global session
  onSnapshot(globalSessionRef, (doc) => {
    if (doc.exists()) {
      globalSessionActive.value = doc.data().isLoggedIn;
    }
  });
}
</script>

<style>
/* Your existing styles */
body {
  background-image: url("bg.jpg");
  background-repeat: repeat-y;
  background-size: contain;
  margin: 0;
  font-family: 'Darker Grotesque';
  font-size: 18px;
}

#app {
  display: flex;
  flex-direction: column;
  grid-template-rows: 10% 80% 10%;
}

nav {

  line-height: 75%;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1;
  width: 100%;
  height: 65px;
  font-size: 18px;
  text-align: center;
  display: grid;
  grid-template-columns: 30% 40% 30%;
  background-color: #f7f7f7;
  color: #f7f7f7;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.center{
  align-items: center;
  justify-self: center;
}
.left{
  display: flex;
  flex-direction: row;
}
.right{
  display: flex;
  grid-column-end: 4;
  flex-direction: row-reverse;
  align-items: center;
}
.wrap{
  flex-wrap: wrap;
}
.timer{
  font-size: large;
  padding-right: 150px;
  padding-top: 20px;
}

.center img {
  height: 65px;
  padding: 5px;
}
.left img {
  height: 35px;
  padding: 5px;
}



.nav-button {
  font-family: 'Darker Grotesque';
  background-color: #f7f7f7;
  border: 2px solid #301b00;
  color: #301b00;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  padding: 10px;
  margin-left: 5px;
  border-radius: 25px;
  transition: background-color 0.3s, color 0.3s, transform 0.3s;
}

.nav-button:hover {
  background-color: #ebe4df;
  color: #301b00;
  transform: scale(1.05);
  border: 2px solid #301b00;
}

.join-now:hover {
  background-color: #301b00;
  color: #f7f7f7;
  border: 2px solid #301b00;
}

.profile-container {
  position: relative;
  cursor: pointer;
}

.profile-image {
  width: 35px;
  height: 35px;
  border-radius: 50%;
}

.profile-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: white;
  color: black;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  width: 150px;
  z-index: 10;
  text-align: center;
}

.profile-dropdown p {
  margin: 0;
  padding: 10px;
  cursor: pointer;
}

.profile-dropdown p:hover {
  background-color: #f0f0f0;
}

.logout-button {
  background-color: #ee7a7a;
  border: none;
  color: white;
  padding: 10px;
  cursor: pointer;
  border-radius: 5px;
  font-size: 18px;
  width: 100%;
  margin: 0;
}

.logout-button:hover {
  background-color: #ee7a7a;
}

.content {
  justify-content: center;
  align-items: center;
  flex: 1;
  padding-top: 20px; /* To account for the fixed navbar height */
}






.customize-page {
  padding: 20px;
  margin: 50px auto;
  width: 100%;
  max-width: 500px;
  border-radius: 120px;
  text-align: center;
  background-color: rgba(220, 216, 210, 0.5);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  justify-content: center;
}

.menu-item-image {
  width: 300px;
  height: auto;
  max-height: 300px;
  object-fit: cover;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin: 20px 0;
}



input[type="range"] {
  width: 100%;
  height: 20px;
  border-radius: 50px;
  outline: none;
  opacity: 0.8;
  transition: opacity .2s;
  color: #333;
}

input[type="range"]:hover {
  opacity: 1;
}

.slider-container {
  width: 100%; /* Width of the outside container */
}
.slider {
  appearance: none;
  width: 100%;
  height: 20px;
  border-radius: 5px;  
  background: #d3d3d3;
  outline: none;
  opacity: 0.7;
  -webkit-transition: .2s;
  transition: opacity .2s;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 27px;
  height: 20px;
  border-radius: 50%; 
  background: #a08b7c;
  cursor: pointer;
}

.slider::-moz-range-thumb {
  width: 27px;
  height: 20px;
  border-radius: 50%;
  background: #a08b7c;
  cursor: pointer;
}
input[type="range"]::-webkit-slider-thumb {
  box-shadow: -410px 0 0 400px #B9a495;
  background-image: url("/top.png");
  background-size: cover;
}
input[type="range"]::-webkit-slider-thumb:hover {
  transform: scale(1.2);
}

input[type="range"]::-moz-range-thumb {
  box-shadow: -410px 0 0 400px #B9a495;
  background-image: url("/top.png");
  background-size: cover;
}

input[type="range"]::-moz-range-thumb:hover {
  transform: scale(1.2);
}
input[type="range"] {
  /*  ...  */
  /*  slider progress trick  */
  overflow: hidden;
  border-radius: 16px;
}

.menu-item-image {
  width: 100%; /* Ensures the image takes up the full width of its container */
  height: auto; /* Maintains the aspect ratio */
  max-height: 300px; /* Limits the maximum height to prevent it from stretching */
  object-fit: cover; /* Ensures the image fills the container while cropping any overflow */
  border-radius: 15px; /* Keeps rounded corners */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Adds a subtle shadow */
  margin: 20px 0;
}

button {
  background-color: #763f00;
  border: none;
  color: white;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s, transform 0.3s;
}

button:hover {
  background-color: #45a049;
  transform: scale(1.05);
}

h1{
  font-family: 'Numans';
  font-size: 40px;
}


/* menu */
.heading{
  text-align:center;
  margin-top: 5%;
  padding-top: 5%;
  padding-bottom: 2%;
  border-width: 2px;
  background-color:rgba(255, 255, 255, 0.75);
  border: #333;
  border-radius: 40px;
  font-family: "Numans";
  font-size: 2.5rem;
  width: 75%;
  justify-content: center;
  justify-self: center;
  
}
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 5%;
  background: url("/cardbg.png");
  border-radius:120px;
}

.order {
  text-align: center;
}

.fixed-size {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.card-equal-height {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 620px;
  border-radius: 40px;
}

.order-button {
  display: inline-block;
  text-align: center;
  border: none;
  background: #a08b7c;
  box-shadow: inset -4px -4px 10px 2px rgba(0, 0, 0, 0.25);
  border-radius: 25px;
  font-size: 20px !important;
  font-weight: 600 !important;
  width: 60%;
  color: #f7f7f7;
  padding: 5px 10px;
  text-decoration: none;
  justify-self: center;

}

.button{
  display: inline-block;
  text-align: center;
  border: none;
  background: rgb(196, 177, 158);
  box-shadow: inset -4px -4px 10px 2px rgba(0, 0, 0, 0.25);
  border-radius: 25px;
  font-size: 20px !important;
  font-weight: 600 !important;
  width: 60%;
  color: #342113;
  padding: 5px 10px;
  text-decoration: none;
  justify-self: center;   
}

.card-img-top {
  height: 200px;
  padding: 10px;
  border-radius: 40px;
}

h5{
  font-family: 'Numans';
}
.card-text{
  line-height: 100%;
  height: 100px;
}

.order-button:hover {
  background: #B9a495;
  box-shadow: inset 2px 2px 10px 2px rgba(0, 0, 0, 0.25);
}
.button:hover{
  background: #B9a495;
  box-shadow: inset 2px 2px 10px 2px rgba(0, 0, 0, 0.25);
}

.login-container {
  display: flex;
  height: 100vh;
  border-radius: 0px;
  font-family: 'Darker Grotesque';
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
  font-family: 'Darker Grotesque';
  background-color: #b39e8f;
  color: white;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  padding: 10px 20px;
  margin-left: 10px;
  border-radius: 25px;
  transition: background-color 0.3s, color 0.3s, transform 0.3s;
}

.login-button:hover {
  background: #ebe4df;
  color: #333;
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
  width: 100%;
  margin-top: 20px;
  text-align: center;
}

.signup p {
  color: #666;
}

.signup a {
  color: #333;
  font-weight: bold;
  text-decoration: none;
}

.error-message {
  margin-top: 20px;
  color: red;
  text-align: center;
}




/* my menu*/

/* Page container */
.menu-page {
  text-align: center;
  width: 100%;
  max-width: 500px;
  font-size: 18px;
}

/* Grid for menu cards */
.menu-grid {
  display: grid;
  flex-wrap: wrap; /* Allows wrapping to the next row if space runs out */
  gap: 20px; /* Adds spacing between the cards */
  row-gap: 40px;
}


/* Form styling */
.menu-form {
  margin: 20px auto;
  width: 75%;
  display: grid;
  gap: 10px;
}

.form-input {
  padding: 10px;
  font-size: 18px;
  border: 1px solid #ddd;
  border-radius: 20px;
}



/* Card styling */
.card {
  border: 2px solid #ddd;
  border-radius: 40px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.card:hover {
  transform: scale(1.05);
}

.card-img{
  border-radius: 40px;
}


.card-body {
  padding-inline: 20px;
  text-align: left;
}

.mycard-body {
  padding-inline: 20px;
  text-align: left;
  height: 100%;
}

.list-group{
  text-align: left;
}

/*signup*/
.signup-container {
  display: flex;
  height: fit-content;
  border-radius: 25px;
  font-family: 'Darker Grotesque';
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
  font-family: 'Darker Grotesque';
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

.checkbox-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 15px;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #666;
  cursor: pointer;
}

.checkbox-group input[type="checkbox"] {
  margin-right: 10px;
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

.error-message {
  margin-top: 20px;
  color: red;
  text-align: center;
}



/*user profile*/
.user-profile {
  padding: 20px;
  width: 100%;
  max-width: 600px;
  font-size: 18px;
}

.profile-info p{
  margin-bottom: 20px;
  font-size: 18px;
}


.order{
  padding-left: 20px;
  padding-bottom: 20px;
}

.order p {
  margin: 5px 0;

  font-size: 18px;
  text-align: left;
}



/* waiting*/
/* Customize hr styling */
hr {
  height: 10px;
  border: none;  /* Remove the default border */
  border-top: 5px solid black;
}

#container {
  margin-left: 90px;
  width: 500px;
  height: 500px;
}

/* Keyframe animation for spinner */
@keyframes animation {
  0% {
    stroke-dasharray: 1 98;
    stroke-dashoffset: -105;
  }
  50% {
    stroke-dasharray: 80 10;
    stroke-dashoffset: -160;
  }
  100% {
    stroke-dasharray: 1 98;
    stroke-dashoffset: -300;
  }
}

#spinner {
  transform-origin: center;
  animation-name: animation;
  animation-duration: 2s;
  animation-timing-function: cubic-bezier;
  animation-iteration-count: infinite;
}

.waiting-page {
  text-align: center;
  margin-top: 50px;
}
</style>