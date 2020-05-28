# Use the Python3.7.2 image
FROM python:3.6-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app 
ADD . .

# Install the dependencies
RUN pip install -r requirements.txt

# run the command to start uWSGI
CMD ["python3", "/app/app.py"]
