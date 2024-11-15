# Use a Python base image
FROM python:3.9

# Set up working directory inside the container
WORKDIR /config

# Install required Python packages and docker-compose
RUN pip install psutil && apt-get update && apt-get install -y docker-compose

# Copy the scale_monitor.py script from the host to the container
COPY scripts/scale_monitor.py /config/scripts/scale_monitor.py

# Set the entrypoint to execute scale_monitor.py
ENTRYPOINT ["python3", "/config/scripts/scale_monitor.py"]