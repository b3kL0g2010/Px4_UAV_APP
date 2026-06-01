import pandas as pd

class MissionDetector:

    def detect_mission_start(self,ulog):

        """
        Detect mission start using PX4 logged messages
        and convert PX4 boot timestamp into real GPS UTC.

        Returns:
            int:
                UTC timestamp in microseconds
        """
        # -------------------------------------------------
        # LOAD GPS DATASET
        # -------------------------------------------------

        try:

            gps_data = ulog.get_dataset(
                "vehicle_gps_position"
            ).data

        except Exception:

            raise RuntimeError(
                "vehicle_gps_position topic not found."
            )

        gps_df = pd.DataFrame(gps_data)

        if gps_df.empty:

            raise RuntimeError(
                "GPS dataset is empty."
            )

        # -------------------------------------------------
        # LOAD PX4 LOGGED MESSAGES
        # -------------------------------------------------

        try:

            logs = ulog.logged_messages

            print("\n========== LOGGED MESSAGES ==========")

            for i, log in enumerate(logs[:100]):

                try:

                    print(
                        i,
                        log.timestamp,
                        log.message
                    )

                except Exception:

                    pass

            print("=====================================\n")

        except Exception as e:

            print(e)

            raise RuntimeError(
                "Failed to access PX4 logged messages."
            )

        if not logs:

            raise RuntimeError(
                "No PX4 logged messages found."
            )

        # -------------------------------------------------
        # SEARCH FOR EXECUTING MISSION MESSAGE
        # -------------------------------------------------

        mission_log = None

        for log in logs:

            try:

                message_text = str(
                    log.message
                ).lower()

                if (
                    "executing mission"
                    in
                    message_text
                ):

                    mission_log = log
                    break

            except Exception:

                continue

        # -------------------------------------------------
        # FALLBACK TO NAV STATE
        # -------------------------------------------------

        if mission_log is None:

            print(
                "[WARNING] "
                "'Executing Mission' "
                "message not found."
            )

            print(
                "[INFO] "
                "Falling back to "
                "vehicle_status nav_state."
            )

            try:

                vehicle_status = ulog.get_dataset(
                    "vehicle_status"
                ).data

            except Exception:

                raise RuntimeError(
                    "vehicle_status topic not found."
                )

            status_df = pd.DataFrame(
                vehicle_status
            )


            print(
                "[NAV STATES AVAILABLE]"
            )

            print(
                sorted(
                    status_df["nav_state"]
                    .unique()
                    .tolist()
                )
            )
            print(
                status_df[
                    ["timestamp", "nav_state"]
                ].head(50)
            )



        else:

            # ---------------------------------------------
            # PX4 BOOT-RELATIVE TIMESTAMP
            # ---------------------------------------------

            boot_timestamp = int(
                mission_log.timestamp
            )

        # -------------------------------------------------
        # CONVERT PX4 BOOT TIME
        # TO GPS UTC TIME
        # -------------------------------------------------

        gps_df["timestamp"] = pd.to_numeric(
            gps_df["timestamp"],
            errors="coerce"
        )

        gps_df["time_utc_usec"] = pd.to_numeric(
            gps_df["time_utc_usec"],
            errors="coerce"
        )

        gps_df = gps_df.dropna(
            subset=[
                "timestamp",
                "time_utc_usec"
            ]
        )

        gps_df = gps_df[
            gps_df["time_utc_usec"] > 0
        ]

        if gps_df.empty:

            raise RuntimeError(
                "No valid GPS UTC timestamps."
            )

        # -------------------------------------------------
        # FIND CLOSEST GPS FRAME
        # -------------------------------------------------

        closest_idx = (

            gps_df["timestamp"]
            -
            boot_timestamp

        ).abs().idxmin()

        utc_timestamp = int(

            gps_df.loc[
                closest_idx,
                "time_utc_usec"
            ]

        )

        # -------------------------------------------------
        # DEBUG LOGGING
        # -------------------------------------------------

        print(

            f"[MISSION] "
            f"PX4 Boot Timestamp: "
            f"{boot_timestamp}"

        )

        print(

            f"[MISSION] "
            f"GPS UTC Start: "
            f"{utc_timestamp}"

        )

        # -------------------------------------------------
        # RETURN UTC TIMESTAMP
        # -------------------------------------------------

        return utc_timestamp