import json
import os
from dataclasses import dataclass, field
import ipinfo


@dataclass(frozen=True, eq=True)
class IPLocation:
    domain: str
    address: str
    links_to: list = field(hash=False)
    lat: float
    long: float


def get_ip_locations(file) -> set:
    """Returns set of IPLocation objects based on jsonl file"""
    file_data = parse_file_data(file)
    ip_info = get_ipinfo(file_data.keys())
    ip_locations = set()
    for address in file_data:
        ip_location = IPLocation(
            address=address,
            domain=file_data[address]['domain'],
            links_to=file_data[address]['linked_to'],
            lat=float(ip_info[address]['latitude']),
            long=float(ip_info[address]['longitude'])
        )
        ip_locations.add(ip_location)
    return ip_locations


def get_ipinfo(ips) -> dict:
    """Sends batch request to ipinfo api"""
    access_token = os.environ['IPINFO_ACCESS_TOKEN']
    handler = ipinfo.getHandler(access_token)
    details = handler.getBatchDetails(ips)
    for response in details:
        if 'status' in details[response]:
            raise InvalidResponseError(f"Received error from response: {details[response]['error']['title']}")
    return details


def parse_file_data(file) -> dict:
    """Parses ip jsonl file into a dict:
    Example output:
    {
        '1.2.3.4': {'domain': 'website.com', 'linked_to': ["1.1.1.1", "2.2.2.2"]},
        '1.1.1.1': {'domain': 'website2.com', 'linked_to': ["0.0.0.0"]}
    }
    """
    with open(file, 'r') as f:
        json_list = list(f)
    file_data = dict()
    for json_str in json_list:
        data = json.loads(json_str)
        file_data[data['address']] = {'domain': data['domain'], 'linked_to': data['linked_to']}
    return file_data


class InvalidResponseError(Exception):
    """Error indicating that ipinfo response is not as expected"""
    pass
