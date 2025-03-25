from adapters.image_adapter import extract_metadata_from_image, clean_metadata_from_image


# use case layer -> knows what to do, but delegates how to do it to adapters
class MetadataService:
    def extract(self, file_path: str, file_type: str):
        if file_type == "image":
            return extract_metadata_from_image(file_path)
        else:
            raise NotImplementedError(f"Unsupported type: {file_type}")

    def clean(self, file_path: str, file_type: str):
        if file_type == "image":
            clean_metadata_from_image(file_path)
        else:
            raise NotImplementedError(f"Unsupported type: {file_type}")
