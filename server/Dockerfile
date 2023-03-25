FROM python:3.9.6-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn Flask

# Copy the rest of the application code to the container
COPY . .

# Set the environment variables
ENV PORT=80

# Expose the port that the application will run on
EXPOSE 80

# Start Gunicorn
CMD gunicorn app:app \
    --bind=0.0.0.0:$PORT 