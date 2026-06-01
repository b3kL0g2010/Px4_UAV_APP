from pathlib import Path


class ImageLoader:


    def load_folder(

        self,

        folder_path
    ):

        images = []

        extensions = (

            "*.jpg",

            "*.jpeg",

            "*.tif",

            "*.tiff"
        )

        for ext in extensions:

            images.extend(

                Path(
                    folder_path
                ).glob(ext)
            )

        return sorted(

            [str(x) for x in images]
        )