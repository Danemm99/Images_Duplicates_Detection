# Images Duplicates Detection

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
docker-compose exec api /bin/bash
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
