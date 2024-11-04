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
            
            let directions = data.directions;
            let currentStepIndex = 0;
            
            function showNextStep() {
                if (currentStepIndex < directions.length) {
                    const directionText = `Node ${data.path[currentStepIndex + 1]}: Go ${directions[currentStepIndex]}`;
                    currentStep.innerHTML = directionText;
                    speak(directionText); // Call speak function for audio guidance
                    currentStepIndex++;
                } else {
                    currentStep.innerHTML = 'You have reached your destination!';
                    speak('You have reached your destination!');
                    nextButton.style.display = 'none';
                }
            }
            
            function speak(text) {
                const utterance = new SpeechSynthesisUtterance(text);
                window.speechSynthesis.speak(utterance);
            }
            
            showNextStep();
            nextButton.style.display = 'inline';
            nextButton.onclick = showNextStep;
        }
    } catch (error) {
        pathInfo.innerHTML = 'Error';
    }
});
