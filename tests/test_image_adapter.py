import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from adapters.image_adapter import extract_metadata_from_image

def test_extract_image_metadata():
    result = extract_metadata_from_image("samples/IMG_5537.jpg")
    assert isinstance(result, dict)
