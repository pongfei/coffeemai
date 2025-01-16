<template>
  <div id="app">
    <nav>
      <div class="left">
        <img src="https://t4.ftcdn.net/jpg/05/14/51/79/360_F_514517927_dXLi1DauUmrCaE3AkElsVgJ1jaYZMcSA.jpg" alt="Expresso logo" />
        <button class="nav-button" @click="menu">Menu</button>
        <button class="nav-button" @click="myMenu">My Menu</button>
      </div>
      <div class="right">
        <!-- Timer -->
        <div class="timer" v-if="timerLogin">
          <p>Time Left: {{ timeLeft }} seconds</p>
        </div>

        <div v-if="isUserLoggedIn" class="profile-container" @click.stop="toggleProfileDropdown">
          <!-- <img src="https://via.placeholder.com/35" alt="Profile" class="profile-image" /> -->
          <img src="/profile.jpg" alt="Profile" class="profile-image" />
           <!-- <img src="profile.jpg" alt="Profile" class="profile-image"> -->

          <div v-if="showProfileDropdown" class="profile-dropdown">
            <p @click="viewProfile">Profile</p>
            <button class="logout-button" @click="logOut">Logout</button>
          </div>
        </div>
        <button v-else class="nav-button join-now" @click="logIn">Login</button>
      </div>
    </nav>
    <div class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { getAuth, onAuthStateChanged, signOut } from 'firebase/auth';
import { useRouter } from 'vue-router';
import { getFirestore, doc, setDoc, onSnapshot } from 'firebase/firestore';


const isUserLoggedIn = ref(false);
const showProfileDropdown = ref(false);
const router = useRouter();

const timerLogin = ref(true);
const timeLeft = ref(30); // Set the timer to 10 seconds for testing
const timer = ref(null);

onMounted(() => {
  const auth = getAuth();
  onAuthStateChanged(auth, (user) => {
    if (user) {
      isUserLoggedIn.value = true;
      startTimer();
    } else {
      isUserLoggedIn.value = false;
      stopTimer();
    }
  });


  // Reset time
  /*
  window.addEventListener('mousemove', resetIdleTimer);
  window.addEventListener('keydown', resetIdleTimer);
  window.addEventListener('click', resetIdleTimer);
  */
  
});


// Clean up event listeners when the component is destroyed just before
/*
onUnmounted(() => {
  window.removeEventListener('mousemove', resetIdleTimer);
  window.removeEventListener('keydown', resetIdleTimer);
  window.removeEventListener('click', resetIdleTimer);
  stopTimer();
});
*/

// Timer logic
/*
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
}*/

/*
function stopTimer() {
  if (timer.value) {
    clearInterval(timer.value); // Stop the timer
    timer.value = null;
  }
  timeLeft.value = 30; // Reset the timer (can adjust the value)
}*/

/*
function resetIdleTimer() {
  stopTimer(); // Reset the timer
  startTimer(); // Start a new timer
}*/

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
  background-color: white;
  margin: 0;
  font-family: Arial, sans-serif;
}

#app {
  background-color: white;
  display: flex;
  flex-direction: column;
}

nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1;
  width: 100%;
  height: 65px;
  font-size: 12px;
  text-align: center;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #624410;
  color: white;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.left,
.right {
  display: flex;
  align-items: center;
}

.timer{
  font-size: large;
  padding-right: 150px;
  padding-top: 20px;
}

.left img {
  height: 35px;
  padding: 5px;
}

.nav-button {
  background-color: transparent;
  border: 2px solid #d99800;
  color: white;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  padding: 10px 20px;
  margin-left: 10px;
  border-radius: 25px;
  transition: background-color 0.3s, color 0.3s, transform 0.3s;
}

.nav-button:hover {
  background-color: #d99800;
  color: white;
  transform: scale(1.05);
}

.join-now:hover {
  background-color: #a77500;
  padding: 10px;
  border-radius: 50px;
  text-decoration: underline;
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
  background-color: #ff4d4d;
  border: none;
  color: white;
  padding: 10px;
  cursor: pointer;
  border-radius: 5px;
  font-size: 14px;
  width: 100%;
}

.logout-button:hover {
  background-color: #e60000;
}

.content {
  justify-content: center;
  align-items: center;
  flex: 1;
  padding-top: 65px; /* To account for the fixed navbar height */
}
</style>