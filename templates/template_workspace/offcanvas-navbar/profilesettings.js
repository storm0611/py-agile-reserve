// ### This code here works for the phone and email of the user incase studystash needs the user urgently 

  const updatePhoneButtonTask = document.getElementById("updatePhoneButtonTask");
  const phoneInputTask = document.getElementById("phoneInputTask");
  const phoneFormTask = document.getElementById("phoneFormTask");
  
  updatePhoneButtonTask.addEventListener("click", function() {
      phoneInputTask.value = "";
      phoneInputTask.placeholder = "";
  });
  
  phoneForm.addEventListener("submit", function(event) {
      event.preventDefault();
      // Save phone input value to your backend or perform other actions
      console.log("Phone form submitted");
  });

  const updateEmailButtonTask = document.getElementById("updateEmailButtonTask");
  const emailInputTask = document.getElementById("emailInputTask");
  const emailFormTask = document.getElementById("emailFormTask");

  updateEmailButtonTask.addEventListener("click", function() {
      emailInputTask.value = "";
      emailInputTask.placeholder = "";
  });

  emailFormTask.addEventListener("submit", function(event) {
      event.preventDefault();
      // Save email input value to your backend or perform other actions
      console.log("Email form submitted");
  });




// #### this code is for the email provided by the user for the communication with studystash


  const emailInput1 = document.getElementById("emailInput1");
  const originalPlaceholder = emailInput1.placeholder; // Store the original placeholder

  // After clicking outside the input, restore the original placeholder
  emailInput1.addEventListener("click", function() {
          emailInput1.value = ""; 
          emailInput1.placeholder = "";
      
  });



// #### this code is for the billing information

  const updateBillingButton = document.getElementById("updateBillingButton");
  const cardNumberInput = document.getElementById("cardNumber");
  const cvvInput = document.getElementById("cvv");
  const expireDateInput = document.getElementById("expireDate");

  updateBillingButton.addEventListener("click", function() {
      cardNumberInput.value = "";
      cardNumberInput.placeholder = "";
      cvvInput.value = "";
      cvvInput.placeholder = "";
      expireDateInput.value = "";
      expireDateInput.placeholder = "";
  });


// ### This code works for the password change issues 

                              const changePasswordButton = document.getElementById("changePasswordButton");
                              const passwordFields = document.getElementById("passwordFields");
                              const cancelPasswordFormButton = document.getElementById("cancelPasswordFormButton");
                          
                              changePasswordButton.addEventListener("click", function() {
                                  passwordFields.style.display = "block";
                              });
                          
                              cancelPasswordFormButton.addEventListener("click", function() {
                                  passwordFields.style.display = "none";
                              });
    

// ### This code here updates the time every

   // Wait for the DOM (HTML document) to be fully loaded and parsed
   document.addEventListener("DOMContentLoaded", function () {
    // Select the HTML element with the ID "current-year" from the document
    const currentYearElem = document.querySelector("#current-year");
   
    // Create a new Date object representing the current date and time
    const currentYear = new Date().getFullYear();
   
    // Update the content of the selected element with the current year
    currentYearElem.textContent = currentYear;
   });
    