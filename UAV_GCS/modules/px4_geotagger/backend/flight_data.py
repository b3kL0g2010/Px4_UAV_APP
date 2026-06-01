class FlightData:

    def __init__(self):

        #
        # PX4 INTERNAL TIMESTAMPS
        #
        self.timestamps = []

        #
        # GPS UTC TIMES
        # (time_utc_usec)
        #
        self.utc_times = []

        #
        # GPS DATA
        #
        self.latitudes = []

        self.longitudes = []

        self.altitudes = []

        #
        # FLIGHT MODES
        #
        self.flight_modes = []

        #
        # BASIC INFO
        #
        self.home_position = None

        self.total_gps_samples = 0

        self.vehicle_type = None



        self.mission_start_utc = None

        self.mission_start_index = None

        self.camera_start_offset_usec = 0