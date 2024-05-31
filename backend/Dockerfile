# Use the latest stable version of the base image with Python 3.8
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8


# Set environment variables
ENV PYTHONPATH="${PYTHONPATH}:/"
ENV PORT=8000

# Install system dependencies
RUN apt-get update \
    && apt-get install -y default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
