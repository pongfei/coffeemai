
  <template>
    <div>
      <h1>Control Raspberry Pi</h1>
      <button @click="sendCommand('coffee')">coffee</button>
      <button @click="sendCommand('sugar')">sugar</button>
      <button @click="sendCommand('milk')">milk</button>
      <button @click="sendCommand('on')">Turn ON</button>
      <button @click="sendCommand('off')">Turn OFF</button>
      
  
      <!-- Display success or error messages -->
      <div v-if="responseMessage" class="response">{{ responseMessage }}</div>
      <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        responseMessage: '', // Success message from the server
        errorMessage: '',    // Error message from the server
      };
    },
    methods: {
      async sendCommand(command) {
        this.responseMessage = ''; // Clear previous messages
        this.errorMessage = '';    // Clear previous errors
  
        try {
          const response = await axios.post('http://192.168.1.108:5000/control', { command });
          this.responseMessage = response.data.message; // Show success message
        } catch (error) {
          console.error('Error communicating with Raspberry Pi:', error);
          if (error.response && error.response.data) {
            this.errorMessage = error.response.data.message; // Show server error message
          } else {
            this.errorMessage = 'Failed to connect to the Raspberry Pi.';
          }
        }
      },
    },
  };
  </script>
  
  <style>
  h1 {
    text-align: center;
    margin-bottom: 20px;
  }
  
  button {
    margin: 10px;
    padding: 10px 20px;
    font-size: 16px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  
  .response {
    margin-top: 20px;
    color: green;
  }
  
  .error {
    margin-top: 20px;
    color: red;
  }
  </style>