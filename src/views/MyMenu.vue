<template>
    <hr>
    <div class="heading"><h1> My Menu </h1></div>
    <div class="menu-page center">

        <!-- new Menu Form -->
        <div class="container mt-5">
        <div class="menu-form">
            <input
                v-model="newMenu.title"
                type="text"
                placeholder="Enter Menu Name"
                class="form-input"
            />

            <!-- sweetness Slider -->
            <div class="slider-container">
                <label for="sweetness">Sweetness Level: {{ newMenu.sweetness }} %</label>
                <input
                    type="range"
                    id="sweetness"
                    v-model="newMenu.sweetness"
                    min="0"
                    max="150"
                    step="50"
                    class="slider"
                />

                <label for="milk">Cream Level: {{ newMenu.milk }}</label>
                <input
                    type="range"
                    id="milk"
                    v-model="newMenu.milk"
                    min="0"
                    max="2"
                    step="1"
                    class="slider"
                />

                <label for="shots">Coffee Shots: {{ newMenu.shots }}</label>
                <input
                    type="range"
                    id="shots"
                    v-model="newMenu.shots"
                    min="1"
                    max="3"
                    step="1"
                    class="slider"
                />
            </div>

            <button @click="addMenu" class="order-button">Add Menu</button>
        </div>
</div>
<div class="mt-4"/>
        <!-- display Menu Cards -->
        
    </div>
    <div class="menu-grid col-md-12">
            <div class="row">
            <div class="col-md-3" v-for="(menu, index) in menuItems" :key="index">
            <div class="card" style="margin-bottom: 20px;">
                <img src="/coffeecup.jpg" class="card-img-top" alt="Coffee" />
                <div class="mycard-body card-text">
                    <h5 class="card-title">{{ menu.title }}</h5>
                    <p >Sweetness: {{ menu.sweetness }} %</p>
                    <p >Cream: {{ menu.milk }}</p>
                    <p >Shots: {{ menu.shots }}</p>
                    <button class="order-button" style="width: 90%;" @click="placeOrder(menu.title)">Order</button>
                </div>
            </div>
            </div>
            </div>
        </div>
    <div class="mt-4"/>
</template>

<script>
import { collection, addDoc, getDocs, query, where,  doc, getDoc, writeBatch} from "firebase/firestore";
import { db } from "../main";
import { getAuth, onAuthStateChanged } from "firebase/auth";
import { useRouter } from "vue-router";
import axios from "axios";
import Swal from "sweetalert2";

