# Images Duplicates Detection

## Overview of Key Functions:

1.  **`add_images`**:
    
    *   Accepts a list of image files.
    *   Checks the file format (only JPEG and PNG are supported) and file size (up to 10 MB).
    *   Converts the images into vectors using the `image_to_vector` function.
    *   Stores the vectors in a Qdrant collection along with additional file information (`filename`, `url`, `request_id`).
    *   Returns the count of successfully uploaded images along with the `request_id`.

2.  **`find_duplicates`**:
    
    *   Accepts a `request_id` and searches for images in Qdrant that match this `request_id`.
    *   For each found image, it searches for similar images based on their vectors.
    *   If duplicates are found, it returns a list of these duplicates with detailed information (image ID, `url`, `filename`).
    *   If no duplicates are found, it returns an appropriate message.

This allows users to upload images and check for duplicates using vector similarity.

## Setup

**1. Clone the repository to your folder:**
```commandline
https://github.com/Danemm99/Images_Duplicates_Detection.git
```

**2. Navigate to the project directory:**
```commandline
cd Images_Duplicates_Detection
```

**3. Set your environment variable in .env file with needed data:**

```commandline
cp .env.example .env
```

**4. Build docker images and containers:**

```commandline
docker compose up --build
```

Start the containers if they are not already running.

**5. Run tests:**

```commandline
docker compose exec api /bin/bash
```

```commandline
pytest
```

## Endpoint documentation:

```commandline
localhost:8000/docs
```

## Qdrant:

```commandline
localhost:6333/dashboard
```
