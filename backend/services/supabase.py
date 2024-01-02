from supabase import create_client, Client
from PIL import Image
from supabase import create_client
from PIL import Image
import numpy as np
import io
import os
import tempfile
import time
from dotenv import load_dotenv

load_dotenv()


class Supabase:
    def __init__(self):
        self.client = create_client(
            supabase_url=os.environ.get("BACKEND_SUPABASE_URL"),
            supabase_key=os.environ.get("BACKEND_SUPABASE_PUBLIC_API")
        )

    def upload_image(self, image: Image, image_name: str):
        """
        Upload an image to Supabase Storage.
        :param image: PIL Image object.
        :param image_name: name of the image.
        :return: URL of the image.
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            image.save(temp_file, format="PNG")
            temp_file_path = temp_file.name

        # Upload the image to Supabase Storage
        with open(temp_file_path, 'rb') as file_to_upload:
            response = self.client.storage.from_("images").upload(
                path=image_name,
                file=file_to_upload,
                file_options={"content-type": "image/png"}
            )
        # Clean up temporary file
        os.remove(temp_file_path)

        url = self.client.storage.from_("images").get_public_url(image_name)
        return url
