<template>
    <div class="waiting-page">
      <h1>Order in Progress</h1>
      <p>Your order is being processed. Please wait...</p>
      <hr>
    </div>

    <div id="container">
  <svg viewBox="0 0 100 100">
    <defs>
      <filter id="shadow">
        <feDropShadow dx="0" dy="0" stdDeviation="1.5" flood-color="#FFFFFF"/>
      </filter>
    </defs>
    <circle id="spinner" style="fill:transparent;stroke:#7d3425;stroke-width: 7px;stroke-linecap: round;filter:url(#shadow);" cx="50" cy="50" r="45"/>
</svg>
</div>
  </template>
  
  <script>
  export default {
    name: 'WaitingPage'
  };

  </script>
  
  <style>

hr{
  height: 100px;
  border: none;  /* Remove the default border */
  border-top: 5px solid black;
}

#container {

  width: 300px;
  height: 300px;
}

@keyframes animation {
  0% {
    stroke-dasharray: 1 98;
    stroke-dashoffset: -105;
  }
  50% {
    stroke-dasharray: 80 10;
    stroke-dashoffset: -160;
  }
  100% {
    stroke-dasharray: 1 98;
    stroke-dashoffset: -300;
  }
}

#spinner {
  transform-origin: center;
  animation-name: animation;
  animation-duration: 2s;
  animation-timing-function: cubic-bezier;
  animation-iteration-count: infinite;
}
  
  .waiting-page {
    text-align: center;
    margin-top: 50px;

  }
  </style>