# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /src

# Copy your requirements file first (this makes rebuilding faster)
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code into an actual 'app' directory inside the container
COPY . ./app

# Expose the port FastAPI runs on
EXPOSE 8000

# Start Uvicorn pointing to the app package
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
