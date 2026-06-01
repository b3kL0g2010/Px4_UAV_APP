from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime, timezone


class ExifReader:

    def __init__(self):

        pass


    def read(self, image_path):

        try:

            image = Image.open(
                image_path
            )

            exif_data = image._getexif()

            if exif_data is None:

                return {}

            result = {}

            for tag_id, value in exif_data.items():

                tag = TAGS.get(
                    tag_id,
                    tag_id
                )

                result[tag] = value

            return result

        except Exception as e:

            print(
                "[EXIF ERROR]",
                str(e)
            )

            return {}
        

    def get_capture_time(
        self,
        image_path
    ):

        exif = self.read(
            image_path
        )

        dt_string = exif.get(
            "DateTimeOriginal",
            None
        )

        if dt_string is None:

            return None

        try:

            return datetime.strptime(

                dt_string,

                "%Y:%m:%d %H:%M:%S"
            )

        except Exception:

            return None
        
    def get_capture_utc_usec(
        self,
        image_path
    ):

        dt = self.get_capture_time(
            image_path
        )

        print(
            "[EXIF DATETIME]",
            dt
        )

        print(
            "[EXIF UTC USEC]",
            int(
                dt.timestamp()
                *
                1_000_000
            )
        )

        if dt is None:

            return None

        dt = dt.replace(
            tzinfo=timezone.utc
        )

        return int(

            dt.timestamp()

            *

            1_000_000
        )