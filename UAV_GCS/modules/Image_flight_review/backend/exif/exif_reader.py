from PIL import Image


class ExifReader:


    def dms_to_decimal(

        self,

        dms,

        ref
    ):

        try:

            degrees = float(
                dms[0]
            )

            minutes = float(
                dms[1]
            )

            seconds = float(
                dms[2]
            )

        except Exception:

            print(
                "[DMS ERROR]",
                dms
            )

            return None

        decimal = (

            degrees

            +

            (minutes / 60)

            +

            (seconds / 3600)
        )

        if ref in [

            "S",

            "W"
        ]:

            decimal *= -1

        return decimal


    def get_location(

        self,

        image_path
    ):

        try:

            image = Image.open(
                image_path
            )

            exif = image._getexif()

            if exif is None:

                print(
                    "[NO EXIF]"
                )

                return None

            gps = exif.get(
                34853
            )

            print(
                "[GPS BLOCK]",
                gps
            )

            if gps is None:

                return None

            lat_ref = gps.get(
                1
            )

            lat_dms = gps.get(
                2
            )

            lon_ref = gps.get(
                3
            )

            lon_dms = gps.get(
                4
            )

            altitude = gps.get(
                6,
                0
            )

            if (

                lat_ref is None

                or

                lat_dms is None

                or

                lon_ref is None

                or

                lon_dms is None

            ):

                print(
                    "[GPS INVALID]"
                )

                return None

            lat = self.dms_to_decimal(

                lat_dms,

                lat_ref
            )

            lon = self.dms_to_decimal(

                lon_dms,

                lon_ref
            )

            result = {

                "lat":
                    lat,

                "lon":
                    lon,

                "alt":
                    float(
                        altitude
                    )
            }

            print(
                "[GPS PARSED]",
                result
            )

            return result

        except Exception as e:

            print(
                "[EXIF ERROR]",
                str(e)
            )

            return None