// Main application JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const scanButton = document.getElementById('scanButton');
    const qrScreen = document.getElementById('qrScreen');
    const endNodeScreen = document.getElementById('endNodeScreen');
    const camera = document.getElementById('camera');
    const scanMessage = document.getElementById('scanMessage');
    const pathForm = document.getElementById('pathForm');
    const pathInfo = document.getElementById('pathInfo');
    const currentStep = document.getElementById('currentStep');
    const nextButton = document.getElementById('nextButton');
    const svgContainer = document.getElementById('svgContainer');
    const searchBar = document.getElementById('searchBar');
    const dropdownMenu = document.getElementById('dropdownMenu');
    
    let startNode = null;
    
    // Initialize UI
    initializeUI();
    
    function initializeUI() {
        // Add event listeners
        scanButton.addEventListener('click', startCamera);
        searchBar.addEventListener('focus', showDropdown);
        document.addEventListener('click', hideDropdownOnClickOutside);
        pathForm.addEventListener('submit', findPath);
        
        // Add loading animation
        scanButton.innerHTML = `
            <span>Scan QR Code</span>
            <span class="scan-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M0 .5A.5.5 0 0 1 .5 0h3a.5.5 0 0 1 0 1H1v2.5a.5.5 0 0 1-1 0v-3Zm12 0a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 .5.5v3a.5.5 0 0 1-1 0V1h-2.5a.5.5 0 0 1-.5-.5ZM.5 12a.5.5 0 0 1 .5.5V15h2.5a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5v-3a.5.5 0 0 1 .5-.5Zm15 0a.5.5 0 0 1 .5.5v3a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1 0-1H15v-2.5a.5.5 0 0 1 .5-.5ZM4 4h1v1H4V4Zm2 0h1v1H6V4Zm-2 2h1v1H4V6Zm2 0h1v1H6V6Zm6-2h1v1h-1V4Zm2 0h1v1h-1V4Zm-2 2h1v1h-1V6Zm2 0h1v1h-1V6Zm1-5a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V3Zm-1 13H2V4h12v12Z"/>
                </svg>
            </span>
        `;
    }
    
    // Camera and QR scanning functions
    function startCamera() {
        scanButton.disabled = true;
        scanButton.innerHTML = 'Accessing camera...';
        
        navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
            .then(stream => {
                camera.srcObject = stream;
                camera.style.display = 'block';
                scanMessage.textContent = 'Scanning for QR code...';
                scanButton.innerHTML = 'Scanning...';
                
                // Add a pulsing animation to the message
                scanMessage.classList.add('pulse-animation');
                
                requestAnimationFrame(scanQR);
            })
            .catch(err => {
                scanButton.disabled = false;
                scanButton.innerHTML = 'Scan QR Code';
                scanMessage.textContent = `Camera error: ${err.message}. Please try again.`;
                scanMessage.style.color = '#FF6B6B';
            });
    }
    
    function stopCamera() {
        const stream = camera.srcObject;
        if (stream) {
            const tracks = stream.getTracks();
            tracks.forEach(track => track.stop());
        }
        camera.style.display = 'none';
        scanMessage.classList.remove('pulse-animation');
    }
    
    function scanQR() {
        if (camera.readyState === camera.HAVE_ENOUGH_DATA) {
            const canvas = document.createElement('canvas');
            canvas.width = camera.videoWidth;
            canvas.height = camera.videoHeight;
            const context = canvas.getContext('2d');
            context.drawImage(camera, 0, 0, canvas.width, canvas.height);
            
            const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
            const code = jsQR(imageData.data, imageData.width, imageData.height);
            
            if (code) {
                startNode = parseInt(code.data, 10);
                if (!isNaN(startNode)) {
                    // Success animation
                    scanMessage.textContent = 'QR Code detected!';
                    scanMessage.style.color = '#A4D77C';
                    
                    // Transition to next screen with animation
                    setTimeout(() => {
                        stopCamera();
                        qrScreen.style.opacity = '0';
                        setTimeout(() => {
                            qrScreen.style.display = 'none';
                            endNodeScreen.style.display = 'block';
                            setTimeout(() => {
                                endNodeScreen.style.opacity = '1';
                                populateDropdown();
                            }, 50);
                        }, 300);
                    }, 800);
                } else {
                    scanMessage.textContent = 'Invalid QR code data. Please try again.';
                    scanMessage.style.color = '#FF6B6B';
                    scanButton.disabled = false;
                    scanButton.innerHTML = 'Scan QR Code';
                }
                return;
            }
        }
        requestAnimationFrame(scanQR);
    }
    
    // Dropdown functions
    async function populateDropdown() {
        try {
            dropdownMenu.innerHTML = '<div class="dropdown-item loading">Loading locations...</div>';
            
            const response = await fetch('/get-staff-locations');
            const data = await response.json();
            
            if (data.error) {
                dropdownMenu.innerHTML = `<div class="dropdown-item error">Error: ${data.error}</div>`;
                return;
            }
            
            dropdownMenu.innerHTML = ''; // Reset dropdown menu
            
            if (data.staff.length === 0) {
                dropdownMenu.innerHTML = '<div class="dropdown-item">No locations found</div>';
                return;
            }
            
            data.staff.forEach(staff => {
                const div = document.createElement('div');
                div.className = 'dropdown-item';
                div.textContent = staff.name;
                div.setAttribute('data-location', staff.location);
                div.onclick = function() {
                    selectEndNode(staff.name, staff.location);
                };
                dropdownMenu.appendChild(div);
            });
        } catch (error) {
            dropdownMenu.innerHTML = '<div class="dropdown-item error">Failed to load locations</div>';
            console.error('Error fetching staff locations:', error);
        }
    }
    
    function selectEndNode(name, location) {
        searchBar.value = name;
        document.getElementById('selectedEndNode').value = location;
        dropdownMenu.style.display = 'none';
        
        // Highlight the search bar to show selection is complete
        searchBar.classList.add('selection-complete');
        setTimeout(() => {
            searchBar.classList.remove('selection-complete');
        }, 1000);
    }
    
    function filterDropdown() {
        const query = searchBar.value.toLowerCase();
        const items = dropdownMenu.getElementsByClassName('dropdown-item');
        let hasResults = false;
        
        for (let item of items) {
            if (item.classList.contains('loading') || item.classList.contains('error')) continue;
            
            if (item.textContent.toLowerCase().includes(query)) {
                item.style.display = '';
                hasResults = true;
            } else {
                item.style.display = 'none';
            }
        }
        
        // Show "no results" message if needed
        let noResultsElement = dropdownMenu.querySelector('.no-results');
        if (!hasResults && query.length > 0) {
            if (!noResultsElement) {
                noResultsElement = document.createElement('div');
                noResultsElement.className = 'dropdown-item no-results';
                noResultsElement.textContent = 'No matching locations';
                dropdownMenu.appendChild(noResultsElement);
            }
            noResultsElement.style.display = '';
        } else if (noResultsElement) {
            noResultsElement.style.display = 'none';
        }
    }
    
    function showDropdown() {
        dropdownMenu.style.display = 'block';
    }
    
    function hideDropdownOnClickOutside(e) {
        if (!e.target.closest('.dropdown-container')) {
            dropdownMenu.style.display = 'none';
        }
    }
    
    // Path finding and navigation
    async function findPath(event) {
        event.preventDefault();
        
        const start = startNode;
        const end = parseInt(document.getElementById('selectedEndNode').value, 10);
        
        if (isNaN(start) || isNaN(end)) {
            pathInfo.innerHTML = '<span style="color: #FF6B6B;">Error: Invalid start or end location</span>';
            return;
        }
        
        // Show loading animation
        svgContainer.style.display = 'flex';
        svgContainer.innerHTML += '<div class="loading-spinner"></div>';
        pathInfo.innerHTML = '<span class="loading-text">Calculating path...</span>';
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
            
            // Remove loading spinner
            const spinner = svgContainer.querySelector('.loading-spinner');
            if (spinner) spinner.remove();
            
            if (data.error) {
                pathInfo.innerHTML = `<span style="color: #FF6B6B;">Error: ${data.error}</span>`;
                return;
            }
            
            // Format path info with better styling
            pathInfo.innerHTML = `
                <div class="path-summary">
                    <div class="path-detail">
                        <span class="detail-label">Path:</span>
                        <span class="detail-value">${data.path.join(' → ')}</span>
                    </div>
                    <div class="path-detail">
                        <span class="detail-label">Distance:</span>
                        <span class="detail-value">${data.distance} units</span>
                    </div>
                </div>
            `;
            
            // Initialize navigation
            let directions = data.directions;
            let currentStepIndex = 0;
            let floor = Math.floor(data.path[0] / 100);
            
            function showElement(element) {
                if (element) {
                    element.style.display = 'inline';
                    element.classList.add('fade-in');
                }
            }
            
            function hideElement(element) {
                if (element) {
                    element.classList.add('fade-out');
                    setTimeout(() => {
                        element.style.display = 'none';
                        element.classList.remove('fade-out');
                    }, 300);
                }
            }
            
            function showFloor(floor) {
                // Add transition for floor change
                svgContainer.classList.add('floor-transition');
                
                // Hide all floors
                const allFloors = document.querySelectorAll('.floor');
                allFloors.forEach(floorElement => hideElement(floorElement));
                
                // Show the specific floor
                const floorElement = document.getElementById(`f${floor}`);
                showElement(floorElement);
                
                // Remove transition class after animation
                setTimeout(() => {
                    svgContainer.classList.remove('floor-transition');
                }, 500);
            }
            
            function showMap(currentStepIndex) {
                const currentFloor = Math.floor(data.path[currentStepIndex] / 100);
                showFloor(currentFloor);
                
                // Hide all path elements
                const allPaths = document.querySelectorAll('.pa');
                allPaths.forEach(pathElement => hideElement(pathElement));
                
                // Show paths for the current floor
                for (let i = currentStepIndex; i < data.path.length - 1; i++) {
                    if (Math.floor(data.path[i + 1] / 100) === currentFloor) {
                        const pathId = `p${data.path[i]}-${data.path[i + 1]}`;
                        const pathElement = document.getElementById(pathId);
                        showElement(pathElement);
                    }
                }
            }
            
            function showNextStep() {
                if (currentStepIndex < directions.length) {
                    const currentFloor = Math.floor(data.path[currentStepIndex] / 100);
                    
                    // If the floor changes, update the map
                    if (Math.floor(data.path[currentStepIndex] / 100) !== floor) {
                        floor = currentFloor;
                        showMap(currentStepIndex);
                    }
                    
                    const directionText = `Node ${data.path[currentStepIndex + 1]}: ${directions[currentStepIndex]}`;
                    
                    // Animate the step change
                    currentStep.classList.add('step-transition');
                    setTimeout(() => {
                        currentStep.innerHTML = directionText;
                        currentStep.classList.remove('step-transition');
                        speak(directionText);
                    }, 300);
                    
                    currentStepIndex++;
                } else {
                    // Final destination reached animation
                    currentStep.classList.add('destination-reached');
                    currentStep.innerHTML = 'You have reached your destination!';
                    nextButton.style.display = 'none';
                    
                    // Celebration animation
                    const celebration = document.createElement('div');
                    celebration.className = 'celebration';
                    svgContainer.appendChild(celebration);
                    setTimeout(() => celebration.remove(), 3000);
                }
            }
            
            function speak(text) {
                if ('speechSynthesis' in window) {
                    const utterance = new SpeechSynthesisUtterance(text);
                    utterance.rate = 0.9; // Slightly slower for clarity
                    window.speechSynthesis.speak(utterance);
                }
            }
            
            // Initialize the map and navigation
            showMap(0);
            showNextStep();
            nextButton.style.display = 'inline';
            nextButton.onclick = showNextStep;
            
            // Add pulse animation to the next button
            nextButton.classList.add('pulse-button');
            
        } catch (error) {
            pathInfo.innerHTML = '<span style="color: #FF6B6B;">Error: Unable to fetch data from the server</span>';
            console.error('Error fetching path data:', error);
        }
    }
});