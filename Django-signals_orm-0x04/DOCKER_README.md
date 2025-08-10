# Docker Setup for Django Messaging App

This document provides instructions for setting up and running the Django messaging app using Docker and Docker Compose.

## Prerequisites

- Docker installed on your system
- Docker Compose installed on your system

## Project Structure

```
messaging_app/
├── Dockerfile                 # Docker image configuration
├── docker-compose.yml         # Multi-container setup
├── requirements.txt           # Python dependencies
├── .env                      # Environment variables
├── .dockerignore             # Files to exclude from Docker build
├── manage.py                 # Django management script
├── messaging_app/            # Django project settings
├── messaging/                # Django app
└── mysql/                    # MySQL initialization scripts
    └── init/
```

## Quick Start

### 1. Build and Run with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build
```

### 2. Access the Application

- **Django App**: http://localhost:8000
- **MySQL Database**: localhost:3306

### 3. Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: This will delete all data)
docker-compose down -v
```

## Manual Docker Commands

### Build Docker Image

```bash
docker build -t messaging-app .
```

### Run Container

```bash
docker run -p 8000:8000 messaging-app
```

## Database Management

### Connect to MySQL Container

```bash
docker-compose exec db mysql -u messaging_user -p messaging_db
```

### Run Django Migrations

```bash
docker-compose exec web python manage.py migrate
```

### Create Superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

### Run Django Shell

```bash
docker-compose exec web python manage.py shell
```

## Environment Variables

The following environment variables are configured in `.env`:

- `DEBUG`: Django debug mode
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DB_NAME`: MySQL database name
- `DB_USER`: MySQL username
- `DB_PASSWORD`: MySQL password
- `DB_HOST`: MySQL host (set to 'db' for Docker)
- `DB_PORT`: MySQL port
- `MYSQL_DATABASE`: MySQL database name
- `MYSQL_USER`: MySQL username
- `MYSQL_PASSWORD`: MySQL password
- `MYSQL_ROOT_PASSWORD`: MySQL root password

## Volumes

- `mysql_data`: Persists MySQL database data across container restarts
- `static_volume`: Persists Django static files

## Troubleshooting

### Common Issues

1. **Port already in use**: Make sure ports 8000 and 3306 are available
2. **Database connection failed**: Wait for MySQL to fully start up
3. **Permission denied**: Check file permissions in your project directory

### View Logs

```bash
# View all service logs
docker-compose logs

# View specific service logs
docker-compose logs web
docker-compose logs db
```

### Reset Everything

```bash
# Stop all services and remove volumes
docker-compose down -v

# Remove all images
docker rmi $(docker images -q)

# Start fresh
docker-compose up --build
```

## Development Workflow

1. Make changes to your code
2. Rebuild the Docker image: `docker-compose build web`
3. Restart the web service: `docker-compose restart web`
4. Or restart all services: `docker-compose restart`

## Production Considerations

- Change `DEBUG=False` in `.env`
- Use strong, unique passwords
- Consider using Docker secrets for sensitive data
- Set up proper logging and monitoring
- Use a reverse proxy (nginx) in front of the Django app