export default {
    name: "MyMenu",
    data() {
        return {
            newMenu: {
                title: "",
                sweetness: 100,
                shots: 1,
                milk: 0,
            },
            menuItems: [],
            auth: getAuth(),
            isLoggedIn: false,
            userId: null, // Track the logged-in user's ID
            stocks: {
                coffee: 0,
                sugar: 0,
                cream: 0,
                water: 0
            }
        };
    },
    created() {
        const router = useRouter();
        onAuthStateChanged(this.auth, (user) => {
            if (user) {
                this.isLoggedIn = true;
                this.userId = user.uid;
                this.loadMenus(); // Load user-specific menus
            } else {
                this.isLoggedIn = false;
                router.push("/login");
            }
        });
        this.fetchStocks();
    },
    methods: {
        async fetchStocks() {
      let updatedStocks = { ...this.stocks }; // Clone to ensure reactivity

      for (const product of Object.keys(updatedStocks)) {
        const docRef = doc(db, "stocks", product);
        const docSnap = await getDoc(docRef);

        if (docSnap.exists()) {
          updatedStocks[product] = docSnap.data().stock; // Update cloned object
        } else {
          await setDoc(docRef, { stock: 0 });
          updatedStocks[product] = 0;
        }
      }
      this.stocks = updatedStocks; // Assign new object to trigger reactivity
      console.log("Updated stock data:", this.stocks);
  },
    async updateStocks(order) {
      const batch = writeBatch(db); // Create batch for multiple updates

      // Compute new stock values
      const newStockLevels = {
        coffee: Math.max(0, this.stocks.coffee - order.shots),
        sugar: Math.max(0, this.stocks.sugar - order.sweetness / 50),
        cream: Math.max(0, this.stocks.cream - order.milk),
        water: Math.max(0, this.stocks.water - 1) // Assuming 1 unit of water per cup
      };

      // Update Firestore stock documents
      for (const [product, newStock] of Object.entries(newStockLevels)) {
        const docRef = doc(db, "stocks", product);
        batch.update(docRef, { stock: newStock });
      }

      // Commit batch update
      await batch.commit();

      // Update local state
      this.stocks = { ...newStockLevels };
    },
    async addMenu() {
        if (!this.newMenu.title) {
            Swal.fire({
            title: "Missing Menu Name!",
            text: "Please enter a menu name!",
            icon: "warning",
            confirmButtonText: "OK",
          });
            return;
        }

        const menuWithUserId = {
            ...this.newMenu,
            userId: this.userId, // Attach the logged-in user's ID
        }

        try {
            const docRef = await addDoc(collection(db, "NewMenu"), menuWithUserId);
            console.log("Menu added with ID: ", docRef.id);

            this.menuItems.push(menuWithUserId); // Update local list
            this.resetForm();
        } catch (error) {
            console.error("Error adding menu: ", error);
        }
    },
    async loadMenus() {
        if (!this.userId) {
            console.error("User not logged in. Cannot load menus.");
            return;
        }

        try {
            const userMenusQuery = query(
                collection(db, "NewMenu"),
                where("userId", "==", this.userId)
            );
            const querySnapshot = await getDocs(userMenusQuery);
            const loadedMenus = querySnapshot.docs.map((doc) => doc.data());
            this.menuItems = loadedMenus;
        } catch (error) {
            console.error("Error loading menus: ", error);
        }
    },
    resetForm() {
        this.newMenu = {
            title: "",
            sweetness: 0,
            shots: 1,
            milk: 0,
        };
    },

    async placeOrder(menuTitle) {
        //checkcup
        const response = await axios.post('http://192.168.58.32:5000/checkcup')
        if (!response.data.success) {
            Swal.fire({
            title: "Missing Cup!",
            text: "Please place a cup!",
            icon: "warning",
            confirmButtonText: "OK",
          });
        throw new Error(response.data.message);
        }

        const selectedMenu = this.menuItems.find((menu) => menu.title === menuTitle);
        if (!selectedMenu) {
            console.error("Menu not found for title:", menuTitle);
            return;
        }

        const auth = getAuth();
        const user = auth.currentUser;

        if (!user) {
            Swal.fire({
                title: "Please log in!",
                icon: "warning",
                confirmButtonText: "OK",
            });
            return;
        }
        
        const order = {
            email: user.email,
            menu: selectedMenu.title,
            sweetness: selectedMenu.sweetness,
            shots: selectedMenu.shots,
            milk: selectedMenu.milk,
            timestamp: new Date(),
        };

        // Check if stock is sufficient before order
        await this.fetchStocks();

        if(this.stocks.coffee < order.shots){
          Swal.fire({
            title: "Warning!",
            text: "Not enough coffee stock!",
            icon: "warning",
            confirmButtonText: "OK",
          });
          return;
      }
      if (this.stocks.sugar < order.sweetness / 50) {
        Swal.fire({
            title: "Warning!",
            text: "Not enough coffee stock!",
            icon: "warning",
            confirmButtonText: "OK",
          });        
          return;
      }
      if (this.stocks.cream < order.milk) {
        Swal.fire({
            title: "Warning!",
            text: "Not enough cream stock!",
            icon: "warning",
            confirmButtonText: "OK",
          });        
          return;
      }
      if (this.stocks.water < 1) {
        Swal.fire({
            title: "Warning!",
            text: "Not enough water stock!",
            icon: "warning",
            confirmButtonText: "OK",
          });        
          return;
      } 

      try {
        await Swal.fire({
          title: "Do you wish to proceed?",
          icon: "warning",
          showCancelButton: true,
          confirmButtonText: "Yes, proceed",
          cancelButtonText: "Cancel",
        });

        if (result.isConfirmed) {
          console.log("User confirmed.");
          // Proceed with your action
        } else {
          console.log("User canceled.");
          return;
        }
            // Deduct ingredients from stock
            await this.updateStocks(order);
            
            this.$router.push({
              name: 'WaitingPage',
              params: { id: this.id },
              query: {
                sweetness: this.sweetness,
                shots: this.shots,
                milk: this.milk,
                water: this.water,
              },
            });

            // Send data to Raspberry Pi
            const response = await axios.post('http://192.168.58.32:5000/control', {
                milk: selectedMenu.milk,
                sugar: selectedMenu.sweetness, // Fixed key name
                shots: selectedMenu.shots,
            });

            if (!response.data.success) {
                throw new Error(response.data.message);
            }

            // Save order in Firebase Firestore
            const docRef = await addDoc(collection(db, "orders"), order);
            console.log("Order successfully");
            Swal.fire({
                title: "Order placed",
                icon: "warning",
                confirmButtonText: "OK",
            });
            this.$router.replace("/DonePage");
        } catch (error) {
            console.error("Error adding order: ", error);
            await Swal.fire({
                title: "Error",
                icon: "Failed to place the order. Please try again.",
                showCancelButton: true,
                confirmButtonText: "OK",
            });
        }
}
    },
};
</script>




