from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from core.services.metadata_service import MetadataService
from PIL import Image
import io
import piexif
import base64

app = FastAPI()
service = MetadataService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract-metadata")
async def extract_metadata(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        exif_data = image.info.get("exif")
        if not exif_data:
            return {"filename": file.filename, "metadata": {}}

        exif_dict = piexif.load(exif_data)
        exif_dict.pop("thumbnail", None)

        readable = {}
        for ifd in exif_dict:
            for tag in exif_dict[ifd]:
                tag_name = piexif.TAGS[ifd][tag]["name"]
                readable[tag_name] = exif_dict[ifd][tag]

        return {"filename": file.filename, "metadata": readable}
    except Exception as e:
        return {"error": str(e)}

@app.post("/clean-metadata")
async def clean_metadata(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        original_img = Image.open(io.BytesIO(contents))
        data = list(original_img.getdata())

        clean_img = Image.new(original_img.mode, original_img.size)
        clean_img.putdata(data)

        output_buffer = io.BytesIO()
        clean_img.save(output_buffer, format="JPEG", exif=piexif.dump({}))
        output_buffer.seek(0)

        # Optional: return as base64 (for frontend preview/download)
        encoded = base64.b64encode(output_buffer.read()).decode("utf-8")

        return {
            "filename": f"{file.filename.rsplit('.', 1)[0]}_metadata_cleaned.jpg",
            "file_base64": encoded
        }

    except Exception as e:
        return {"error": str(e)}
