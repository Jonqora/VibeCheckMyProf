// app.js

document.addEventListener('DOMContentLoaded', function() {
    const urlInput = document.getElementById('urlInput');
    const errorElement = document.getElementById('error');
    const responseField = document.getElementById('responseField');
    const vibeCheckButton = document.getElementById('vibeCheckButton');

    // Function to validate if the input URL matches 'https://www.ratemyprofessors.com/professor/<id>' pattern
    function validateUrl(url) {
        const lowerUrl = url.toLowerCase();
        const pattern = /^https:\/\/(www\.)?ratemyprofessors\.com\/professor\/\d+$/;
        return pattern.test(lowerUrl);
    }

    function displayError(message) {
        errorElement.textContent = message;
    }

    function clearError() {
        errorElement.textContent = '';
    }

    // Function to send API request to the API Gateway endpoint
    function sendApiRequest(professorUrl) {
        // The API URL is loaded from config.js
        // eslint-disable-next-line no-undef
        fetch(config.apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            // The URL entered by the user is sent in the request body
            body: JSON.stringify({ url: professorUrl })
        })
            .then(response => response.json())
            .then(data => {
                // Display the API response in the text area
                responseField.value = `Response: ${JSON.stringify(data, null, 2)}`;
            })
            .catch(error => {
                // Display error message if the request fails
                responseField.value = `Error: ${error.message}`;
            });
    }

    // Event listener for VibeCheck button click
    vibeCheckButton.addEventListener('click', function() {
        const professorUrl = urlInput.value.trim().toLowerCase();

        // Validate the user-inputted URL
        if (!validateUrl(professorUrl)) {
            displayError('URL format is wrong. Must match https://ratemyprofessors.com/professor/<id>');
        } else {
            clearError();
            // Send the professor URL to the API Gateway endpoint
            sendApiRequest(professorUrl);
        }
    });

    // Event listener for Enter key press in the input field
    urlInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            vibeCheckButton.click(); // Trigger the VibeCheck button click
        }
    });
});
