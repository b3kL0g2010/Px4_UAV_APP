import folium


class MapGenerator:


    def __init__(self):

        pass


    def generate(
        self,
        flight_data,
        output_html
    ):

        #
        # -------------------------------------
        # HOME POSITION
        # -------------------------------------
        #

        center_lat = (
            flight_data.latitudes[0]
        )

        center_lon = (
            flight_data.longitudes[0]
        )


        #
        # -------------------------------------
        # CREATE MAP
        # -------------------------------------
        #

        fmap = folium.Map(

            location=[
                center_lat,
                center_lon
            ],

            zoom_start=18,

            tiles="OpenStreetMap"
        )


        #
        # -------------------------------------
        # FLIGHT PATH
        # -------------------------------------
        #

        coordinates = []


        for i in range(
            len(flight_data.latitudes)
        ):

            coordinates.append([

                flight_data.latitudes[i],

                flight_data.longitudes[i]
            ])


        #
        # -------------------------------------
        # ROUTE LINE
        # -------------------------------------
        #

        folium.PolyLine(

            coordinates,

            color="cyan",

            weight=4,

            opacity=0.9

        ).add_to(fmap)


        #
        # -------------------------------------
        # TAKEOFF MARKER
        # -------------------------------------
        #

        folium.Marker(

            coordinates[0],

            popup="TAKEOFF",

            icon=folium.Icon(
                color="green"
            )

        ).add_to(fmap)


        #
        # -------------------------------------
        # LANDING MARKER
        # -------------------------------------
        #

        folium.Marker(

            coordinates[-1],

            popup="LANDING",

            icon=folium.Icon(
                color="red"
            )

        ).add_to(fmap)


        #
        # -------------------------------------
        # SAVE MAP
        # -------------------------------------
        #

        fmap.save(
            output_html
        )


        print(
            "[MAP] GENERATED:",
            output_html
        )