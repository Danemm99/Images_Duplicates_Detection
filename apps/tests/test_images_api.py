import io
from PIL import Image
from apps.tests.conftest import setup_qdrant
from apps.crud.crud_images import crud_images
from dotenv import load_dotenv
import os


load_dotenv()

collection_name = os.getenv("TEST_COLLECTION_NAME")


class FakeUploadFile:
    def __init__(self, filename, file, content_type, size):
        self.filename = filename
        self.file = file
        self.content_type = content_type
        self.size = size


def create_test_image(filename: str, size=(224, 224), color=(73, 109, 137)):
    image = Image.new("RGB", size, color=color)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return (filename, img_byte_arr)


def test_add_images(setup_qdrant):
    filename, img = create_test_image("test_image.png")
    request_id = "test_request_id"

    files = [FakeUploadFile(filename, img, "image/png", img.getbuffer().nbytes)]

    response = crud_images.add_images(
        files=files,
        request_id=request_id,
        collection_name=collection_name
    )

    assert response["uploaded"] == 1
    assert response["request_id"] == request_id


def test_find_duplicates(setup_qdrant):
    filename1, img1 = create_test_image("duplicate_image.png")
    filename2, img2 = create_test_image("duplicate_image.png")
    request_id = "test_request_id"

    files = [FakeUploadFile(filename1, img1, "image/png", img1.getbuffer().nbytes),
             FakeUploadFile(filename2, img2, "image/png", img2.getbuffer().nbytes)]

    crud_images.add_images(files=files, request_id=request_id, collection_name=collection_name)
    response = crud_images.find_duplicates(request_id=request_id, collection_name=collection_name)

    assert "duplicates" in response
    assert len(response["duplicates"]) > 0


def test_unsupported_file_format(setup_qdrant):
    filename, img = create_test_image("unsupported_image.bmp")
    request_id = "test_request_id"

    files = [FakeUploadFile(filename, img, "image/bmp", img.getbuffer().nbytes)]

    response = crud_images.add_images(
        files=files,
        request_id=request_id,
        collection_name=collection_name
    )

    assert response["error"] == "Unsupported file format: image/bmp. Only JPEG and PNG are allowed."
