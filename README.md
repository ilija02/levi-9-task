
---

# Basketball Stats API

This is a simple Flask API for retrieving basketball player statistics. The application uses an in-memory SQLite database to store player data and provides endpoints for fetching player statistics.

## Prerequisites

- Python 3
- Docker (optional)

## Getting Started

### 1. Clone the Repository

```bash
git clone git@github.com:ilija02/levi-9-task.git
cd levi-9-task
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
```

- On Windows:

  ```bash
  .\venv\Scripts\activate
  ```

- On Unix or MacOS:

  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app/main.py
```

The API will be accessible at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Docker Support (Optional)

### 1. Build the Docker Image

```bash
docker build -t basketball-stats-api .
```

### 2. Run the Docker Container

```bash
docker run -p 5000:5000 basketball-stats-api
```

## Docker the lazy way

If you can't be bothered to run docker commands manually, you can do
```bash
chmod +x docker_run.sh
./docker_run.sh
```

The API will be accessible at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## API Endpoints

### Get Player Stats

Retrieve basketball player statistics by providing the player's full name.

```http
GET /stats/player/{playerFullName}/
```

Replace `{playerFullName}` with the full name of the player.

### Example

```http
curl -X GET http://127.0.0.1:5000/stats/player/Sifiso%20Abdalla/
```

## Running unit-tests

To run the unit tests, issue the following command in the project root directory (while being in a virtual environment)
```python
python -m unittest discover tests
```