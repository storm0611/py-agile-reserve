/**
* Template Name: Ninestars - v4.8.0
* Template URL: https://bootstrapmade.com/ninestars-free-bootstrap-3-theme-for-creative/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/
(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    let selectEl = select(el, all)
    if (selectEl) {
      if (all) {
        selectEl.forEach(e => e.addEventListener(type, listener))
      } else {
        selectEl.addEventListener(type, listener)
      }
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select('#navbar .scrollto', true)
  const navbarlinksActive = () => {
    let position = window.scrollY + 200
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return
      let section = select(navbarlink.hash)
      if (!section) return
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active')
      } else {
        navbarlink.classList.remove('active')
      }
    })
  }
  window.addEventListener('load', navbarlinksActive)
  onscroll(document, navbarlinksActive)

  /**
   * Scrolls to an element with header offset
   */
  const scrollto = (el) => {
    let header = select('#header')
    let offset = header.offsetHeight

    let elementPos = select(el).offsetTop
    window.scrollTo({
      top: elementPos - offset,
      behavior: 'smooth'
    })
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Mobile nav toggle
   */
  on('click', '.mobile-nav-toggle', function(e) {
    select('#navbar').classList.toggle('navbar-mobile')
    this.classList.toggle('bi-list')
    this.classList.toggle('bi-x')
  })

  /**
   * Mobile nav dropdowns activate
   */
  on('click', '.navbar .dropdown > a', function(e) {
    if (select('#navbar').classList.contains('navbar-mobile')) {
      e.preventDefault()
      this.nextElementSibling.classList.toggle('dropdown-active')
    }
  }, true)

  /**
   * Scrool with ofset on links with a class name .scrollto
   */
  on('click', '.scrollto', function(e) {
    if (select(this.hash)) {
      e.preventDefault()

      let navbar = select('#navbar')
      if (navbar.classList.contains('navbar-mobile')) {
        navbar.classList.remove('navbar-mobile')
        let navbarToggle = select('.mobile-nav-toggle')
        navbarToggle.classList.toggle('bi-list')
        navbarToggle.classList.toggle('bi-x')
      }
      scrollto(this.hash)
    }
  }, true)

  /**
   * Scroll with ofset on page load with hash links in the url
   */
  window.addEventListener('load', () => {
    if (window.location.hash) {
      if (select(window.location.hash)) {
        scrollto(window.location.hash)
      }
    }
  });

  /**
   * Porfolio isotope and filter
   */
  window.addEventListener('load', () => {
    let portfolioContainer = select('.portfolio-container');
    if (portfolioContainer) {
      let portfolioIsotope = new Isotope(portfolioContainer, {
        itemSelector: '.portfolio-item',
        layoutMode: 'fitRows'
      });

      let portfolioFilters = select('#portfolio-flters li', true);

      on('click', '#portfolio-flters li', function(e) {
        e.preventDefault();
        portfolioFilters.forEach(function(el) {
          el.classList.remove('filter-active');
        });
        this.classList.add('filter-active');

        portfolioIsotope.arrange({
          filter: this.getAttribute('data-filter')
        });
        portfolioIsotope.on('arrangeComplete', function() {
          AOS.refresh()
        });
      }, true);
    }

  });

  /**
   * Initiate portfolio lightbox 
   */
  const portfolioLightbox = GLightbox({
    selector: '.portfolio-lightbox'
  });

  /**
   * Portfolio details slider
   */
  new Swiper('.portfolio-details-slider', {
    speed: 400,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    }
  });

  /**
   * Clients Slider
   */
  new Swiper('.clients-slider', {
    speed: 400,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    slidesPerView: 'auto',
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    },
    breakpoints: {
      320: {
        slidesPerView: 2,
        spaceBetween: 40
      },
      480: {
        slidesPerView: 3,
        spaceBetween: 60
      },
      640: {
        slidesPerView: 4,
        spaceBetween: 80
      },
      992: {
        slidesPerView: 6,
        spaceBetween: 120
      }
    }
  });

  /**
   * Animation on scroll
   */
  window.addEventListener('load', () => {
    AOS.init({
      duration: 1000,
      easing: "ease-in-out",
      once: true,
      mirror: false
    });
  });

})()





