# Docker Workflow Guide

This guide provides the standard commands and procedures for developing, testing, and managing this project using Docker.

## Initial Setup & Building

To build the Docker image for the application:
```bash
docker compose build
```

## Running the Application

### Start the Server
To start the application using the current configuration (runs via `gunicorn`):
```bash
docker compose up
```

### Run in Detached Mode
To run the containers in the background:
```bash
docker compose up -d
```

> **Note:** Because the current setup does not use volume mounts for source code, any changes you make to the code will require you to rebuild the image to see the changes:
> ```bash
> docker compose build
> ```

## Django Management Commands

You can run Django management commands by using `docker compose run --rm server`. This starts a one-off container, executes the command, and removes the container when finished.

### Database Migrations
Run migrations:
```bash
docker compose run --rm server python manage.py migrate
```

Create new migrations:
```bash
docker compose run --rm server python manage.py makemigrations
```

### Administrative Tasks
Create a superuser:
```bash
docker compose run --rm server python manage.py createsuperuser
```

Open a Django shell:
```bash
docker compose run --rm server python manage.py shell
```

## Running Tests

To run the application's test suite inside a container:
```bash
docker compose run --rm server python manage.py test
```

## Monitoring & Logs

### View Logs
To see the output from your running containers:
```bash
docker compose logs -f server
```

## Stopping & Cleanup

### Stop Containers
To stop the running services:
```bash
docker compose stop
```

### Remove Containers
To stop and remove all containers defined in `compose.yaml`:
```bash
docker compose down
```
