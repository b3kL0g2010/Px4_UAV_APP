from pyulog import ULog

from modules.px4_geotagger.backend.flight_data import FlightData

from modules.px4_geotagger.backend.mission.mission_detector import MissionDetector


class ULogParser:


    def __init__(self):

        self.flight_data = FlightData()


    def load(
        self,
        ulg_path
    ):

        #
        # ----------------------------------
        # LOAD ULOG
        # ----------------------------------
        #

        ulog = ULog(
            ulg_path
        )

        print(
            "[ULOG] FILE LOADED"
        )

        #
        # ----------------------------------
        # DETECT MISSION START
        # ----------------------------------
        #

        detector = MissionDetector()

        self.flight_data.mission_start_utc = (

            detector.detect_mission_start(
                ulog
            )
        )

        #
        # ----------------------------------
        # FIND GPS TOPIC
        # ----------------------------------
        #

        gps_topic = None

        for dataset in ulog.data_list:

            if dataset.name == "vehicle_gps_position":

                gps_topic = dataset

                break

        if gps_topic is None:

            raise RuntimeError(
                "vehicle_gps_position topic not found."
            )

        #
        # ----------------------------------
        # GPS DATA
        # ----------------------------------
        #

        gps_data = gps_topic.data

        timestamps = gps_data["timestamp"]

        utc_times = gps_data["time_utc_usec"]

        latitudes = gps_data["latitude_deg"]

        longitudes = gps_data["longitude_deg"]

        altitudes = gps_data["altitude_msl_m"]

        #
        # ----------------------------------
        # STORE GPS DATA
        # ----------------------------------
        #

        for i in range(

            len(
                timestamps
            )
        ):

            self.flight_data.timestamps.append(

                timestamps[i]
            )

            self.flight_data.utc_times.append(

                utc_times[i]
            )

            self.flight_data.latitudes.append(

                latitudes[i]
            )

            self.flight_data.longitudes.append(

                longitudes[i]
            )

            self.flight_data.altitudes.append(

                altitudes[i]
            )

        #
        # ----------------------------------
        # VEHICLE STATUS
        # ----------------------------------
        #

        for dataset in ulog.data_list:

            if dataset.name == "vehicle_status":

                status_data = dataset.data

                nav_states = status_data["nav_state"]

                status_timestamps = status_data["timestamp"]

                for i in range(

                    len(
                        nav_states
                    )
                ):

                    self.flight_data.flight_modes.append(

                        {

                            "timestamp":
                                status_timestamps[i],

                            "nav_state":
                                nav_states[i]
                        }
                    )

                break

        #
        # ----------------------------------
        # BASIC INFO
        # ----------------------------------
        #

        self.flight_data.total_gps_samples = len(

            self.flight_data.timestamps
        )

        self.flight_data.home_position = (

            self.flight_data.latitudes[0],

            self.flight_data.longitudes[0]
        )

        #
        # ----------------------------------
        # FIND MISSION GPS INDEX
        # ----------------------------------
        #

        if self.flight_data.mission_start_utc:

            closest_index = min(

                range(
                    len(
                        self.flight_data.utc_times
                    )
                ),

                key=lambda i:

                abs(

                    self.flight_data.utc_times[i]

                    -

                    self.flight_data.mission_start_utc
                )
            )

            self.flight_data.mission_start_index = (

                closest_index
            )

        #
        # ----------------------------------
        # DEBUG
        # ----------------------------------
        #

        print(
            "[ULOG] GPS SAMPLES:",
            self.flight_data.total_gps_samples
        )

        print(
            "[ULOG] HOME:",
            self.flight_data.home_position
        )

        print(
            "[UTC FIRST]",
            self.flight_data.utc_times[0]
        )

        print(
            "[UTC LAST]",
            self.flight_data.utc_times[-1]
        )

        print(
            "[MISSION UTC]",
            self.flight_data.mission_start_utc
        )

        print(
            "[MISSION INDEX]",
            self.flight_data.mission_start_index
        )

        return self.flight_data