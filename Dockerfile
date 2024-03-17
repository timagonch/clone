# Base Image
FROM python:3.12-slim

# Set environment variables for PostgreSQL connection
ENV DB_PORT=20290
ENV DB_HOST=roundhouse.proxy.rlwy.net
ENV DB_NAME=railway
ENV DB_USER=your_postgres
ENV DB_PASSWORD=gAGnyhsxJCbdQfsazMzNJXbtBKssbCeM

# Work directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

# Copy other project files
COPY . .

# Expose a port to Containers 
EXPOSE 8080


# Command to run on server
#CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
CMD ["gunicorn", "app:app"]
