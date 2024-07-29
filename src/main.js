import './assets/main.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router' //main.js read all the links in the router
//but if we don't wanna route it with the router, we can use  <router-view></router-view>

// Import the functions you need from the SDKs you need
import { initializeApp } from 'firebase/app';
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore'; // Import Firestore

const firebaseConfig = {
    apiKey: "AIzaSyD6z84iJBYA_KG-YSN6lAVR-MwP5sZwn2Y",
    authDomain: "coffeemai-2bf6d.firebaseapp.com",
    projectId: "coffeemai-2bf6d",
    storageBucket: "coffeemai-2bf6d.appspot.com",
    messagingSenderId: "349970863172",
    appId: "1:349970863172:web:dc86ab51fe5d0e444c5811"
  };

// Initialize Firebase
const firebaseApp = initializeApp(firebaseConfig);
const db = getFirestore(firebaseApp); // Initialize Firestore
const auth = getAuth(firebaseApp);

let app;

onAuthStateChanged(auth, (user) => {
  if (!app) {
    app = createApp(App).use(router).mount('#app');
  }
});

// export { db }; // Export Firestore instance for use in components
  