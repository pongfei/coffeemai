<template>
  <div class="heading"><h1> User Profile </h1></div>
  <div class="user-profile container row mt-4">
    <div class="profile-info">
      <h3><strong>Email:</strong> {{ user.email }}</h3>
      <!--<p><strong>Password:</strong> {{ user.password }}</p>-->
    </div>
    <hr>
    <h3>Information</h3>
    <div class="order">
      <p><strong>Health Condition:</strong> {{user.healthCondition}}</p>
      <p><strong>Age:</strong> {{user.ageGroup}}</p>
      <p><strong>Preferences:</strong> {{user.preferences}}</p>
    </div>
    
    <hr>
    <h3>Order History</h3>
    <div v-if="orders.length">
      <div v-for="order in orders" :key="order.id" class="order">
        <!-- <p><strong>Order ID:</strong> {{ order.id }}</p> -->
        <p><strong>Menu:</strong> {{ order.menu }}</p>
        <p><strong>milk:</strong> {{ order.milk }}</p>
        <p><strong>shot:</strong> {{ order.shot }}</p>
        <p><strong>sweetness:</strong> {{ order.sweetness }}</p> 
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
import { getFirestore, doc, getDoc, collection, getDocs, query, where } from 'firebase/firestore';

export default {
  name: 'UserProfile',
  data() {
    return {
      user: {
        email: null,
        password: '',
      },
      orders: [],
    };
  },
  async created() {
    await this.getUser();
    await this.getOrder();
  },
  methods: {
    
    async getUser() {
      const auth = getAuth(); // Initialize Firebase Auth
      const db = getFirestore();
      const user = auth.currentUser; // Get authenticated user

      if (user) {
        const userDocRef = doc(db, 'users', user.uid); //ref to firestore document
        const userDoc = await getDoc(userDocRef); //fetch from firestore via userDocRef

        if (userDoc.exists()) {
          this.user = userDoc.data();
        } else {
          console.log('No user data found in Firestore.');
        }
      } else {
        console.log('No user is logged in');
      }
    },

    
    async getOrder() {
      const auth = getAuth();
      const db = getFirestore();
      const user = auth.currentUser;

      if (user) {
        const userEmail = user.email;

        try {
          //query by mail
          const q = query(collection(db, 'orders'), where('email', '==', userEmail));

          //execute query
          const querySnapshot = await getDocs(q);

          //show 
          this.orders = querySnapshot.docs.map((doc) => ({
            // id: doc.id,
            menu: doc.data().menu, //menu is from firestore
            milk: doc.data().milk,
            shot: doc.data().shots,
            sweetness: doc.data().sweetness,
            createdAt: doc.data().timestamp.toDate().toLocaleString(), // Convert Firestore timestamp to readable date

            // ...doc.data(),

          }));

          console.log('Orders for current user:', this.orders);
        } catch (error) {
          console.error('Error fetching orders:', error);
        }
      } else {
        console.log('No user is logged in.');
      }
    },
  },
};
</script>

<style scoped>

</style>
