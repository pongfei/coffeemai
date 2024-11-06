import './assets/main.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'  //main.js read all the links in the router
//but if we don't wanna route it with the router, we can use  <router-view></router-view>

// Import the functions you need from the SDKs you need
import { initializeApp } from 'firebase/app';
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { getFirestore, doc, setDoc, getDoc, serverTimestamp } from 'firebase/firestore'; // Import Firestore

const firebaseConfig = {
    apiKey: "AIzaSyD6z84iJBYA_KG-YSN6lAVR-MwP5sZwn2Y",
    authDomain: "coffeemai-2bf6d.firebaseapp.com",
    projectId: "coffeemai-2bf6d",
    storageBucket: "coffeemai-2bf6d.appspot.com",
    messagingSenderId: "349970863172",
    appId: "1:349970863172:web:dc86ab51fe5d0e444c5811"
  };

  //init CORS


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

// const manageUserSession = async (user) => {
//   if (!user) return;

//   const sessionId = `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
//   const userSessionRef = doc(db, 'activeSessions', user.uid);
//   const userSessionDoc = await getDoc(userSessionRef);

//   if (userSessionDoc.exists() && userSessionDoc.data().sessionId !== sessionId) {
//     // A different session exists, sign out the current user
//     await signOut(auth);
//     alert('You have been signed out because your account is being used in another session.');
//   } else {
//     // Update Firestore with the new session
//     await setDoc(userSessionRef, { 
//       sessionId,
//       timestamp: serverTimestamp() 
//     });
//   }
// };

export { db, auth }; // Export Firestore instance for use in components
  