import shutil
import piexif


class ExifWriter:


    def __init__(self):

        pass


    def to_deg(
        self,
        value
    ):

        degrees = int(value)

        minutes_float = abs(
            value - degrees
        ) * 60

        minutes = int(
            minutes_float
        )

        seconds = round(

            (
                minutes_float
                -
                minutes
            )

            * 60

            * 100
        )

        return (

            (
                abs(degrees),
                1
            ),

            (
                minutes,
                1
            ),

            (
                seconds,
                100
            )
        )


    def write_gps(

        self,

        image_path,

        output_path,

        latitude,

        longitude,

        altitude
    ):

        #
        # COPY IMAGE
        #

        shutil.copy2(

            image_path,

            output_path
        )

        #
        # LOAD EXISTING EXIF
        #

        try:

            exif_dict = piexif.load(
                output_path
            )

        except Exception:

            exif_dict = {

                "0th": {},

                "Exif": {},

                "GPS": {},

                "1st": {},

                "thumbnail": None
            }

        #
        # LATITUDE
        #

        exif_dict["GPS"][

            piexif.GPSIFD.GPSLatitudeRef

        ] = (

            b"N"

            if latitude >= 0

            else b"S"
        )

        exif_dict["GPS"][

            piexif.GPSIFD.GPSLatitude

        ] = self.to_deg(

            latitude
        )

        #
        # LONGITUDE
        #

        exif_dict["GPS"][

            piexif.GPSIFD.GPSLongitudeRef

        ] = (

            b"E"

            if longitude >= 0

            else b"W"
        )

        exif_dict["GPS"][

            piexif.GPSIFD.GPSLongitude

        ] = self.to_deg(

            longitude
        )

        #
        # ALTITUDE
        #

        exif_dict["GPS"][

            piexif.GPSIFD.GPSAltitudeRef

        ] = 0

        exif_dict["GPS"][

            piexif.GPSIFD.GPSAltitude

        ] = (

            int(
                altitude * 100
            ),

            100
        )

        #
        # WRITE EXIF
        #

        exif_bytes = piexif.dump(
            exif_dict
        )

        piexif.insert(

            exif_bytes,

            output_path
        )