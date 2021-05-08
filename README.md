# match-recommendation-service
Match Recommendation Service for the Harmony app.

## Local Setup
Requires Python-3.6+.
* Clone the forked repository.
* Create a virtual environment: `python -m venv venv`.
* Upgrade PIP: `python -m pip install –upgrade pip`
* Install all dependencies: `pip install -r requirements.txt`
* Set `DATABASE_URL` environment variable to a Postgres database URL (local/cloud).
* Set `SPOTIFY_CLIENT_ID` & `SPOTIFY_CLIENT_SECRET` environment variables with Spotify credentials.
* Run migration scripts: `alembic upgrade head`
* Start application: `uvicorn api.main:app --reload`
* Generate migrations: `alembic revision --autogenerate -m <revision-msg>`

API documentations available at `/docs` & `/redoc`.
