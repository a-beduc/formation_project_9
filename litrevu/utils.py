from django.core.files import File
from pathlib import Path
from PIL import Image
from io import BytesIO

images_types = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "gif": "GIF",
    "tif": "TIFF",
    "tiff": "TIFF",
}


def image_resize(image, width, height):
    """
    Resize a given image to fit within the specified width and height, maintaining aspect ratio.
    If the image is larger than the specified width or height, it will be resized to fit within the specified
    width and height; otherwise no resize occurs.
    :param image: The image to be resized.
    :param width: The maximum width allowed for the resized image.
    :param height: The maximum height allowed for the resized image.
    :return:
    """
    img = Image.open(image)

    if img.width > width or img.height > height:
        output_size = (width, height)
        img.thumbnail(output_size)

        img_filename = Path(image.file.name).name
        img_suffix = Path(image.file.name).name.split(".")[-1]
        img_format = images_types[img_suffix]

        # Create an in-memory buffer
        buffer = BytesIO()

        # Save the resized image into the buffer
        img.save(buffer, format=img_format)

        # Wrap the buffer in a Django File object
        file_object = File(buffer)

        # Save the image in the imageField
        image.save(img_filename, file_object)
