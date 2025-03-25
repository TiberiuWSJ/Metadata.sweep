from PIL import Image
import piexif


#basic adapter for images
def extract_metadata_from_image(file_path: str) -> dict:
    try:
        img = Image.open(file_path)
        exif_data = img.info.get("exif")
        if not exif_data:
            return {}

        exif_dict = piexif.load(exif_data)
        # Remove 'thumbnail' key, it's not useful AND causes issues
        exif_dict.pop('thumbnail', None)
        readable = {}

        for ifd in exif_dict:
            for tag in exif_dict[ifd]:
                tag_name = piexif.TAGS[ifd][tag]["name"]
                readable[tag_name] = exif_dict[ifd][tag]
        return readable
    except Exception as e:
        return {"error": str(e)}

import piexif
from PIL import Image
import os

def clean_metadata_from_image(file_path: str, output_path: str = None):
    try:
        img = Image.open(file_path)
        data = list(img.getdata())
        clean_img = Image.new(img.mode, img.size)
        clean_img.putdata(data)

        # Save cleaned image to the root directory with a _metadata_cleaned suffix
        if not output_path:
            base_name = os.path.basename(file_path)  # e.g., "IMG_5537.jpg"
            name, ext = os.path.splitext(base_name)
            output_path = os.path.abspath(f"./{name}_metadata_cleaned{ext}")

        clean_img.save(output_path, exif=piexif.dump({}))
        return output_path

    except Exception as e:
        raise RuntimeError(f"Failed to clean image metadata: {e}")

