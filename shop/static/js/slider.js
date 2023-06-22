// slider.js
// Get the slider element
var sliderElement = document.getElementById('slider');

// Initialize the slider
var slider = new bootstrap.Carousel(sliderElement, {
  interval: false, // Disable automatic sliding
});

// Get the next and previous buttons
var nextButton = document.querySelector('.carousel-control-next');
var prevButton = document.querySelector('.carousel-control-prev');

// Add event listeners for next and previous buttons
nextButton.addEventListener('click', function() {
  slider.next(); // Go to the next slide
});

prevButton.addEventListener('click', function() {
  slider.prev(); // Go to the previous slide
});

