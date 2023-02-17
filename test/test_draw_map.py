from map.draw_map import *
from map.ip_location import IPLocation
from unittest.mock import patch


def setup_mock_ip_locations() -> set:
    """Creates a set of mock ip locations to be used in testing."""
    return {
        IPLocation(
            domain='website2',
            address='2.2.2.2',
            links_to=['3.3.3.3'],
            lat=50.0,
            long=50.0
        ),
        IPLocation(
            domain='website3',
            address='3.3.3.3',
            links_to=['2.2.2.2'],
            lat=50.0,
            long=50.0
        ),
        IPLocation(
            domain='website1',
            address='0.0.0.0',
            links_to=['1.1.1.1', '3.3.3.3'],
            lat=0.0,
            long=0.0
        ),
    }


def test_get_locations():
    """Test that IPLocations are grouped into locations based on physical locations"""
    mock_locations = setup_mock_ip_locations()
    expected_results = [
        Location(
            lat=0.0,
            long=0.0,
            ip_locations={mock_locations.pop()}
        ),
        Location(
            lat=50.0,
            long=50.0,
            ip_locations=mock_locations
        )
    ]

    with patch('map.draw_map.get_ip_locations') as mock_get_ip_locations:
        mock_get_ip_locations.return_value = setup_mock_ip_locations()
        locations = get_locations('file')
    assert locations == expected_results
