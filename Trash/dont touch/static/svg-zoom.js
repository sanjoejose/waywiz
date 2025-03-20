// SVG Zoom and Pan Functionality
function initSvgZoom() {
    const svgContainer = document.getElementById('svgContainer');
    const svg = svgContainer.querySelector('svg');
    
    if (!svg) return; // Exit if SVG isn't found
    
    let scale = 1;
    const maxScale = 5;
    const minScale = 0.5;
    let panning = false;
    let startPoint = { x: 0, y: 0 };
    let endPoint = { x: 0, y: 0 };
    
    // Create zoom controls if they don't exist
    if (!document.querySelector('.zoom-controls')) {
        const zoomControls = document.createElement('div');
        zoomControls.className = 'zoom-controls';
        zoomControls.innerHTML = `
            <button id="zoomIn" aria-label="Zoom In">+</button>
            <button id="zoomOut" aria-label="Zoom Out">-</button>
            <button id="resetZoom" aria-label="Reset Zoom">Reset</button>
        `;
        zoomControls.style.position = 'absolute';
        zoomControls.style.top = '70px'; // Below sticky header
        zoomControls.style.right = '10px';
        zoomControls.style.zIndex = '200';
        zoomControls.style.backgroundColor = '#1F293A';
        zoomControls.style.padding = '5px';
        zoomControls.style.borderRadius = '5px';
        svgContainer.appendChild(zoomControls);
        
        // Add event listeners for zoom controls
        document.getElementById('zoomIn').addEventListener('click', function() {
            if (scale < maxScale) {
                scale += 0.2;
                applyTransform();
            }
        });
        
        document.getElementById('zoomOut').addEventListener('click', function() {
            if (scale > minScale) {
                scale -= 0.2;
                applyTransform();
            }
        });
        
        document.getElementById('resetZoom').addEventListener('click', function() {
            scale = 1;
            svg.style.transform = `scale(${scale})`;
            svgContainer.scrollLeft = 0;
            svgContainer.scrollTop = 0;
        });
    }
    
    // Mouse wheel zoom
    svgContainer.addEventListener('wheel', function(e) {
        e.preventDefault();
        
        // Get mouse position relative to container
        const rect = svgContainer.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;
        
        // Calculate scroll position as percentage
        const scrollXPercent = (svgContainer.scrollLeft + mouseX) / (svg.getBoundingClientRect().width * scale);
        const scrollYPercent = (svgContainer.scrollTop + mouseY) / (svg.getBoundingClientRect().height * scale);
        
        // Adjust scale based on wheel direction
        if (e.deltaY < 0 && scale < maxScale) {
            // Zoom in
            scale += 0.2;
        } else if (e.deltaY > 0 && scale > minScale) {
            // Zoom out
            scale -= 0.2;
        }
        
        // Apply transform
        applyTransform();
        
        // Adjust scroll to keep point under mouse
        const newWidth = svg.getBoundingClientRect().width * scale;
        const newHeight = svg.getBoundingClientRect().height * scale;
        svgContainer.scrollLeft = (newWidth * scrollXPercent) - mouseX;
        svgContainer.scrollTop = (newHeight * scrollYPercent) - mouseY;
    });
    
    // Apply transform with the current scale
    function applyTransform() {
        svg.style.transform = `scale(${scale})`;
        svg.style.transformOrigin = 'top left';
    }
    
    // Enable panning with mouse drag
    svgContainer.addEventListener('mousedown', function(e) {
        if (e.button === 0) { // Left mouse button
            panning = true;
            startPoint = { x: e.clientX, y: e.clientY };
            svgContainer.style.cursor = 'grabbing';
        }
    });
    
    document.addEventListener('mousemove', function(e) {
        if (panning) {
            endPoint = { x: e.clientX, y: e.clientY };
            const dx = endPoint.x - startPoint.x;
            const dy = endPoint.y - startPoint.y;
            
            svgContainer.scrollLeft -= dx;
            svgContainer.scrollTop -= dy;
            
            startPoint = { x: e.clientX, y: e.clientY };
        }
    });
    
    document.addEventListener('mouseup', function() {
        panning = false;
        svgContainer.style.cursor = 'grab';
    });
    
    // Touch events for mobile pinch zoom
    let initialPinchDistance = 0;
    
    svgContainer.addEventListener('touchstart', function(e) {
        if (e.touches.length === 2) {
            initialPinchDistance = getPinchDistance(e);
        } else if (e.touches.length === 1) {
            panning = true;
            startPoint = { x: e.touches[0].clientX, y: e.touches[0].clientY };
        }
    }, { passive: false });
    
    svgContainer.addEventListener('touchmove', function(e) {
        if (e.touches.length === 2) {
            e.preventDefault(); // Prevent default scrolling
            
            const currentDistance = getPinchDistance(e);
            const pinchRatio = currentDistance / initialPinchDistance;
            
            let newScale = scale * pinchRatio;
            
            // Constrain scale within limits
            if (newScale > maxScale) newScale = maxScale;
            if (newScale < minScale) newScale = minScale;
            
            scale = newScale;
            initialPinchDistance = currentDistance;
            
            applyTransform();
        } else if (e.touches.length === 1 && panning) {
            endPoint = { x: e.touches[0].clientX, y: e.touches[0].clientY };
            const dx = endPoint.x - startPoint.x;
            const dy = endPoint.y - startPoint.y;
            
            svgContainer.scrollLeft -= dx;
            svgContainer.scrollTop -= dy;
            
            startPoint = { x: e.touches[0].clientX, y: e.touches[0].clientY };
        }
    }, { passive: false });
    
    svgContainer.addEventListener('touchend', function() {
        panning = false;
    }, { passive: true });
    
    function getPinchDistance(e) {
        return Math.hypot(
            e.touches[0].clientX - e.touches[1].clientX,
            e.touches[0].clientY - e.touches[1].clientY
        );
    }
    
    // Initialize cursor style
    svgContainer.style.cursor = 'grab';
}

// Call this function after the SVG is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Check if SVG already exists
    const svg = document.querySelector('#svgContainer svg');
    if (svg) {
        initSvgZoom();
    }
});

// Export function for use in other scripts
window.initSvgZoom = initSvgZoom;