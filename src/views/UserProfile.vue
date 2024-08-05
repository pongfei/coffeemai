<template>
    <div class="user-profile">
      <h2>User Profile</h2>
      <div class="profile-info">
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Password:</strong> {{ user.password }}</p>
      </div>
      <h3>Order History</h3>
      <div v-if="orders.length">
        <div v-for="order in orders" :key="order.id" class="order">
          <p><strong>Order ID:</strong> {{ order.id }}</p>
          <p><strong>Items:</strong> {{ order.items }}</p>
          <p><strong>Date:</strong> {{ order.createdAt }}</p>
        </div>
      </div>
      <div v-else>
        <p>No orders found.</p>
      </div>
    </div>
  </template>
  
  <script>
  import { getAuth } from 'firebase/auth';
  import { getFirestore, doc, getDoc, collection, getDocs } from 'firebase/firestore';
  
  export default {
    name: 'UserProfile',
    data() {
      return {
        user: {
          email: '',
          password:''
        },
        orders: []
      };
    },
    async created() {
      await this.fetchUserProfile();
      await this.fetchUserOrders();
      await this.fetchUserPassword();
    },
    methods: {
      async fetchUserProfile() {
        const auth = getAuth();
        const db = getFirestore();
        const user = auth.currentUser;
  
        if (user) {
          const userDocRef = doc(db, 'users', user.uid);
          const userDoc = await getDoc(userDocRef);
  
          if (userDoc.exists()) {
            this.user = userDoc.data();
          } else {
            console.log('No user data found in Firestore.');
          }
        } else {
          console.log('No user is logged in');
        }
      },
      async fetchUserOrders() {
        const auth = getAuth();
        const db = getFirestore();
        const user = auth.currentUser;
  
        if (user) {
          const ordersCollectionRef = collection(db, 'orderHistory', user.uid, 'orders');
          const querySnapshot = await getDocs(ordersCollectionRef);
  
          const orders = [];
          querySnapshot.forEach((doc) => {
            orders.push({ id: doc.id, ...doc.data() });
          });
  
          this.orders = orders;
        } else {
          console.log('No user is logged in');
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .user-profile {
    padding: 20px;
  }
  
  .profile-info {
    margin-bottom: 20px;
  }
  
  .order {
    border: 1px solid #ddd;
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 4px;
  }
  
  .order p {
    margin: 5px 0;
  }
  </style>