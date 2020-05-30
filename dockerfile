FROM ubuntu:18.04

# Upgrade installed packages
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Python package management and basic dependencies
RUN apt-get install -y curl python3.6 python3.6-dev python3.6-distutils 


# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app 
ADD . /app

# Install the dependencies
RUN apt-get install -y python3-pip
RUN pip3 install -r requirements.txt

# run the command to start uWSGI
CMD ["python3", "/app/app.py"]
