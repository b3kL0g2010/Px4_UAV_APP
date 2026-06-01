from pathlib import Path

import folium


class MapGenerator:


    def generate(

        self,

        image_records,

        output_file
    ):

        if not image_records:

            return

        center_lat = image_records[0]["lat"]

        center_lon = image_records[0]["lon"]

        m = folium.Map(

            location=[

                center_lat,

                center_lon
            ],

            zoom_start=18
        )
        #
        # START POINT
        #

        start = image_records[0]

        folium.Marker(

            location=[

                start["lat"],

                start["lon"]
            ],

            popup="START",

            tooltip="START",

            icon=folium.Icon(
                color="green",
                icon="play"
            )

        ).add_to(m)

        #
        # END POINT
        #

        end = image_records[-1]

        folium.Marker(

            location=[

                end["lat"],

                end["lon"]
            ],

            popup="END",

            tooltip="END",

            icon=folium.Icon(
                color="red",
                icon="stop"
            )

        ).add_to(m)

        #
        # FLIGHT PATH POLYLINE
        #

        path = [

            (
                record["lat"],
                record["lon"]
            )

            for record in image_records
        ]

        folium.PolyLine(

            path,

            color="cyan",

            weight=3,

            opacity=0.8

        ).add_to(m)

        m.fit_bounds(path)

        #
        # IMAGE POINTS
        # each image location is marked with a circle marker and a popup showing the filename and coordinates

        
        for record in image_records:

            filename = Path(

                record["file"]

            ).name

            popup_text = (

                f"{filename}<br>"

                f"Lat: {record['lat']:.7f}<br>"

                f"Lon: {record['lon']:.7f}<br>"

                f"Alt: {record['alt']:.2f} m"
            )

            folium.CircleMarker(

                location=[

                    record["lat"],

                    record["lon"]
                ],

                radius=4,

                popup=popup_text,

                color="red",

                fill=True,

                fill_opacity=1.0

            ).add_to(m)

        m.save(
            output_file
        )