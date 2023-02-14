from unittest.mock import patch
import pytest

from map.ip_location import *


def test_build_ip_locations():
    expected_output = {
        IPLocation(
            address='1.2.3.4',
            domain='website.com',
            links_to=['1.1.1.1', '2.2.2.2'],
            lat=0.0,
            long=0.0
        ),
        IPLocation(
            address='1.1.1.1',
            domain='website2.com',
            links_to=['0.0.0.0'],
            lat=0.0,
            long=0.0
        )
    }
    file = './test/test_results.jsonl'
    parsed_file = parse_file_data(file)
    with patch('map.ip_location.get_ipinfo') as mock_get_ip_info:
        mock_handler = MockHandler(True)
        mock_get_ip_info.return_value = mock_handler.getBatchDetails(parsed_file.keys())
        locations = get_ip_locations(file)
    assert locations == expected_output


def test_parse_file_data():
    # expected_output based on test_results.jsonl file
    expected_output = {
        '1.2.3.4': {'domain': 'website.com', 'linked_to': ["1.1.1.1", "2.2.2.2"]},
        '1.1.1.1': {'domain': 'website2.com', 'linked_to': ["0.0.0.0"]}
    }
    file = './test/test_results.jsonl'
    parsed_file = parse_file_data(file)
    assert parsed_file == expected_output


def test_getipinfo_invalid_token():
    """Test that InvalidResponseError is thrown when auth token is invalid"""
    with patch('ipinfo.getHandler') as mock_getHandler, patch('os.environ') as mock_token:
        mock_getHandler.return_value = MockHandler(valid_auth=False)
        mock_token.return_value = 'abc'
        with pytest.raises(InvalidResponseError):
            get_ipinfo({'100.2.3.1', '10.11.12.13'})


def test_getipinfo_valid_token():
    """Test that MockHandler response is returned when auth token is valid"""
    with patch('ipinfo.getHandler') as mock_getHandler, patch('os.environ') as mock_token:
        mock_handler = MockHandler(valid_auth=True)
        mock_token.return_value = 'abc'
        expected_results = mock_handler.getBatchDetails({'1.1.1.1'})
        mock_getHandler.return_value = mock_handler
        assert get_ipinfo({'1.1.1.1'}) == expected_results


class MockHandler:
    """A class to mock the output of ipinfo.Handler class"""

    def __init__(self, valid_auth=True):
        self.valid_auth = valid_auth

    def getBatchDetails(self, ips):
        """method being called in real Handler that is being faked"""
        if self.valid_auth:
            return self._get_batch_details_valid_auth(ips)
        else:
            return self._get_batch_details_invalid_auth(ips)

    def _get_batch_details_valid_auth(self, ips):
        """Example of ipinfo response when auth token is valid."""
        batch_details = dict()
        for ip in ips:
            batch_details[ip] = {'ip': f'{ip}', 'city': 'City', 'region': 'Region', 'country': 'Country', 'loc': '0.0',
                                 'org': 'Org', 'postal': '00000', 'timezone': 'Time', 'country_name': 'Country',
                                 'isEU': False, 'country_flag': {'emoji': 'Emoji', 'unicode': 'Unicode'},
                                 'country_currency': {'code': 'Money', 'symbol': '!'},
                                 'continent': {'code': 'Code', 'name': 'Name'},
                                 'latitude': '00.0000', 'longitude': '00.0000'
                                 }
        return batch_details

    def _get_batch_details_invalid_auth(self, ips):
        """Example of ipinfo response when auth token is invalid."""
        return {'1.1.1.1': {'status': 403, 'error': {'title': 'Unknown token', 'message': "Please.... for help"},
                            'country_name': None, 'isEU': False, 'country_flag': None, 'country_currency': None,
                            'continent': None, 'latitude': None, 'longitude': None}}
