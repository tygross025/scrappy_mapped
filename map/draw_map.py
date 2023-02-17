import folium
from dataclasses import dataclass
from map.ip_location import get_ip_locations


@dataclass
class Location:
    """Data representation of location to be plotted on map"""
    lat: float
    long: float
    ip_locations: set


def get_locations(jsonl_file_path) -> list:
    """Returns a list of Location elements based on addresses in jsonl file."""
    ip_info = get_ip_locations(jsonl_file_path)
    locations = list()
    for ip_location in ip_info:
        is_new_location = True
        for location in locations:
            if location.lat == ip_location.lat and location.long == ip_location.long:
                location.ip_locations.add(ip_location)
                is_new_location = False
                break
        if is_new_location:
            locations.append(Location(
                lat=ip_location.lat,
                long=ip_location.long,
                ip_locations={ip_location}
            ))
    return locations


def run_draw_map():
    draw_map('/Users/tygross/PycharmProjects/scrappy_mapped/exported_results.jsonl')


def add_location_circle(location_map, location):
    """Adds a circle marking a given location onto the given map"""
    title = ', '.join([i.domain for i in location.ip_locations])
    html = folium.Html(
        """
        <!DOCTYPE html>
        <html>
        <head>
          <h3>{title}</h3>
        </head>
        </html> 
        """.format(
            title=title),
        script=True
    )
    # for every additional ip in a location make radius larger
    r = 10 * (len(location.ip_locations) * 200)
    folium.Circle(
        radius=r,
        location=(location.lat, location.long),
        popup=folium.Popup(html, max_height=500, max_width=500, lazy=True),
        color='#FF0000',
        fill=True,
    ).add_to(location_map)


def draw_map(jsonl_file_path):
    """Creates map and adds all locations in file to map."""
    location_map = folium.Map()
    locations = get_locations(jsonl_file_path)

    for location in locations:
        add_location_circle(location_map, location)

    location_map.save('map.html')
