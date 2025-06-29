/**
 * Main application JavaScript for Where is the Sun
 */

document.addEventListener('DOMContentLoaded', function() {
    const flightForm = document.getElementById('flightForm');
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
        welcomeMessage.classList.add('d-none');
        resultsContainer.classList.add('d-none');
        
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
        }
    });
    
    function showError(message) {
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
        const recommendationSide = document.getElementById('recommendationSide');
        const sideText = result.recommended_seat_side === 'left' ? 'left side' : 'right side';
        recommendationText.textContent = `Choose a seat on the ${sideText} of the plane to minimize sun exposure.`;
        recommendationSide.textContent = `Best Side: ${sideText}`;
        
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
        
        // Манометр sun exposure
        const exposureValue = document.getElementById('exposureValue');
        const exposureArrow = document.getElementById('exposureArrow');
        let percent = result.sun_exposure_percentage;
        if (typeof percent !== 'number' || isNaN(percent)) percent = 0;
        if (exposureValue) {
            exposureValue.textContent = percent.toFixed(1) + '%';
        }
        // Поворот стрелки: 0% = -120deg, 100% = +120deg (240 градусов), центр (100,100)
        const angle = -120 + (percent * 2.4);
        if (exposureArrow) exposureArrow.setAttribute('transform', `rotate(${angle} 100 100)`);
        
        // Update airplane visualization
        updateAirplaneVisualization(result);
    }
    
    function updateAirplaneVisualization(result) {
        // Проверка: если солнце всё время ниже горизонта
        const allNight = Array.isArray(result.sun_positions) && result.sun_positions.every(pos => pos.elevation < 0);
        const leftOverlay = document.getElementById('planeLeftOverlay');
        const rightOverlay = document.getElementById('planeRightOverlay');
        // Удаляем sunIndicator и shadowIndicator полностью
        leftOverlay.style.background = 'none';
        rightOverlay.style.background = 'none';
        // sunIndicator.classList.add('d-none');
        // shadowIndicator.classList.add('d-none');
        // Меняем текст рекомендации, если ночь
        if (allNight) {
            document.getElementById('recommendationText').textContent = 'During the entire flight it will be night — the sun will not shine into the windows.';
            return;
        }
        // Не показываем sunIndicator и shadowIndicator вообще
        // Остальной код не трогаем
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
    
    // Toggle switches logic
    const instrumentGrid = document.querySelector('.instrument-grid');

    // Авиационные электронные часы
    function updateAviaclock() {
        const clock = document.getElementById('aviaclockTime');
        if (clock) {
            const now = new Date();
            const h = String(now.getHours()).padStart(2, '0');
            const m = String(now.getMinutes()).padStart(2, '0');
            const s = String(now.getSeconds()).padStart(2, '0');
            clock.textContent = `${h}:${m}:${s}`;
        }
    }
    setInterval(updateAviaclock, 1000);
    updateAviaclock();

    document.querySelectorAll('.tumbler-img').forEach(function(img) {
        img.addEventListener('click', function() {
            // Basic image toggle for all tumblers
            if (img.dataset.toggled === 'true') {
                img.src = '/static/tumbler.png';
                img.dataset.toggled = 'false';
            } else {
                img.src = '/static/tumbler_down.png';
                img.dataset.toggled = 'true';
            }

            // Specific action for the light switch
            if (img.dataset.toggleId === '1') {
                if (instrumentGrid) {
                    instrumentGrid.classList.toggle('backlight-on');
                }
            }
        });
    });
}); 