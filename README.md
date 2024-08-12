# Open Weather API

This project represents an API for the Open Weather API Challenge. It calls the Open Weather API, retrieving its data and processing them using async jobs.


## Technologies

1. Python 3.11.
2. FastAPI and all its dependencies to the API itself.
3. SQLite database.
4. pytest and auxiliary dependencies to run unit tests.
5. Celery to run async tasks.


## Authentication to Open Weather API

You have to set up a **.env** file based on **.env.sample**. It has 2 attributes to be defined: **APP_ID** and **DATABASE_NAME**. **APP_ID** is the API token generated in Open Weather's website and you need it to run the endpoints sucessfully. **DATABASE_NAME** can be defined by any value with its default value being **sql-app** if it is not defined. If the database already exists and you want to reset it, you can delete the SQLite database file and it will create a new database when the application is executed again.


## Instructions to run application

After cloning the repository, you can run this API using Docker-compose. To set it up, you just need to run the following command:

```docker-compose up --build```

It will create Docker containers based on what is defined inside docker-compose.yml and Dockerfile.
The application runs on port 8000 by default.

## Running unit tests

To run all the unit tests, you must get inside of the Docker container and make sure you are in **api/** directory. Execute the following commands:

```
docker exec -it open-weather-challenge-web-1 bash
pytest
```