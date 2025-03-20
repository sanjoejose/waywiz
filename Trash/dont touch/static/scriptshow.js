document.getElementById('pathForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const start = document.getElementById('start').value;
    const end = document.getElementById('end').value;
    const resultDiv = document.getElementById('result');
    const pathInfo = document.getElementById('pathInfo');
    const currentStep = document.getElementById('currentStep');
    const nextButton = document.getElementById('nextButton');
    
    pathInfo.innerHTML = 'Calculating...';
    currentStep.innerHTML = '';
    nextButton.style.display = 'none';
    
    try {
        const response = await fetch('/shortest-path', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ start, end })
        });
        
        const data = await response.json();
        
        if (data.distance === Infinity) {
            pathInfo.innerHTML = 'No path found.';
            currentStep.innerHTML = '';
        } else {
            pathInfo.innerHTML = `
                <p>Shortest Path: ${data.path.join(' -> ')}</p>
                <p>Total Distance: ${data.distance}</p>
            `;
            
            // Store directions and initialize the current step
            let directions = data.directions;
            let currentStepIndex = 0;
            
            // Function to display the next step
            function showNextStep() {
                if (currentStepIndex < directions.length) {
                    currentStep.innerHTML = `Step ${currentStepIndex + 1}: Go ${directions[currentStepIndex]}`;
                    currentStepIndex++;
                } else {
                    currentStep.innerHTML = 'You have reached your destination!';
                    nextButton.style.display = 'none'; // Hide button when done
                }
            }
            
            // Show the first direction and set up the button
            showNextStep();
            nextButton.style.display = 'inline';
            nextButton.onclick = showNextStep;
        }
    } catch (error) {
        pathInfo.innerHTML = 'An error occurred. Please try again.';
    }
});
