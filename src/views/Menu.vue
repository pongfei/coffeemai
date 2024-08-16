<template>

  <div class= "heading"> <h1> Coffee Mai Menu </h1> 
  </div>
    <div class="container mt-5">
      <div class="row">
        <div class="col-md-4" v-for="(card, index) in menu" :key="index">
          <div class="card mb-4 card-equal-height">
            <img :src="card.img" class="card-img-top fixed-size" :alt="card.title">
            <div class="card-body">
              <h5 class="card-title">{{ card.title }}</h5>
              <p class="card-text">{{ card.text }}</p>
            </div>
            <ul class="list-group list-group-flush">
              <li class="list-group-item" v-for="(item, itemIndex) in card.items" :key="itemIndex">{{ item }}</li>
              <li class="list-group-item"><strong>Calories: {{ card.calories }} kcal</strong></li>
            </ul>
            <div class="card-body">
              <div class="order">
                <!-- <router-link :to ="{name: 'Customize', params: {id: card.id}}"> Order Now </router-link> -->
                <router-link :to="{ name: 'Customize', params: { id: card.id, img: card.img  }, query: { img: card.img ,sweetness: card.presets.sweetness, shots: card.presets.shots, milk: card.presets.milk, water: card.presets.water} }" class="order-button">Order Now</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>

  <script>
  import axios from 'axios';

  export default {
    name: 'Menu', 
    data() {
      return {
        // Description of each beverage is fetched from the description.json file
        menu: [
          {
            id: 'Espresso',
            img: 'espresso.jpg',
            title: 'Espresso',
            text: '',
            items: ['Milk 0 ml', 'Caffeine 63 mg', 'Sugar 0 ml'],
            calories: 5,
            presets:{
              sweetness: 0, // No sweetness
              shots: 1, // Single shot
              milk: 0, // No milk
              water: 0 // No additional water
            }
          },
          {
            id: 'Cappuccino',
            img: 'cappucino.jpg',
            title: 'Cappuccino',
            text: '',
            items: ['Espresso: 30 ml', 'Milk: 60 ml (steamed milk)', 'Sugar: 0-15 g '],
            calories: 80,
            presets:{
              sweetness: 2,
              shots: 1, 
              milk: 2,
              water: 0 
            }
          },
          {
            id: 'Latte',
            img: 'latte.jpg',
            title: 'Latte',
            text: '',
            items: ['Espresso: 30 ml ', 'Milk: 210 ml (steamed milk)', 'Sugar: 0-15 g'],
            calories: 160,
            presets:{
              sweetness: 2,
              shots: 1, 
              milk: 2,
              water: 0 
            }
          },
          {
            id: 'Americano',
            img: 'americano.jpeg',
            title: 'Americano',
            text: '',
            items: ['Espresso: 30 ml', 'Milk: 0 ml', 'Sugar: 0 g'],
            calories: 5,
            presets:{
              sweetness: 0, 
              shots: 1, 
              milk: 0, 
              water: 2 
            }
          },
          {
            id: 'Black',
            img: 'black.jpg',
            title: 'Black',
            text: '',
            items: ['Caffeine: Approximately 95 mg', 'Milk: 0 ml ', 'Sugar: 0 g'],
            calories: 5,
            presets:{
              sweetness: 0, 
              shots: 1,
              milk: 0,
              water: 0 
            }
          },
        ],
      };
    },
    methods: {
      // Function to retrieve descriptions from JSON file
      fetchDescriptions() {
        axios.get('description.json')
          .then(response => {
            const descriptions = response.data.coffeeList;
            this.menu.forEach(item => {
              if (descriptions[item.id]) {
                item.text = descriptions[item.id].desc;
              }
            });
          })
          .catch(error => {
            console.error('Error fetching descriptions:', error);
          });
      }
    },
    created() {
      this.fetchDescriptions();
    }
  };
  </script>
  
  <style>

  .heading{
    text-align: center;
    margin-top: 5%;
    padding-top: 2%;
    padding-bottom: 2%;
    font: Sans-serif;
    border-style: solid;
    border-color: rgb(182, 91, 1);
    border-radius: 25px;

  }
  .container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 1%;
  }
  
  .order {
    text-align: center;
  }
  
  .fixed-size {
    width: 100%;
    height: 200px;
    object-fit: cover;
  }
  
  .card-equal-height {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 600px;
  }
  
  .order-button {
    display: inline-block;
    text-align: center;
    border: none;
    border-radius: 2px;
    background-color: rgb(135, 83, 16);
    font-size: 12px !important;
    font-weight: 600 !important;
    width: 100%;
    color: rgb(255, 255, 255);
    padding: 10px 20px;
  }
  
  .order-button:hover {
    color: white;
    background-color: rgb(74, 46, 25);
  }
  </style>
  