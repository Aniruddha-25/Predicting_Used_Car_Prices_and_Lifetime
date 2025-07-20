
// ===================================
// CAR PREDICTION APP - CLEAN SCRIPT
// ===================================

console.log('🚗 Car Prediction App JavaScript Loading...');

// Main initialization when DOM loads
document.addEventListener("DOMContentLoaded", function () {
  console.log('🚀 Initializing Car Prediction App...');
  
  // Set max date for year input (manufacturing date shouldn't be in future)
  const yearInput = document.getElementById("year");
  if (yearInput) {
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, "0");
    const dd = String(today.getDate()).padStart(2, "0");
    yearInput.max = `${yyyy}-${mm}-${dd}`;
    
    // Set minimum date to reasonable car manufacturing start (e.g., 1980)
    yearInput.min = "1980-01-01";
    console.log('✅ Year input date range set (1980 - today)');
  }

  // Initialize background slideshow
  initBackgroundSlideshow();

  // Initialize form validation
  initFormValidation();

  console.log('✅ All modules loaded successfully');
});

// Background slideshow function
function initBackgroundSlideshow() {
  console.log('🎨 Starting background slideshow...');
  
  const bgImages = [
    "/static/images/Car_1.webp",
    "/static/images/Car_2.jpeg",
    "/static/images/Car_3.jpg",
    "/static/images/Car_4.jpeg"
  ];

  const bgA = document.getElementById("bg-slideshow-a");
  const bgB = document.getElementById("bg-slideshow-b");

  if (bgA && bgB) {
    let currentIndex = 0;
    let isShowingA = true;

    // Set first background
    bgA.style.backgroundImage = `url('${bgImages[0]}')`;
    bgA.classList.add("active");
    console.log('✅ Background slideshow started');

    // Change background every 4 seconds
    setInterval(() => {
      currentIndex = (currentIndex + 1) % bgImages.length;
      
      if (isShowingA) {
        bgB.style.backgroundImage = `url('${bgImages[currentIndex]}')`;
        bgB.classList.add("active");
        bgA.classList.remove("active");
      } else {
        bgA.style.backgroundImage = `url('${bgImages[currentIndex]}')`;
        bgA.classList.add("active");
        bgB.classList.remove("active");
      }
      
      isShowingA = !isShowingA;
    }, 4000);
  } else {
    console.error('❌ Background elements not found');
  }
}

// Form validation function
function initFormValidation() {
  console.log('📝 Setting up form validation...');
  
  const form = document.getElementById('carForm');
  if (!form) {
    console.error('❌ Form not found');
    return;
  }

  // Mileage input - numbers only
  const mileageInput = document.getElementById('mileage');
  if (mileageInput) {
    mileageInput.addEventListener('input', function(e) {
      e.target.value = e.target.value.replace(/[^0-9]/g, '');
    });
  }

  // Model input - capitalize
  const modelInput = document.getElementById('model');
  if (modelInput) {
    modelInput.addEventListener('input', function(e) {
      e.target.value = e.target.value.replace(/\b\w/g, l => l.toUpperCase());
    });
  }

  // Form submission validation
  form.addEventListener('submit', function(e) {
    const brand = document.getElementById('brand').value;
    const model = document.getElementById('model').value;
    const year = document.getElementById('year').value;
    const fuel = document.getElementById('fuel').value;
    const mileage = document.getElementById('mileage').value;
    const transmission = document.querySelector('input[name="transmission"]:checked');

    if (!brand || !model || !year || !fuel || !mileage || !transmission) {
      e.preventDefault();
      alert('Please fill in all required fields!');
      return false;
    }

    console.log('✅ Form validation passed');
    return true;
  });

  console.log('✅ Form validation ready');
}

console.log('✅ JavaScript file loaded completely');
