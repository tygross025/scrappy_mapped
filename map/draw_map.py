import json
import folium
from ip_location import IPLocations


def draw_map(json_list):
    location_map = folium.Map()

    ipinfo = IPLocations(json_list)

    for address in ipinfo.ips:
        html = folium.Html(
            """
            <!DOCTYPE html>
            <html>
            <head>
              <h3>{title}</h3>
            </head>
            <body>
            <p>{info}</p>
            </body>
            </html> 
            """.format(title=data['domain'], info=data['address']),
            script=True
        )

    for i in json_list:
        data = json.loads(i)

        html = folium.Html(
            """
            <!DOCTYPE html>
            <html>
            <head>
              <h3>{title}</h3>
            </head>
            <body>
            <p>{info}</p>
            </body>
            </html> 
            """.format(title=data['domain'], info=data['address']),
            script=True
        )
        folium.Circle(
            radius=10,
            location=(data['latitude'], data['longitude']),
            popup=folium.Popup(html, max_height=500, max_width=500, lazy=True),

            # i['title'],
            color='#FF0000',
            fill=True,
        ).add_to(location_map)
    location_map.save('map.html')