let currentSection = 1;
const totalSections = 4;

function showNext() {
  if (currentSection < totalSections) {
    currentSection++;
    hideAllSections();
    document.getElementById(`section${currentSection}`).style.display = "block";
  }
}

function showPrevious() {
  if (currentSection > 1) {
    currentSection--;
    hideAllSections();
    document.getElementById(`section${currentSection}`).style.display = "block";
  }
}

function hideAllSections() {
  for (let i = 1; i <= totalSections; i++) {
    document.getElementById(`section${i}`).style.display = "none";
  }
}


// Keep track of the number of clicks for each product
const productClicks = {};

let totalItems = 0;
let totalPrice = 0;


function addToCart(price, productName) {
  totalItems++;
  if (productClicks[productName]) {
    productClicks[productName]++;
  } else {
    productClicks[productName] = 1;
  }

  updateCartValues(price, productClicks[productName]);
  updateModalTable();
}

function updateCartValues(price, quantity) {
  totalItems += quantity;
  totalPrice += price * quantity;
  document.getElementById("totalItems").value = totalItems;
  document.getElementById("totalPrice").value = "$" + totalPrice;
}

function proceedToCheckout() {
  // Implement your logic to proceed to checkout
  // This function can redirect the user to a checkout page or trigger any other relevant action.
  // For the purpose of this example, let's close the modal.
  $('#exampleModal').modal('hide');
}


function incrementQuantity(productName, price) {
  productClicks[productName]++;
  updateCartValues(price, productClicks[productName]);
  updateModalTable();
}

function decrementQuantity(productName, price) {
  if (productClicks[productName] > 1) {
    productClicks[productName]--;
    updateCartValues(-price, productClicks[productName]);
    updateModalTable();
  } else {
    delete productClicks[productName];
    updateCartValues(-price, 0);
    updateModalTable();
  }
}



function updateModalTable() {
  const selectedProductsTableBody = document.getElementById('selectedProductsTable').getElementsByTagName('tbody')[0];
  selectedProductsTableBody.innerHTML = '';

  totalPrice = 0; // Initialize the totalPrice variable

  for (const productName in productClicks) {
    const productQuantity = productClicks[productName];
    const productPrice = getProductPrice(productName);
    const productTotalPrice = productQuantity * productPrice;

    // Update the modal table with the selected products and their quantities
    const row = selectedProductsTableBody.insertRow();
    row.innerHTML = `
      <td>${productName}</td>
      <td>${productQuantity}</td>
      <td>
        <div class="btn-group" role="group" aria-label="Increment/Decrement">
          <button type="button" class="btn btn-secondary" onclick="decrementQuantity('${productName}', ${productPrice})">-</button>
          <button type="button" class="btn btn-secondary" onclick="incrementQuantity('${productName}', ${productPrice})">+</button>
        </div>
      </td>
    `;

    // Add the productTotalPrice to the totalPrice
    totalPrice += productTotalPrice;
  }

  // Update the total amount to be paid in the modal
  const totalAmountElement = document.getElementById('totalAmount');
  totalAmountElement.textContent = `$${totalPrice}`;
}


// Function to get the price of a product based on its name
function getProductPrice(productName) {
  // You can implement this function based on how you are storing the product prices
  // For example, you can have an object or a database where you store the product names and prices
  // Here, I'm using a simple example with hard-coded prices for demonstration purposes
  const prices = {
    'Product 13EE': 20,
    'Product 14': 30,
    'Product 15': 25,
    'Product 16FF': 35,
    'Product 17': 40,
    'Product jjngdf': 28,
    // Add more products and their prices as needed
  };

  // Return the price of the product based on its name
  return prices[productName] || 0; // Default to 0 if the product name is not found in the prices object
  console.log('Received Product Name:', productName);
  console.log('Returned Product Price:', prices[productName] || 0);

}

//This code here works if the uploaded document is not a pdf an error occurs

