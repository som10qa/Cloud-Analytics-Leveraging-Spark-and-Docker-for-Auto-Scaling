
# Cloud-Based Data Analytics Platform with Auto-Scaling

## Introduction

This project creates a platform for analyzing large amounts of data using Apache Spark and Docker. It automatically scales up or down based on how much work needs to be done. This makes it easier to handle large datasets without wasting resources.

## Features

- **Data Processing with Spark:** Use Spark to quickly analyze large datasets.
- **Auto-Scaling:** Automatically adjusts the number of workers based on CPU usage.
- **Dockerized Setup:** The platform runs in Docker containers for easy deployment.
- **AWS S3 Integration:** Data is stored and accessed in an AWS S3 bucket.

## How It Works

1. **Setup with Docker:** The platform uses Docker containers for Spark master and workers.
2. **Dynamic Scaling:** A script monitors CPU usage and adjusts the number of workers.
3. **Data Processing:** The platform processes data stored in AWS S3.
4. **Results:** Outputs are saved and uploaded back to S3.

## How to Use

1. **Clone the Repository:**
   ```bash
   git clone <repository-link>
   cd project-folder
   ```

2. **Set Up Environment Variables:**
   Create a `.env` file with your AWS credentials:
   ```
   AWS_ACCESS_KEY_ID=<your-access-key>
   AWS_SECRET_ACCESS_KEY=<your-secret-key>
   S3_BUCKET_NAME=<your-bucket-name>
   ```

3. **Build and Start Docker Containers:**
   ```bash
   docker-compose up --build
   ```

4. **Submit a Spark Job:**
   Run the command inside the Spark master container:
   ```bash
   docker exec -it spark-master /opt/spark/bin/spark-submit \
       --master spark://spark-master:7077 \
       --conf spark.eventLog.enabled=true \
       --conf spark.eventLog.dir=/tmp/spark-events \
       /path/to/your-spark-job.py
   ```

5. **Check Outputs:**
   Processed results are saved to your S3 bucket.

## Folder Structure

- `config/`: Configuration files, including `docker-compose.yml`.
- `scripts/`: Scripts for auto-scaling and monitoring.
- `data/`: Data storage for local testing.
- `logs/`: Logs for monitoring system performance.

## Future Improvements

- Adding Kubernetes for better scaling.
- Improving resource usage efficiency.
- Adding a user-friendly interface.
