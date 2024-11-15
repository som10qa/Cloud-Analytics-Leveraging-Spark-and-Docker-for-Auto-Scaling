# Use the official Spark image
FROM apache/spark:latest

# Install additional packages
USER root
RUN apt-get update && \
    apt-get install -y procps iputils-ping curl netcat && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

# Copy the startup script for Spark Worker
COPY scripts/start-master.sh /opt/spark/scripts/start-master.sh
RUN chmod +x /opt/spark/scripts/start-master.sh
RUN pip install pandas openpyxl pyspark psutil python-dotenv boto3

RUN wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar -P /opt/spark/jars/
RUN wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.538/aws-java-sdk-bundle-1.12.538.jar -P /opt/spark/jars/

# Expose the necessary ports for Spark Worker
EXPOSE 8081

# Start the Spark Worker process
ENTRYPOINT ["/opt/spark/scripts/start-master.sh"]
