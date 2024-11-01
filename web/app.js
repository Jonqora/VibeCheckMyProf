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
                const responseData = JSON.parse(data.body);
                renderResponse(responseData);
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

function renderResponse(data) {
    const professorOverview = document.getElementById('response-prof');
    console.log(transformPolarity(-1)); // Expected output: 0.0
    console.log(transformPolarity(0));  // Expected output: 2.5
    console.log(transformPolarity(1));  // Expected output: 5.0
    professorOverview.innerHTML = '';
    professorOverview.innerHTML = `
    <div class="prof-name">${data.name}</div>
    <div class="school-name">${data.school_name}</div>
    <div class="flex-row vibes-row">
        ${renderVibes(data.vcmp_emotion, data.num_ratings)}
    </div>
    <div class="flex-row feels-row">
        ${renderFeels(data.vcmp_sentiment, data.num_ratings)}
    </div>
    <div class="flex-row stats-row">
        <div class="flex-col stats-rmp">
            <div class="stats-prof">Prof:</div>
            <div class="flex-row stats-1">
                <div class="flex-col quality stats-box">
                    <div class="quality-stat stats-stat flex-row">
                        <div class="stats-num">${data.rating.toFixed(1)}</div>
                        <div class="stats-den">/5</div>
                    </div>
                    <div class="quality-text stats-text">quality</div>
                </div>
                <div class="flex-col difficulty stats-box">
                    <div class="difficulty-stat stats-stat flex-row">
                        <div class="stats-num">${data.difficulty.toFixed(1)}</div>
                        <div class="stats-den">/5</div>
                    </div>
                    <div class="difficulty-text stats-text">difficulty</div>
                </div>
            </div>
        </div>
        <div class="flex-col stats-vcmp">
            <div class="stats-reviews">Reviews:</div>
            <div class="flex-row stats-2">
                <div class="flex-col polarity stats-box" >
                    <div class="polarity-stat stats-stat flex-row">
                        <div class="stats-num">${transformPolarity(data.vcmp_polarity)}</div>
                        <div class="stats-den">/5</div>
                    </div>
                    <div class="polarity-text stats-text">positivity</div>
                </div>
                <div class="flex-col subjectivity stats-box">
                    <div class="subjectivity-stat stats-stat flex-row">
                        <div class="stats-num">${transformSubjectivity(data.vcmp_subjectivity)}</div>
                        <div class="stats-den">/5</div>
                    </div>
                    <div class="subjectivity-text stats-text">subjectivity</div>
                </div>
                <div class="flex-col spelling stats-box">
                    <div class="spelling-stat stats-stat">${transformSpelling(data.vcmp_spellingquality)}%</div>
                    <div class="spelling-text stats-text">spelling</div>
                </div>
            </div>
        </div>
    </div>`;

    const coursesComponent = document.getElementById('response-courses');
    coursesComponent.innerHTML = '';
    for (const course of data.courses) {
        coursesComponent.insertAdjacentHTML('beforeend', renderCourse(course));
    }
}

