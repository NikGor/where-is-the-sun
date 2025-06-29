"""
European airports data for sun position calculations.
"""
from typing import Dict
from pydantic import BaseModel


class Airport(BaseModel):
    """Airport information model."""
    code: str
    name: str
    city: str
    country: str
    latitude: float
    longitude: float


def get_airports() -> Dict[str, Airport]:
    """Get dictionary of European airports."""
    airports_data = [
        Airport(code="LHR", name="Heathrow", city="London", country="UK", latitude=51.4700, longitude=-0.4543),
        Airport(code="CDG", name="Charles de Gaulle", city="Paris", country="France", latitude=49.0097, longitude=2.5479),
        Airport(code="FRA", name="Frankfurt", city="Frankfurt", country="Germany", latitude=50.0379, longitude=8.5622),
        Airport(code="AMS", name="Schiphol", city="Amsterdam", country="Netherlands", latitude=52.3105, longitude=4.7683),
        Airport(code="MAD", name="Barajas", city="Madrid", country="Spain", latitude=40.4983, longitude=-3.5676),
        Airport(code="BCN", name="El Prat", city="Barcelona", country="Spain", latitude=41.2974, longitude=2.0833),
        Airport(code="FCO", name="Fiumicino", city="Rome", country="Italy", latitude=41.8045, longitude=12.2508),
        Airport(code="MXP", name="Malpensa", city="Milan", country="Italy", latitude=45.6306, longitude=8.7281),
        Airport(code="ZRH", name="Zurich", city="Zurich", country="Switzerland", latitude=47.4588, longitude=8.5559),
        Airport(code="VIE", name="Schwechat", city="Vienna", country="Austria", latitude=48.1102, longitude=16.5697),
        Airport(code="CPH", name="Kastrup", city="Copenhagen", country="Denmark", latitude=55.6180, longitude=12.6508),
        Airport(code="ARN", name="Arlanda", city="Stockholm", country="Sweden", latitude=59.6498, longitude=17.9238),
        Airport(code="OSL", name="Gardermoen", city="Oslo", country="Norway", latitude=60.1975, longitude=11.1004),
        Airport(code="HEL", name="Helsinki-Vantaa", city="Helsinki", country="Finland", latitude=60.3172, longitude=24.9633),
        Airport(code="WAW", name="Chopin", city="Warsaw", country="Poland", latitude=52.1657, longitude=20.9671),
        Airport(code="PRG", name="Václav Havel", city="Prague", country="Czech Republic", latitude=50.1008, longitude=14.2600),
        Airport(code="BUD", name="Ferenc Liszt", city="Budapest", country="Hungary", latitude=47.4369, longitude=19.2556),
        Airport(code="IST", name="Istanbul", city="Istanbul", country="Turkey", latitude=41.2751, longitude=28.7519),
        Airport(code="ATH", name="Eleftherios Venizelos", city="Athens", country="Greece", latitude=37.9364, longitude=23.9445),
        Airport(code="LIS", name="Portela", city="Lisbon", country="Portugal", latitude=38.7813, longitude=-9.1359),
        Airport(code="OPO", name="Francisco Sá Carneiro", city="Porto", country="Portugal", latitude=41.2481, longitude=-8.6814),
        Airport(code="DUB", name="Dublin", city="Dublin", country="Ireland", latitude=53.4213, longitude=-6.2701),
        Airport(code="BRU", name="Brussels", city="Brussels", country="Belgium", latitude=50.9014, longitude=4.4844),
        Airport(code="GVA", name="Geneva", city="Geneva", country="Switzerland", latitude=46.2381, longitude=6.1089),
        Airport(code="LUX", name="Luxembourg", city="Luxembourg", country="Luxembourg", latitude=49.6266, longitude=6.2115),
        Airport(code="KEF", name="Keflavík", city="Reykjavik", country="Iceland", latitude=63.9850, longitude=-22.6056),
        Airport(code="RIX", name="Riga", city="Riga", country="Latvia", latitude=56.9236, longitude=23.9711),
        Airport(code="TLL", name="Tallinn", city="Tallinn", country="Estonia", latitude=59.4133, longitude=24.8328),
        Airport(code="VNO", name="Vilnius", city="Vilnius", country="Lithuania", latitude=54.6341, longitude=25.2858),
        Airport(code="SOF", name="Sofia", city="Sofia", country="Bulgaria", latitude=42.6954, longitude=23.4062),
        Airport(code="OTP", name="Henri Coandă", city="Bucharest", country="Romania", latitude=44.5711, longitude=26.0850),
        Airport(code="BEG", name="Nikola Tesla", city="Belgrade", country="Serbia", latitude=44.8184, longitude=20.3091),
        Airport(code="ZAG", name="Zagreb", city="Zagreb", country="Croatia", latitude=45.7429, longitude=16.0688),
        Airport(code="LJU", name="Jože Pučnik", city="Ljubljana", country="Slovenia", latitude=46.2237, longitude=14.4576),
        Airport(code="SKP", name="Skopje", city="Skopje", country="North Macedonia", latitude=41.9614, longitude=21.6214),
        Airport(code="TIA", name="Tirana", city="Tirana", country="Albania", latitude=41.4147, longitude=19.7206),
        Airport(code="KBP", name="Boryspil", city="Kiev", country="Ukraine", latitude=50.3450, longitude=30.8947),
        Airport(code="MSQ", name="Minsk", city="Minsk", country="Belarus", latitude=53.8825, longitude=28.0307),
        Airport(code="LED", name="Pulkovo", city="Saint Petersburg", country="Russia", latitude=59.8003, longitude=30.2625),
        Airport(code="SVO", name="Sheremetyevo", city="Moscow", country="Russia", latitude=55.9726, longitude=37.4146),
    ]
    
    return {airport.code: airport for airport in airports_data} 