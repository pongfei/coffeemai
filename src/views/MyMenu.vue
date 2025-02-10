<template>
    <div class="heading"><h1> My Menu </h1></div>
    <div class="menu-page col-md-4">

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
        <!-- display Menu Cards -->
        <div class="menu-grid">
            <div
                class="card"
                style="width: 20rem;"
                v-for="(menu, index) in menuItems"
                :key="index"
            >
            <img src="https://img.freepik.com/premium-vector/coffee-cup-cartoon-icon-illustration-food-drink-icon-concept-isolated-flat-cartoon-style_138676-2097.jpg?w=1060" class="card-img-top" alt="Coffee" />
                <div class="card-body">
                    <h5 class="card-title">{{ menu.title }}</h5>
                    <p class="card-text">Sweetness: {{ menu.sweetness }} %</p>
                    <p class="card-text">Cream: {{ menu.milk }}</p>
                    <p class="card-text">Shots: {{ menu.shots }}</p>
                    <button class="btn btn-primary" @click="placeOrder(menu.title)">
                        Order
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { collection, addDoc, getDocs, query, where } from "firebase/firestore";
import { db } from "../main";
import { getAuth, onAuthStateChanged } from "firebase/auth";
import { useRouter } from "vue-router";
import axios from "axios";

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
    },
    methods: {
        async addMenu() {
            if (!this.newMenu.title) {
                alert("Please enter a menu name!");
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
    const selectedMenu = this.menuItems.find((menu) => menu.title === menuTitle);
    if (!selectedMenu) {
        console.error("Menu not found for title:", menuTitle);
        return;
    }

    const auth = getAuth();
    const user = auth.currentUser;

    if (!user) {
        alert("Please log in to place an order.");
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

    try {
        // Send data to Raspberry Pi
        const response = await axios.post('http://192.168.58.32:5000/control', {
            milk: selectedMenu.milk,
            sweetness: selectedMenu.sweetness, // Fixed key name
            shots: selectedMenu.shots,
            water: 1
        });

        if (!response.data.success) {
            throw new Error(response.data.message);
        }

        // Save order in Firebase Firestore
        const docRef = await addDoc(collection(db, "orders"), order);
        console.log("Order successfully added with ID: ", docRef.id);
        alert(`Order placed for ${selectedMenu.title}!`);
    } catch (error) {
        console.error("Error adding order: ", error);
        alert("Failed to place the order. Please try again.");
    }
}
    },
};
</script>




