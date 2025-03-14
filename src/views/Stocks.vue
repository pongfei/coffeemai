<template>
  <div class="container mt-5 row" style="width: 800px; padding-top: 0px; ">
    <h1 class="heading">Ingredient Status</h1>
      <div>
        <div v-for="(stock, product) in stocks" :key="product">
          <h2>{{ product }}</h2>
          <span>Stock: {{ stock }}</span><br>
          <button @click="updateStock(product, 0)" class="button" style="width: 40%">Empty</button>
          <button @click="updateStock(product, product === 'water' ? 3 : 40)" class="button" style="width: 40%">Max</button>
        </div>
      </div>
    </div>
    <hr>
  </template>
  
  <script>
  import { ref, onMounted } from "vue";
  import { doc, updateDoc, getDoc, setDoc } from "firebase/firestore"; // Import Firestore config
  import { db } from '../main';

  export default {
    setup() {
      const stocks = ref({
        coffee: 0,
        sugar: 0,
        cream: 0,
        water: 0
      });
      const fetchStocks = async () => {
        for (const product of Object.keys(stocks.value)) {
        const docRef = doc(db, "stocks", product);
        const docSnap = await getDoc(docRef);

        if (docSnap.exists()) {
          stocks.value[product] = docSnap.data().stock;
        } else {
          await setDoc(docRef, { stock: 0 }); 
        }
        }
      };
      const updateStock = async (product, newStock) => {
        const docRef = doc(db, "stocks", product);

        try {
        await updateDoc(docRef, { stock: newStock });
        stocks.value[product] = newStock;
        } catch (error) {
        console.error("Error updating stock:", error);
        }
      };
      onMounted(fetchStocks);
      return { stocks, updateStock };
    }
  };
  </script>
  
  <style>
  
  </style>
  