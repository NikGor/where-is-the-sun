/**
 * Main application JavaScript for Where is the Sun
 */

document.addEventListener('DOMContentLoaded', function() {
    const flightForm = document.getElementById('flightForm');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const welcomeMessage = document.getElementById('welcomeMessage');
    const resultsContainer = document.getElementById('resultsContainer');
    const airplaneVisualization = document.getElementById('airplaneVisualization');
    const sunIndicator = document.getElementById('sunIndicator');
    const shadowIndicator = document.getElementById('shadowIndicator');
    
    // Form submission handler
    flightForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        if (!flightForm.checkValidity()) {
            flightForm.classList.add('was-validated');
            return;
        }
        
        // Show loading state
        showLoading();
        
        try {
            const formData = {
                departure_airport: document.getElementById('departureAirport').value,
                arrival_airport: document.getElementById('arrivalAirport').value,
                departure_time: document.getElementById('departureTime').value
            };
            
            const response = await fetch('/api/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            displayResults(result);
            
        } catch (error) {
            console.error('Error:', error);
            showError('An error occurred while calculating sun position. Please try again.');
        } finally {
            hideLoading();
        }
    });
    
    function showLoading() {
        loadingSpinner.classList.remove('d-none');
        welcomeMessage.classList.add('d-none');
        resultsContainer.classList.add('d-none');
    }
    
    function hideLoading() {
        loadingSpinner.classList.add('d-none');
    }
    
    function showError(message) {
        hideLoading();
        welcomeMessage.classList.remove('d-none');
        welcomeMessage.innerHTML = `
            <div class="alert alert-danger">
                <h4><i class="fas fa-exclamation-triangle"></i> Error</h4>
                <p>${message}</p>
            </div>
        `;
    }
    
    function displayResults(result) {
        // Hide welcome message and show results
        welcomeMessage.classList.add('d-none');
        resultsContainer.classList.remove('d-none');
        
        // Update recommendation text
        const recommendationText = document.getElementById('recommendationText');
        const sideText = result.recommended_seat_side === 'left' ? 'left side' : 'right side';
        recommendationText.textContent = `Choose a seat on the ${sideText} of the plane to minimize sun exposure.`;
        
        // Update flight details
        const flightDetails = document.getElementById('flightDetails');
        const departureTime = new Date(result.departure_time).toLocaleString();
        const durationHours = Math.floor(result.flight_duration_minutes / 60);
        const durationMinutes = result.flight_duration_minutes % 60;
        
        flightDetails.innerHTML = `
            <strong>Route:</strong> ${result.departure_airport} → ${result.arrival_airport}<br>
            <strong>Departure:</strong> ${departureTime}<br>
            <strong>Duration:</strong> ${durationHours}h ${durationMinutes}m
        `;
        
        // Update sun exposure
        const sunExposure = document.getElementById('sunExposure');
        sunExposure.innerHTML = `
            <strong>Recommended side exposure:</strong> ${result.sun_exposure_percentage.toFixed(1)}%<br>
            <strong>Opposite side exposure:</strong> ${(100 - result.sun_exposure_percentage).toFixed(1)}%
        `;
        
        // Update airplane visualization
        updateAirplaneVisualization(result);
    }
    
    function updateAirplaneVisualization(result) {
        // Проверка: если солнце всё время ниже горизонта
        const allNight = Array.isArray(result.sun_positions) && result.sun_positions.every(pos => pos.elevation < 0);
        const leftOverlay = document.getElementById('planeLeftOverlay');
        const rightOverlay = document.getElementById('planeRightOverlay');
        if (allNight) {
            leftOverlay.style.background = 'none';
            rightOverlay.style.background = 'none';
            sunIndicator.classList.add('d-none');
            shadowIndicator.classList.add('d-none');
            // Меняем текст рекомендации
            document.getElementById('recommendationText').textContent = 'В течение всего полёта будет ночь — солнце не будет светить в окна.';
            return;
        }
        sunIndicator.classList.remove('d-none');
        shadowIndicator.classList.remove('d-none');
        leftOverlay.style.background = 'none';
        rightOverlay.style.background = 'none';
        if (result.recommended_seat_side === 'left') {
            rightOverlay.style.background = 'rgba(255, 215, 0, 0.35)';
            leftOverlay.style.background = 'rgba(70, 130, 180, 0.35)';
            sunIndicator.style.left = 'auto';
            sunIndicator.style.right = '100px';
            shadowIndicator.style.right = 'auto';
            shadowIndicator.style.left = '100px';
        } else {
            leftOverlay.style.background = 'rgba(255, 215, 0, 0.35)';
            rightOverlay.style.background = 'rgba(70, 130, 180, 0.35)';
            sunIndicator.style.right = 'auto';
            sunIndicator.style.left = '100px';
            shadowIndicator.style.left = 'auto';
            shadowIndicator.style.right = '100px';
        }
    }
    
    // Set default departure time to current time + 1 hour
    const now = new Date();
    now.setHours(now.getHours() + 1);
    now.setMinutes(0);
    now.setSeconds(0);
    now.setMilliseconds(0);
    
    const departureTimeInput = document.getElementById('departureTime');
    departureTimeInput.value = now.toISOString().slice(0, 16);
    
    // Add form validation feedback
    const inputs = flightForm.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.checkValidity()) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            } else {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            }
        });
    });
    
    // Prevent selecting same airport for departure and arrival
    const departureSelect = document.getElementById('departureAirport');
    const arrivalSelect = document.getElementById('arrivalAirport');
    
    function updateArrivalOptions() {
        const departureValue = departureSelect.value;
        const arrivalValue = arrivalSelect.value;
        
        Array.from(arrivalSelect.options).forEach(option => {
            if (option.value === departureValue) {
                option.disabled = true;
                if (arrivalValue === departureValue) {
                    arrivalSelect.value = '';
                }
            } else {
                option.disabled = false;
            }
        });
    }
    
    departureSelect.addEventListener('change', updateArrivalOptions);
    arrivalSelect.addEventListener('change', updateArrivalOptions);
    
    // Initialize arrival options
    updateArrivalOptions();
}); 