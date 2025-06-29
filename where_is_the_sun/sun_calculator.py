"""
Sun position calculator for flights.
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from math import cos, sin, radians, degrees, asin, acos, pi, atan2

from pydantic import BaseModel

from .airports import Airport

logger = logging.getLogger(__name__)


class SunPosition(BaseModel):
    """Sun position at specific time."""
    azimuth: float  # Degrees from north
    elevation: float  # Degrees above horizon
    time: datetime


class FlightSunResult(BaseModel):
    """Result of sun position calculation for flight."""
    departure_airport: str
    arrival_airport: str
    departure_time: datetime
    flight_duration_minutes: int
    sun_positions: List[SunPosition]
    recommended_seat_side: str  # "left" or "right"
    sun_exposure_percentage: float


class SunCalculator:
    """Calculate sun position during flights."""
    
    def __init__(self):
        """Initialize sun calculator."""
        self.earth_radius_km = 6371.0
        self.avg_flight_speed_kmh = 800.0  # Average commercial flight speed
    
    def calculate_flight_sun_position(
        self,
        departure_airport: Airport,
        arrival_airport: Airport,
        departure_time: datetime
    ) -> FlightSunResult:
        """Calculate sun position throughout the flight."""
        logger.info(f"Calculating sun position for flight {departure_airport.code} -> {arrival_airport.code}")
        
        # Calculate flight duration
        distance = self._calculate_distance(departure_airport, arrival_airport)
        flight_duration_hours = distance / self.avg_flight_speed_kmh
        flight_duration_minutes = int(flight_duration_hours * 60)
        
        # Calculate sun positions throughout flight
        sun_positions = []
        time_step_minutes = 15  # Check every 15 minutes
        
        for i in range(0, flight_duration_minutes + 1, time_step_minutes):
            current_time = departure_time + timedelta(minutes=i)
            current_position = self._interpolate_position(
                departure_airport, arrival_airport, i / flight_duration_minutes
            )
            
            sun_azimuth, sun_elevation = self._calculate_sun_position(
                current_position, current_time
            )
            
            sun_positions.append(SunPosition(
                azimuth=sun_azimuth,
                elevation=sun_elevation,
                time=current_time
            ))
        
        # Determine recommended seat side
        recommended_side, exposure_percentage = self._determine_best_seat_side(
            sun_positions, departure_airport, arrival_airport
        )
        
        return FlightSunResult(
            departure_airport=departure_airport.code,
            arrival_airport=arrival_airport.code,
            departure_time=departure_time,
            flight_duration_minutes=flight_duration_minutes,
            sun_positions=sun_positions,
            recommended_seat_side=recommended_side,
            sun_exposure_percentage=exposure_percentage
        )
    
    def _calculate_distance(self, airport1: Airport, airport2: Airport) -> float:
        """Calculate distance between two airports using Haversine formula."""
        lat1, lon1 = radians(airport1.latitude), radians(airport1.longitude)
        lat2, lon2 = radians(airport2.latitude), radians(airport2.longitude)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(min(1, a**0.5))
        
        return self.earth_radius_km * c
    
    def _interpolate_position(
        self,
        departure: Airport,
        arrival: Airport,
        progress: float
    ) -> Dict[str, float]:
        """Interpolate position along flight path."""
        lat1, lon1 = departure.latitude, departure.longitude
        lat2, lon2 = arrival.latitude, arrival.longitude
        
        # Simple linear interpolation (for short distances this is adequate)
        lat = lat1 + (lat2 - lat1) * progress
        lon = lon1 + (lon2 - lon1) * progress
        
        return {"latitude": lat, "longitude": lon}
    
    def _calculate_sun_position(
        self,
        position: Dict[str, float],
        time: datetime
    ) -> tuple[float, float]:
        """Calculate sun azimuth and elevation at given position and time."""
        # Simplified sun position calculation
        # In a real implementation, you would use astronomical algorithms
        
        # Convert to UTC if needed
        if time.tzinfo is None:
            time = time.replace(tzinfo=None)
        
        # Day of year
        day_of_year = time.timetuple().tm_yday
        
        # Hour angle (simplified)
        hour = time.hour + time.minute / 60.0
        hour_angle = (hour - 12) * 15  # 15 degrees per hour
        
        # Declination (simplified)
        declination = 23.45 * sin(radians(360/365 * (day_of_year - 80)))
        
        # Calculate elevation
        lat_rad = radians(position["latitude"])
        decl_rad = radians(declination)
        hour_rad = radians(hour_angle)
        
        sin_elevation = (
            sin(lat_rad) * sin(decl_rad) +
            cos(lat_rad) * cos(decl_rad) * cos(hour_rad)
        )
        elevation = degrees(asin(max(-1, min(1, sin_elevation))))
        
        # Calculate azimuth
        cos_azimuth = (
            (sin(decl_rad) - sin_elevation * sin(lat_rad)) /
            (cos(elevation) * cos(lat_rad))
        )
        azimuth = degrees(acos(max(-1, min(1, cos_azimuth))))
        
        # Adjust azimuth based on hour angle
        if hour_angle > 0:
            azimuth = 360 - azimuth
        
        return azimuth, elevation
    
    def _determine_best_seat_side(
        self,
        sun_positions: List[SunPosition],
        departure: Airport,
        arrival: Airport
    ) -> tuple[str, float]:
        """Determine which side of the plane has less sun exposure."""
        # Calculate flight heading
        heading = self._calculate_heading(departure, arrival)
        
        # Analyze sun positions relative to flight direction
        left_exposure = 0
        right_exposure = 0
        total_positions = len(sun_positions)
        
        for sun_pos in sun_positions:
            if sun_pos.elevation < 0:  # Sun below horizon
                continue
                
            # Calculate relative sun position to flight direction
            relative_azimuth = (sun_pos.azimuth - heading) % 360
            
            # Determine which side of the plane the sun is on
            if 90 <= relative_azimuth <= 270:
                left_exposure += 1
            else:
                right_exposure += 1
        
        # Calculate exposure percentages
        left_percentage = (left_exposure / total_positions) * 100
        right_percentage = (right_exposure / total_positions) * 100
        
        # Recommend the side with less exposure
        if left_percentage < right_percentage:
            return "left", left_percentage
        else:
            return "right", right_percentage
    
    def _calculate_heading(self, departure: Airport, arrival: Airport) -> float:
        """Calculate heading from departure to arrival airport."""
        lat1, lon1 = radians(departure.latitude), radians(departure.longitude)
        lat2, lon2 = radians(arrival.latitude), radians(arrival.longitude)
        
        dlon = lon2 - lon1
        
        y = sin(dlon) * cos(lat2)
        x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)
        
        heading = degrees(atan2(y, x))
        return (heading + 360) % 360 