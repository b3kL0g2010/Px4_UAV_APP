class TimeSync:


    def get_gps_for_image(

        self,

        image_index,

        interval_seconds,

        flight_data
    ):

        target_utc = (

            flight_data.mission_start_utc

            +

            flight_data.camera_start_offset_usec

            +

            image_index

            *

            interval_seconds

            *

            1_000_000
        )

        if target_utc > flight_data.utc_times[-1]:

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

                target_utc
            )
        )

        return {

            "gps_index":
                closest_index,

            "utc":
                target_utc,

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