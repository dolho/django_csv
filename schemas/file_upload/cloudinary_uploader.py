from .base_uploader import AbstractFileUploader
import cloudinary
import cloudinary.uploader
import cloudinary.api
from csv_creator.settings import CLOUD_NAME, CLOUD_API_KEY, CLOUD_API_SECRET

cloudinary.config(
     cloud_name=CLOUD_NAME,
     api_key=CLOUD_API_KEY,
     api_secret=CLOUD_API_SECRET
)
cloudinary.config()


class CloudinaryFileUploader(AbstractFileUploader):

    def upload(self, file, **options):
        return cloudinary.uploader.upload(file, **options)

    def return_link_to_file(self, filename):
        return cloudinary.utils.cloudinary_url(filename, resource_type="raw")
        # return f"https://res.cloudinary.com/dz1vtcq3j/raw/upload/v1643366430/{filename}"

    def delete(self, file, **options):
        raise NotImplementedError