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
            items: ['Milk 0 ml', 'Caffeine 63 mg', 'Sugar 0 ml'],
            calories: 5,
            presets:{
              sweetness: 50, // No sweetness
              shots: 1, // Single shot
              milk: 0, // No milk
              water: 1 // No additional water
            }
          },
          {
            id: 'Cappuccino',
            img: 'cappucino.jpg',
            title: 'Cappuccino',
            text: " A Cappuccino is a coffee drink made with equal parts of espresso, steamed milk, and milk foam which will resuls in a rich, creamy beverage flavor. \n \n",
            items: ['Espresso: 30 ml', 'Milk: 60 ml (steamed milk)', 'Sugar: 0-15 g '],
            calories: 100,
            presets:{
              sweetness: 100,
              shots: 1, 
              milk: 2,
              water: 1
            }
          },
          {
            id: 'Latte',
            img: 'latte.jpg',
            title: 'Latte',
            text: "A latte is a coffee drink made with espresso and steamed milk, topped with a small amount of milk foam, offering a smooth and creamy flavor.",
            items: ['Espresso: 30 ml ', 'Milk: 210 ml (steamed milk)', 'Sugar: 0-15 g'],
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
            img: 'americano.jpeg',
            title: 'Americano',
            text: "An Americano is a coffee drink made by diluting espresso with hot water, resulting in a milder flavor similar to brewed coffee.",
            items: ['Espresso: 30 ml', 'Milk: 0 ml', 'Sugar: 0 g'],
            calories: 5,
            presets:{
              sweetness: 100, 
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
            items: ['Caffeine: Approximately 95 mg', 'Milk: 0 ml ', 'Sugar: 0 g'],
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

  .heading{
    text-align: center;
    margin-top: 5%;
    padding-top: 2%;
    padding-bottom: 2%;
    font: 'Darker Grotesque';
    border-style: solid;
    border-color: rgb(37, 22, 6);
    border-radius: 25px;

  }
  .container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 5%;
    background: rgba(220, 216, 210, 0.5);
    border-radius:120px;
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
    border-radius: 50px;
  }
  
  .order-button {
    display: inline-block;
    text-align: center;
    border: none;
    background: #a08b7c;
    box-shadow: inset -4px -4px 10px 2px rgba(0, 0, 0, 0.25);
    border-radius: 25px;
    font-size: 16px !important;
    font-weight: 600 !important;
    width: 60%;
    color: #f7f7f7;
    padding: 5px 10px;
  }
    
  .card-text{
    line-height: 80%;
    height: 100px;
  }
  
  .order-button:hover {
    background: #B9a495;
    box-shadow: inset 2px 2px 10px 2px rgba(0, 0, 0, 0.25);
  }
  </style>
  
