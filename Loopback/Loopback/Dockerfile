    # Use an official Python runtime as a parent image
    FROM python:3.9-slim-buster

    # Set the working directory in the container
    WORKDIR /app

    # Set environment variables
    ENV PYTHONDONTWRITEBYTECODE 1
    ENV PYTHONUNBUFFERED 1

    # Install dependencies
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    # Copy the Django project code into the container
    COPY . .

    # Expose the port Django will run on
    EXPOSE 8000

    # Command to run the Django application
    CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]