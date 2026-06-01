import os


class ImageLoader:


    def __init__(self):

        pass


    def load_folder(self, folder_path):

        image_paths = []


        for root, dirs, files in os.walk(folder_path):

            for file in files:

                if file.lower().endswith(

                    (
                        ".jpg",
                        ".jpeg"
                    )
                ):

                    full_path = os.path.join(

                        root,
                        file
                    )

                    image_paths.append(
                        full_path
                    )


        print(
            "[IMAGES] FOUND:",
            len(image_paths)
        )

        return image_paths