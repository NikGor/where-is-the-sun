"""
Web application for sun position calculation on flights.
"""
import logging
from datetime import datetime
from typing import Dict, List, Optional

from flask import Flask, render_template, request, jsonify
from pydantic import BaseModel

from .airports import Airport, get_airports
from .sun_calculator import SunCalculator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
sun_calculator = SunCalculator()


class FlightRequest(BaseModel):
    """Request model for flight calculation."""
    departure_airport: str
    arrival_airport: str
    departure_time: str


@app.route('/')
def index():
    """Main page with flight form."""
    logger.info("Rendering main page")
    airports = get_airports()
    return render_template('index.html', airports=airports)


@app.route('/api/calculate', methods=['POST'])
def calculate_sun_position():
    """Calculate sun position for the flight."""
    try:
        data = request.get_json()
        flight_request = FlightRequest(**data)
        
        logger.info(f"Calculating sun position for flight: {flight_request.departure_airport} -> {flight_request.arrival_airport}")
        
        # Parse departure time
        departure_time = datetime.fromisoformat(flight_request.departure_time.replace('Z', '+00:00'))
        
        # Get airports
        airports = get_airports()
        departure_airport = airports.get(flight_request.departure_airport)
        arrival_airport = airports.get(flight_request.arrival_airport)
        
        if not departure_airport or not arrival_airport:
            return jsonify({'error': 'Airport not found'}), 400
        
        # Calculate sun position
        result = sun_calculator.calculate_flight_sun_position(
            departure_airport=departure_airport,
            arrival_airport=arrival_airport,
            departure_time=departure_time
        )
        
        logger.info(f"Calculation completed successfully")
        return jsonify(result.model_dump())
        
    except Exception as e:
        logger.error(f"Error calculating sun position: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/airports')
def get_airports_api():
    """Get list of available airports."""
    logger.info("Returning airports list")
    airports = get_airports()
    return jsonify(list(airports.values()))


def main():
    """Run the Flask application."""
    logger.info("Starting Where is the Sun web application")
    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main() 