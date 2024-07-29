<template>
  <div id="app" @click="closeBasketDropdown">
    <nav>
      <div class="left">
        <img src="https://t4.ftcdn.net/jpg/05/14/51/79/360_F_514517927_dXLi1DauUmrCaE3AkElsVgJ1jaYZMcSA.jpg" alt="Expresso logo" />
        <!-- <button class="nav-button" @click="mainPage">Main Page</button> -->
        <button class="nav-button" @click="menu">Menu</button>
      </div>
      <div class="right">

        <div v-if="isUserLoggedIn" class="profile-container" @click.stop="toggleProfileDropdown">

        </div>
        <button v-else class="nav-button join-now" @click="logIn">Login</button>
      </div>
    </nav>
    
    <div class="content">
      <router-view :add-to-basket="addToBasket"></router-view>
    </div>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref, computed, onMounted } from 'vue'
import { getAuth, onAuthStateChanged, signOut } from 'firebase/auth'
import { useRouter } from 'vue-router'



onMounted(() => {
  const auth = getAuth()
  onAuthStateChanged(auth, user => {
    if (user) {
      isUserLoggedIn.value = true
    } else {
      isUserLoggedIn.value = false
    }
  })
})

function logOut() {
  const auth = getAuth()
  signOut(auth).then(() => {
    isUserLoggedIn.value = false
  }).catch(error => {
    console.error('Sign out error', error)
  })
}

</script>

<script>
export default {
  methods: {
    mainPage() {
      this.$router.push("/mainPage");
    },
    menu() {
      this.$router.push("/menu"); 
    },
    logIn() {
      this.$router.push("/login"); 
    }
  },
};
</script>

<style>
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

.order-details {
  display: flex;
  align-items: center;
}

.order-image {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 5px;
  margin-right: 10px;
}

.order-info {
  flex-grow: 1;
}

.basket-dropdown p {
  padding: 10px;
  text-align: center;
}

.total-price {
  padding: 10px;
  border-top: 1px solid #ddd;
  text-align: center;
  font-size: 16px;
  font-weight: bold;
}

.payment-button {
  background-color: #4CAF50;
  border: none;
  color: white;
  padding: 10px 20px;
  text-align: center;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  margin: 10px auto;
  border-radius: 10px;
  display: block;
  width: 80%;
}

.payment-button:hover {
  background-color: #45a049;
}

.remove-button {
  background-color: #ff4d4d;
  border: none;
  color: white;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 5px;
  font-size: 12px;
}

.remove-button:hover

 {
  background-color: #e60000;
}

.profile-container {
  position: relative;
}

.profile-image {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  cursor: pointer;
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
  padding-top: 50px; /* to account for the fixed navbar height */
}

</style>