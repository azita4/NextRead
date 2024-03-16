document.addEventListener("DOMContentLoaded", function() {
    var myButton = document.querySelector(".button1");

    // Add a click event listener to the button
    myButton.addEventListener("click", function() {
        // Navigate to the desired page (replace '/other_page' with the actual route)
        window.location.href = '/other_page';
    });
});