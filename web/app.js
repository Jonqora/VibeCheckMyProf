// app.js

document.addEventListener('DOMContentLoaded', function() {
    const urlInput = document.getElementById('urlInput');
    const messageElement = document.getElementById('message');
    const responseField = document.getElementById('responseField');
    const vibeCheckButton = document.getElementById('vibeCheckButton');
    const loadingOverlay = document.getElementById('loading');
    let pollingInterval;

    // Function to validate if the input URL matches 'https://www.ratemyprofessors.com/professor/<id>' pattern
    function validateUrl(url) {
        const lowerUrl = url.toLowerCase();
        const pattern = /^https:\/\/(www\.)?ratemyprofessors\.com\/professor\/\d+$/;
        return pattern.test(lowerUrl);
    }

    function displayError(message) {
        messageElement.textContent = message;
    }

    function clearError() {
        messageElement.textContent = '';
    }

    function clearRequestInProgress() {
        clearInterval(pollingInterval);
        loadingOverlay.style.display = 'none';
    }

    // Function to send API request to the API Gateway endpoint
    async function sendApiRequest(professorUrl, count) {
        document.getElementById('response-prof').style.display = 'none';
        document.getElementById('response-courses').style.display = 'none';

        // The API URL is loaded from config.js
        // eslint-disable-next-line no-undef
        try {
            const response = await fetch(config.apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                // The URL entered by the user is sent in the request body
                body: JSON.stringify({ url: professorUrl, count: count })
            });

            const data = await response.json();
            const responseCode = JSON.parse(data.statusCode);
            const responseData = JSON.parse(data.body);

            if (responseCode === 200) {
                return responseData;
            } else {
                displayError(responseData.error || 'Unexpected error');
                clearRequestInProgress();
            }

        } catch (error) {
            displayError(`Error: ${error.message}`);
        }
        return null;
    }

    // Function to handle the polling logic
    async function startPolling(professorUrl) {
        loadingOverlay.style.display = 'flex';
        responseField.value = '';
        clearError();
        document.getElementById('response-prof').style.display = 'none';
        document.getElementById('response-courses').style.display = 'none';
        clearInterval(pollingInterval);

        let count = 0; // Initialize poll count
        let prof_name = null;

        const checkStatus = async () => {
            // Send the request with the current count
            const data = await sendApiRequest(professorUrl, count);

            if (data) {
                // Handle the different statuses
                if (data.STATUS === 'DATA_RETRIEVED') {
                    clearRequestInProgress(); // Stop polling on success
                    clearError();
                    renderResponse(data.DATA);
                    responseField.value = `Response: ${JSON.stringify(data, null, 2)}`;
                } else if (data.STATUS === 'ANALYSIS_REQUESTED') {
                    prof_name = data.PROF_NAME;
                    messageElement.textContent = 'New data! Processing takes a while.';
                } else if (data.STATUS === 'ANALYSIS_IN_PROGRESS') {
                    if (prof_name) {
                        messageElement.textContent = `Data processing for ${prof_name} is in progress.`;
                    } else {
                        messageElement.textContent = 'Data processing is in progress.';
                    }
                } else if (data.STATUS === 'ANALYSIS_FAILED') {
                    messageElement.textContent = 'Analysis failed for unknown reasons.';
                    clearRequestInProgress(); // Stop polling if analysis failed
                } else {
                    messageElement.textContent = 'Unknown error response';
                    clearRequestInProgress(); // Stop polling if status is unknown
                }
            }
            count++; // Increment for the next poll
        };

        // Initial request + polling every 15 seconds
        await checkStatus(); // Run first check immediately
        pollingInterval = setInterval(checkStatus, 15000);
    }

    // Event listener for VibeCheck button click
    vibeCheckButton.addEventListener('click', function() {
        const professorUrl = urlInput.value.trim().toLowerCase();

        // Validate the user-inputted URL
        if (!validateUrl(professorUrl)) {
            displayError('URL format is wrong. Must match https://ratemyprofessors.com/professor/<id>');
        } else {
            // Send API request
            clearError();
            startPolling(professorUrl);
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
    const rating = data.rating.toFixed(1);
    const difficulty = data.difficulty.toFixed(1);
    const polarity = transformPolarity(data.vcmp_polarity);
    const subjectivity = transformSubjectivity(data.vcmp_subjectivity);
    const spellingquality = transformSpelling(data.vcmp_spellingquality);

    const professorOverview = document.getElementById('response-prof');
    professorOverview.style.display = 'block'; // Undo display:none
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
                <div class="flex-col quality stats-box" 
                     style="background-color: ${toGradient(rating, 1, 5)}">
                    <div class="quality-stat stats-stat flex-row">
                        <div class="stats-num">${rating}</div>
                        <div class="stats-den">/5</div>
                    </div>
                    <div class="quality-text stats-text">quality</div>
                </div>
                <div class="flex-col difficulty stats-box"
                     style="background-color: ${toGradient(difficulty, 1, 5)}">
                    <div class="difficulty-stat stats-stat flex-row">
                        <div class="stats-num">${difficulty}</div>
                        <div class="stats-den">/5</div>
                    </div>
                    <div class="difficulty-text stats-text">difficulty</div>
                </div>
            </div>
        </div>
        <div class="flex-col stats-vcmp">
            <div class="stats-reviews">Reviews:</div>
            <div class="flex-row stats-2">
                <div class="flex-col polarity stats-box"
                     style="background-color: ${toGradient(polarity, 1, 5)}">
                    <div class="polarity-stat stats-stat flex-row">
                        <div class="stats-num">${polarity}</div>
                        <div class="stats-den">/5</div>
                    </div>
                    <div class="polarity-text stats-text">positivity</div>
                </div>
                <div class="flex-col subjectivity stats-box"
                     style="background-color: ${toGradient(subjectivity, 1, 5)}">
                    <div class="subjectivity-stat stats-stat flex-row">
                        <div class="stats-num">${subjectivity}</div>
                        <div class="stats-den">/5</div>
                    </div>
                    <div class="subjectivity-text stats-text">subjectivity</div>
                </div>
                <div class="flex-col spelling stats-box"
                     style="background-color: ${toGradient(spellingquality, 85, 100)}">
                    <div class="spelling-stat stats-stat">${spellingquality}%</div>
                    <div class="spelling-text stats-text">spelling</div>
                </div>
            </div>
        </div>
    </div>`;

    const coursesComponent = document.getElementById('response-courses');
    coursesComponent.innerHTML = '';
    coursesComponent.style.display = 'block'; // Undo display:none
    for (const course of data.courses) {
        coursesComponent.insertAdjacentHTML('beforeend', renderCourse(course));
    }

    const emojiTooltipContainers = document.querySelectorAll('.emoji-container');

    emojiTooltipContainers.forEach(container => {
        const tooltipTrigger = container.querySelector('.emoji-trigger');
    
        tooltipTrigger.addEventListener('click', (event) => {
            event.stopPropagation(); // Prevent from bubbling to the document
            container.classList.toggle('active');
        });
    });
    
    // Close tooltip if clicked outside
    document.addEventListener('click', () => {
        emojiTooltipContainers.forEach(container => {
            container.classList.remove('active');
        });
    });
}

function renderCourse(courseData) {
    const rating = courseData.rating.toFixed(1);
    const difficulty = courseData.difficulty.toFixed(1);
    const polarity = transformPolarity(courseData.vcmp_polarity);
    const subjectivity = transformSubjectivity(courseData.vcmp_subjectivity);
    const spellingquality = transformSpelling(courseData.vcmp_spellingquality);
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
                    <div class="flex-col quality stats-box"
                         style="background-color: ${toGradient(rating, 0, 5)}">
                        <div class="quality-stat stats-stat flex-row">
                            <div class="stats-num">${rating}</div>
                            <div class="stats-den">/5</div>
                        </div>
                        <div class="quality-text stats-text">quality</div>
                    </div>
                    <div class="flex-col difficulty stats-box"
                         style="background-color: ${toGradient(difficulty, 0, 5)}">
                        <div class="difficulty-stat stats-stat flex-row">
                            <div class="stats-num">${difficulty}</div>
                            <div class="stats-den">/5</div>
                        </div>
                        <div class="difficulty-text stats-text">difficulty</div>
                    </div>
                </div>
            </div>
            <div class="flex-col stats-vcmp">
                <div class="stats-reviews">Reviews:</div>
                <div class="flex-row stats-2">
                    <div class="flex-col polarity stats-box"
                         style="background-color: ${toGradient(polarity, 0, 5)}">
                        <div class="polarity-stat stats-stat flex-row">
                            <div class="stats-num">${polarity}</div>
                            <div class="stats-den">/5</div>
                        </div>
                        <div class="polarity-text stats-text">positivity</div>
                    </div>
                    <div class="flex-col subjectivity stats-box"
                         style="background-color: ${toGradient(subjectivity, 0, 5)}">
                        <div class="subjectivity-stat stats-stat flex-row">
                            <div class="stats-num">${subjectivity}</div>
                            <div class="stats-den">/5</div>
                        </div>
                        <div class="subjectivity-text stats-text">subjectivity</div>
                    </div>
                    <div class="flex-col spelling stats-box"
                         style="background-color: ${toGradient(spellingquality, 90, 100)}">
                        <div class="spelling-stat stats-stat">${spellingquality}%</div>
                        <div class="spelling-text stats-text">spelling</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="flex-row emojis-row">
            ${renderEmojis(courseData.reviews)}
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

function renderEmojis(reviewsData) {
    let emojisHTML = '';
    for (const review of reviewsData) {
        let displayType = 'block';
        if (
            review.comment == null ||
            review.comment.trim() === '' ||
            review.comment.trim().toLowerCase() === 'no comments'
        ) {
            displayType = 'none';
        }
        const reviewHTML = `
            <div class="emoji-container" style="display: ${displayType};">
                <span class="emoji-trigger">${toEmoji(review.vcmp_emotion)}</span>
                <div class="emoji-tooltip">
                    ${review.comment} <br>
                    ${toEmoji(review.vcmp_emotion)} (${review.vcmp_emotion})
                </div>
            </div>
        `;
        emojisHTML += reviewHTML;
    }
    return emojisHTML;
}

function transformPolarity(num) {
    // Standardize -1-1 to 1-5
    let transformed = num * 2 + 3;
    transformed = Math.min(5, Math.max(1, transformed));
    return transformed.toFixed(1);
}

function transformSubjectivity(num) {
    // Standardize 0-1 to 1-5
    let transformed = num * 4 + 1;
    transformed = Math.min(5, Math.max(1, transformed));
    return transformed.toFixed(1);
}

function transformSpelling(num) {
    // Show 0-1 as %
    let transformed = num * 100;
    return transformed.toFixed(0);
}

function toGradient(value, minValue, maxValue) {
    const color1 = '#3d86ff';
    const color2 = '#ff41b5';

    value = Math.max(Math.min(value, maxValue), minValue);

    // Convert hex to RGB
    const color1RGB = [
        parseInt(color1.slice(1, 3), 16),
        parseInt(color1.slice(3, 5), 16),
        parseInt(color1.slice(5, 7), 16)
    ];
    const color2RGB = [
        parseInt(color2.slice(1, 3), 16),
        parseInt(color2.slice(3, 5), 16),
        parseInt(color2.slice(5, 7), 16)
    ];

    // Normalize value to range [0.0, 1.0]
    const factor = (value - minValue) / (maxValue - minValue);

    // Interpolate each RGB channel
    const interpolatedRGB = color1RGB.map((channel, i) =>
        Math.round(channel + (color2RGB[i] - channel) * factor)
    );

    // Convert RGB back to hex
    const interpolatedHex = `#${interpolatedRGB
        .map(channel => channel.toString(16).padStart(2, '0'))
        .join('')}`;

    return interpolatedHex;
}

function toEmoji(emotion) {
    const emojiMap = {
        admiration: '👏',
        amusement: '😂',
        anger: '😡',
        annoyance: '😒',
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
        relief: '😅',
        remorse: '😟',
        sadness: '😢',
        surprise: '😮',
        neutral: '❓'
    };
  
    // Return the matching emoji or a default question mark if not found
    return emojiMap[emotion.toLowerCase()] || '❓';
}
