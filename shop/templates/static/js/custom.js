document.addEventListener("DOMContentLoaded", function() {
    const slider = document.querySelector(".slider");
    const slides = Array.from(slider.children);
    const slideWidth = slides[0].getBoundingClientRect().width;
    
    // Set the width of the slider to accommodate all slides
    slider.style.width = `${slideWidth * slides.length}px`;
  
    function moveToSlide(slider, currentSlide, targetSlide) {
      slider.style.transform = `translateX(-${targetSlide.style.left})`;
      currentSlide.classList.remove("active");
      targetSlide.classList.add("active");
    }
  
    function updateNavButtons(currentSlide, prevButton, nextButton) {
      if (currentSlide === slides[0]) {
        prevButton.setAttribute("disabled", true);
      } else {
        prevButton.removeAttribute("disabled");
      }
      if (currentSlide === slides[slides.length - 1]) {
        nextButton.setAttribute("disabled", true);
      } else {
        nextButton.removeAttribute("disabled");
      }
    }
  
    function handlePrevSlide() {
      const currentSlide = slider.querySelector(".active");
      const prevSlide = currentSlide.previousElementSibling;
      moveToSlide(slider, currentSlide, prevSlide);
      updateNavButtons(prevSlide, prevButton, nextButton);
    }
  
    function handleNextSlide() {
      const currentSlide = slider.querySelector(".active");
      const nextSlide = currentSlide.nextElementSibling;
      moveToSlide(slider, currentSlide, nextSlide);
      updateNavButtons(nextSlide, prevButton, nextButton);
    }
  
    const prevButton = document.getElementById("prev-button");
    const nextButton = document.getElementById("next-button");
  
    prevButton.addEventListener("click", handlePrevSlide);
    nextButton.addEventListener("click", handleNextSlide);
  });