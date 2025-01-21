<template>
    <div class="menu-page">
        <h1> My Menu </h1>

        <!-- new Menu Form -->
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
                />

                <label for="milk">Milk Level: {{ newMenu.milk }}</label>
                <input
                    type="range"
                    id="milk"
                    v-model="newMenu.milk"
                    min="0"
                    max="3"
                    step="1"
                />

                <label for="shots">Coffee Shots: {{ newMenu.shots }}</label>
                <input
                    type="range"
                    id="shots"
                    v-model="newMenu.shots"
                    min="1"
                    max="3"
                    step="1"
                />
            </div>

            <button @click="addMenu" class="btn btn-primary">Add Menu</button>
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
                    <p class="card-text">Milk: {{ menu.milk }}</p>
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

export default {
    name: "MyMenu",
    data() {
        return {
            newMenu: {
                title: "",
                sweetness: 3,
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
            };

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
                sweetness: 3,
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
        // userId: user.uid,
        email: user.email,
        menu: selectedMenu.title,
        sweetness: selectedMenu.sweetness,
        shots: selectedMenu.shots,
        milk: selectedMenu.milk,
        timestamp: new Date(), // Add a timestamp for the order
    };

    try {
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


<style scoped>
/* Grid for menu cards */
.menu-grid {
    display: flex;
    flex-wrap: wrap; /* Allows wrapping to the next row if space runs out */
    justify-content: flex-start; /* Aligns items to the start of the row */
    gap: 20px; /* Adds spacing between the cards */
    margin-top: 20px;
}

/* Page container */
.menu-page {
    text-align: center;
    margin-top: 20px;
}

/* Form styling */
.menu-form {
    margin: 20px auto;
    width: 100%;
    max-width: 400px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.form-input {
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

/* Grid for menu cards */
.menu-grid {
    display: flex;
    flex-wrap: wrap; /* Allows wrapping to the next row if space runs out */
    justify-content: flex-start; /* Aligns items to the start of the row */
    gap: 20px; /* Adds spacing between the cards */
    margin-top: 20px;
}

/* Card styling */
.card {
    border: 1px solid #ddd;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s;
}

.card:hover {
    transform: scale(1.05);
}

.card-img-top {
    border-radius: 10px 10px 0 0;
    height: 200px;
    object-fit: cover;
}

.card-body {
    padding: 20px;
}

.btn-primary {
    width: 100%;
    background-color: #624410;
    border-color: #624410;
    transition: background-color 0.3s, border-color 0.3s;
}

.btn-primary:hover {
    background-color: #c3a500;
    border-color: #c3a500;
}

</style>