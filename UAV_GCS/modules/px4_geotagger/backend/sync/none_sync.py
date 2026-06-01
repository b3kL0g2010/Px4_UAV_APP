class NoneSync:


    def get_gps_for_image(

        self,

        image_utc,

        flight_data
    ):

        if image_utc is None:

            return None

        if image_utc < flight_data.utc_times[0]:

            return None

        if image_utc > flight_data.utc_times[-1]:

            return None

        closest_index = min(

            range(
                len(
                    flight_data.utc_times
                )
            ),

            key=lambda i:

            abs(

                flight_data.utc_times[i]

                -

                image_utc
            )
        )

        return {

            "gps_index":
                closest_index,

            "utc":
                flight_data.utc_times[
                    closest_index
                ],

            "lat":
                flight_data.latitudes[
                    closest_index
                ],

            "lon":
                flight_data.longitudes[
                    closest_index
                ],

            "alt":
                flight_data.altitudes[
                    closest_index
                ]
        }