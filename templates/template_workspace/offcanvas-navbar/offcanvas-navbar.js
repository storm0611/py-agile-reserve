(() => {
  'use strict'

  document.querySelector('#navbarSideCollapse').addEventListener('click', () => {
    document.querySelector('.offcanvas-collapse').classList.toggle('open')
  })
})()





  // Wait for the document to be fully loaded before attaching event listeners
  document.addEventListener('DOMContentLoaded', function() {
    // Get the link element with the id "openModalLink"
    var openModalLink = document.getElementById('openModalLink');
    
    // Get the modal element by its ID
    var modal = new bootstrap.Modal(document.getElementById('staticBackdrop'));
    
    // Attach a click event listener to the link element
    openModalLink.addEventListener('click', function(event) {
      // Prevent the default behavior of the link (e.g., navigating to the href)
      event.preventDefault();
      
      // Show the modal
      modal.show();
    });
  });

  

//This script works on the courses we support link

 // Wait for the document to be fully loaded before attaching event listeners
 document.addEventListener('DOMContentLoaded', function() {
  // Get the link element with the id "openCourseModalLink"
  var openModalLink = document.getElementById('openCoursesModalLink');
  
  // Get the modal element by its ID
  var modal = new bootstrap.Modal(document.getElementById('coursesModal'));
  
  // Attach a click event listener to the link element
  openModalLink.addEventListener('click', function(event) {
    // Prevent the default behavior of the link (e.g., navigating to the href)
    event.preventDefault();
    
    // Show the modal
    modal.show();
  });
});





    document.addEventListener('DOMContentLoaded', function() {
        // Get the course list element and search input element
        var courseList = document.getElementById('courseList');
        var courseSearchInput = document.getElementById('courseSearchInput');

        // Filter the course list based on the search input
        courseSearchInput.addEventListener('input', function(event) {
            var searchTerm = event.target.value.toLowerCase();
            var listItems = courseList.getElementsByTagName('li');

            for (var i = 0; i < listItems.length; i++) {
                var listItem = listItems[i];
                var text = listItem.textContent.toLowerCase();

                if (text.indexOf(searchTerm) > -1) {
                    listItem.style.display = 'block';
                } else {
                    listItem.style.display = 'none';
                }
            }
        });
    });



    // Wait for the document to be fully loaded before attaching event listeners
    document.addEventListener('DOMContentLoaded', function() {
      // Get the link element with the class "nav-link"
      var scholarshipLoansLink = document.querySelector('a.nav-link[href="#scholarshipLoansModal"]');

      // Get the modal element by its ID
      var scholarshipLoansModal = new bootstrap.Modal(document.getElementById('scholarshipLoansModal'));

      // Attach a click event listener to the link element
      scholarshipLoansLink.addEventListener('click', function(event) {
          // Prevent the default behavior of the link (e.g., navigating to the href)
          event.preventDefault();

          // Show the modal
          scholarshipLoansModal.show();
      });
  });


   // Get a reference to the "Employment" link using its ID
   const employmentLink = document.getElementById('employmentLink');

   // Get a reference to the modal using its ID
   const employmentModal = new bootstrap.Modal(document.getElementById('employmentModal'));
 
   // Add a click event listener to the link
   employmentLink.addEventListener('click', function (event) {
     event.preventDefault(); // Prevent the default link behavior
     employmentModal.show(); // Show the modal when the link is clicked
   });

  
   
   // Wait for the DOM (HTML document) to be fully loaded and parsed
document.addEventListener("DOMContentLoaded", function () {
 // Select the HTML element with the ID "current-year" from the document
 const currentYearElem = document.querySelector("#current-year");

 // Create a new Date object representing the current date and time
 const currentYear = new Date().getFullYear();

 // Update the content of the selected element with the current year
 currentYearElem.textContent = currentYear;
});
 