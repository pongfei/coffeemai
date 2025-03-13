<template>

  <div class="heading"> <h1> Main Menu </h1> 
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
                 <!-- send it to customize page -->
                <router-link :to="{ name: 'Customize', params: { id: card.id, img: card.img  }, 
                query: { img: card.img ,sweetness: card.presets.sweetness, shots: card.presets.shots, milk: card.presets.milk, water: card.presets.water} }"
                class="order-button">Order Now</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="mt-4"/>

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
            text: "Espresso is a strong, concentrated coffee made by forcing hot water through finely-ground coffee beans, resulting in a rich flavor and creamy foam.",
            items: ['Cream 0 tsp', 'Coffee 2 tsp', 'Sugar 1 tsp'],
            calories: 5,
            presets:{
              sweetness: 50, 
              shots: 2, 
              milk: 0, 
              water: 1 
            }
          },
          {
            id: 'Cappuccino',
            img: 'cappucino.jpg',
            title: 'Cappuccino',
            text: " A Cappuccino is a coffee drink made with equal parts of espresso, steamed milk, and milk foam which will resuls in a rich, creamy beverage flavor. \n \n",
            items: ['Cream 1 tsp', 'Coffee 1 tsp', 'Sugar 2 tsp'],
            calories: 100,
            presets:{
              sweetness: 100,
              shots: 1, 
              milk: 1,
              water: 1
            }
          },
          {
            id: 'Latte',
            img: 'latte.jpg',
            title: 'Latte',
            text: "A latte is a coffee drink made with espresso and steamed milk, topped with a small amount of milk foam, offering a smooth and creamy flavor.",
            items: ['Cream 2 tsp', 'Coffee 1 tsp', 'Sugar 2 tsp'],
            calories: 160,
            presets:{
              sweetness: 100,
              shots: 1, 
              milk: 2,
              water: 1
            }
          },
          {
            id: 'Americano',
            img: 'americano.jpg',
            title: 'Americano',
            text: "An Americano is a coffee drink made by diluting espresso with hot water, resulting in a milder flavor similar to brewed coffee.",
            items: ['Cream 0 tsp', 'Coffee 1 tsp', 'Sugar 0 tsp'],
            calories: 5,
            presets:{
              sweetness: 0, 
              shots: 1, 
              milk: 0, 
              water: 1
            }
          },
          {
            id: 'Black',
            img: 'black.jpg',
            title: 'Black',
            text: "Black coffee is a simple, straightforward coffee made without any added milk, cream, or sugar.",
            items: ['Cream 0 tsp', 'Coffee 2 tsp', 'Sugar 0 tsp'],
            calories: 5,
            presets:{
              sweetness: 0, 
              shots: 2,
              milk: 0,
              water: 1
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


  </style>
  