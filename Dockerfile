# Use the official Python image from the Docker Hub
FROM python:3.12-alpine

# Set the working directory in the container
WORKDIR /app

# Install uv
RUN pip install uv

# Copy the application code into the container
ADD . /app

# Install dependencies using uv
RUN uv sync --locked

# Don't buffer log output to stdout
ENV PYTHONUNBUFFERED=1

# Expose the application port
EXPOSE 5919

# Run the application with Gunicorn, logging to stdout
CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:5050", "--access-logfile", "-", "--error-logfile", "-", "app:app"]