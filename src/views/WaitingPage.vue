<template>
  <div class="waiting-page">
    <h1>Order in Progress</h1>
    <img src= "/logo.png"/>
    <h2>Your order is being processed. Please wait...</h2>
    <p>________</p>
    <!-- <h4>Estimated Time: {{ formatTime(timeLeft) }}</h4> -->
    <h4 v-if="timeLeft>0">Estimated Time: {{ (timeLeft) }}</h4>
    <!-- <button v-if="showSpinner=falase"> Menu </button> -->
    <hr>
  </div>

  <!-- Conditionally render the spinner only if showSpinner is true -->
  <div id="container" v-if="showSpinner">
    <svg viewBox="0 0 100 100">
      <defs>
        <filter id="shadow">
          <feDropShadow dx="0" dy="0" stdDeviation="1.9" flood-color="#FFFFFF" />
        </filter>
      </defs>
      <circle
        id="spinner"
        style="fill:transparent;stroke:#7d3425;stroke-width: 
        7px;stroke-linecap: round;filter:url(#shadow);"
        cx="45"
        cy="50"
        r="40"
      />
    </svg>
  </div>
  <div class="mt-4"/>
</template>

<script>
export default {
  name: 'WaitingPage',
  data() {
    return {
      timeLeft: 10, // Start the countdown at 120 seconds
      showSpinner: true, // Show the spinner initially
    };
  },
  mounted() {
    this.startCountdown();
  },
  methods: {
    // Method to start the countdown
    startCountdown() {
      const countdownInterval = setInterval(() => {
        if (this.timeLeft > 0) {
          this.timeLeft -= 1;
        } else {
          this.showSpinner = false; // Hide the spinner when countdown reaches 0
          clearInterval(countdownInterval); // Stop the countdown when it reaches 0
        }
      }, 1000); // Decrease the timeLeft by 1 every second
    },
    // Method to format the time as mm:ss
    formatTime(seconds) {
      const minutes = Math.floor(seconds / 60);
      const secs = seconds % 60;
      return `${minutes}:${secs < 10 ? '0' : ''}${secs}`;
    },
  },
};
</script>

<style>

</style>