function renderCourse(courseData) {
    const html = `
    <div class="course">
        <div class="course-name">${courseData.course_name}</div>
        <div class="flex-row vibes-row">
            ${renderVibes(courseData.vcmp_emotion, courseData.num_ratings)}
        </div>
        <div class="flex-row feels-row">
            ${renderFeels(courseData.vcmp_sentiment, courseData.num_ratings)}
        </div>
        <div class="flex-row stats-row">
            <div class="flex-col stats-rmp">
                <div class="stats-prof">Prof:</div>
                <div class="flex-row stats-1">
                    <div class="flex-col quality stats-box">
                        <div class="quality-stat stats-stat flex-row">
                            <div class="stats-num">${courseData.rating.toFixed(1)}</div>
                            <div class="stats-den">/5</div>
                        </div>
                        <div class="quality-text stats-text">quality</div>
                    </div>
                    <div class="flex-col difficulty stats-box">
                        <div class="difficulty-stat stats-stat flex-row">
                            <div class="stats-num">${courseData.difficulty.toFixed(1)}</div>
                            <div class="stats-den">/5</div>
                        </div>
                        <div class="difficulty-text stats-text">difficulty</div>
                    </div>
                </div>
            </div>
            <div class="flex-col stats-vcmp">
                <div class="stats-reviews">Reviews:</div>
                <div class="flex-row stats-2">
                    <div class="flex-col polarity stats-box">
                        <div class="polarity-stat stats-stat flex-row">
                            <div class="stats-num">${transformPolarity(courseData.vcmp_polarity)}</div>
                            <div class="stats-den">/5</div>
                        </div>
                        <div class="polarity-text stats-text">positivity</div>
                    </div>
                    <div class="flex-col subjectivity stats-box">
                        <div class="subjectivity-stat stats-stat flex-row">
                            <div class="stats-num">${transformSubjectivity(courseData.vcmp_subjectivity)}</div>
                            <div class="stats-den">/5</div>
                        </div>
                        <div class="subjectivity-text stats-text">subjectivity</div>
                    </div>
                    <div class="flex-col spelling stats-box">
                        <div class="spelling-stat stats-stat">${transformSpelling(courseData.vcmp_spellingquality)}%</div>
                        <div class="spelling-text stats-text">spelling</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `;
    return html;
}

function renderVibes(vibesData, numRatings) {
    // Generate HTML string or  for the vibes-row content
    const emotion1 = vibesData[0];
    const emotion2 = vibesData.length > 1 ? vibesData[1] : null;
    const emotion3 = vibesData.length > 2 ? vibesData[2] : null;
    let content = `
    <div class="vibes-text">Vibes:</div>
    <div class="vibes">${toEmoji(emotion1[0])} ${emotion1[0]} (${emotion1[1]})</div>
    `;
    if (emotion2 !== null) {
        content += `<div class="vibes">${toEmoji(emotion2[0])} ${emotion2[0]} (${emotion2[1]})</div>`;
    }
    if (emotion3 !== null) {
        content += `<div class="vibes">${toEmoji(emotion3[0])} ${emotion3[0]} (${emotion3[1]})</div>`;
    }
    return content;
}

function renderFeels(feelsData, numRatings) {
    return `
        <div class="feels-text">Feels:</div>
        <div class="feels-positive feels">⬆️ positive (${feelsData.positive})</div>
        <div class="feels-negative feels">⬇️ negative (${feelsData.negative})</div>
        <div class="feels-neutral feels">⏺️ neutral (${feelsData.neutral})</div>
        <div class="feels-mixed feels">🔀 mixed (${feelsData.mixed})</div>
    `;
}

function transformPolarity(num) {
    // Standardize -1-1 to 0-5
    let transformed = num * 2.5 + 2.5;
    transformed = Math.min(5, Math.max(0, transformed));
    return transformed.toFixed(1);
}

function transformSubjectivity(num) {
    // Standardize 0-1 to 0-5
    let transformed = num * 5;
    transformed = Math.min(5, Math.max(0, transformed));
    return transformed.toFixed(1);
}

function transformSpelling(num) {
    // Show 0-1 as %
    let transformed = num * 100;
    return transformed.toFixed(0);
}

function toEmoji(emotion) {
    const emojiMap = {
        admiration: '👏',
        amusement: '😂',
        anger: '😡',
        annoyance: '😠',
        approval: '👍',
        caring: '🩷',
        confusion: '🤨',
        curiosity: '🔍',
        desire: '✨',
        disappointment: '😞',
        disapproval: '👎',
        disgust: '🤮',
        embarrassment: '😳',
        excitement: '🤩',
        fear: '😨',
        gratitude: '🙏',
        grief: '😭',
        joy: '😃',
        love: '❤️',
        nervousness: '😬',
        optimism: '🤞',
        pride: '😤',
        realization: '👀',
        relief: '😌',
        remorse: '😟',
        sadness: '😢',
        surprise: '😮'
    };
  
    // Return the matching emoji or a default question mark if not found
    return emojiMap[emotion.toLowerCase()] || '❓';
}
