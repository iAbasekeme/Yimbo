#!/usr/bin/node
/* js podcast script */

document.addEventListener("DOMContentLoaded", function() {
  // Get all category links
  var categoryLinks = document.querySelectorAll('.category a');
  var catLinkLen = categoryLinks.length;

  for (var i = 0; i < catLinkLen; i++) {
    var link = categoryLinks[i];

    // Add a click event listener to each category link
    link.addEventListener('click', function(event) {
      event.preventDefault();

      // Extract the category name from the text content of the clicked link
      var category = link.textContent;
      
      // Find the nearest ancestor element with class 'display_content'
      var displayContent = link.closest('.display_content');
      
      // Find the nearest h3 element within the ancestor element and get the text content of h3
      var h3Element = displayContent.querySelector('h3');
      var tableName = h3Element.textContent;

      // Send a request to the backend server to sort data by category and table
      fetch('/sort_category', {
        method: "POST",
        // Specify that the data being sent is in JSON format
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ category: category, table: tableName })
      })
      .then(data => {
        // Handle the response from the server if needed
        console.log('Category:', data.category);
        console.log('Table:', data.table);
      })
      .catch(error => {
        // Log any errors to the browser's console
        console.error('Error:', error);
      });
    });
  }
});

