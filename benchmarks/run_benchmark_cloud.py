from pyspark.sql import SparkSession
import time
import psutil
import pandas as pd
import os
import boto3

# Start time for benchmarking
start_time = time.time()

# Initialize Spark Session
spark = SparkSession.builder.appName("Performance Benchmarking Airline Delay").getOrCreate()

# Define the path to data and output
data_folder_path = "/opt/spark-data/"
output_excel_path = "/tmp/airline_delay_benchmark_output.xlsx"  # Save temporarily before uploading
output_csv_path = "/tmp/benchmark_results.csv"  # Save temporarily before uploading

# S3 bucket and output path
s3_bucket_name = os.getenv("S3_BUCKET_NAME")

# List of years to process
years = [str(year) for year in range(2009, 2018)]

# Function to log CPU and memory utilization
def log_resource_utilization():
    cpu_usage = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    return cpu_usage, memory_info.percent

# Start processing and logging resource usage
cpu_log, memory_log = [], []
avg_delay_data = []
total_delay_data = []

for year in years:
    file_path = os.path.join(data_folder_path, f"{year}.csv")
    df = spark.read.csv(file_path, header=True, inferSchema=True)

    # Calculate average delay per airline and total delay per day and airline
    avg_delay = df.groupBy("OP_CARRIER").agg({"DEP_DELAY": "avg"}).toPandas()
    avg_delay["Year"] = year  # Add the year for reference
    avg_delay_data.append(avg_delay)
    
    total_delay = df.groupBy("FL_DATE", "OP_CARRIER").agg({"ARR_DELAY": "sum"}).toPandas()
    total_delay["Year"] = year  # Add the year for reference
    total_delay_data.append(total_delay)

    # Log resource utilization after each year's processing
    cpu, memory = log_resource_utilization()
    cpu_log.append(cpu)
    memory_log.append(memory)
    print(f"Year {year} processed - CPU: {cpu}%, Memory: {memory}%")

end_time = time.time()
total_duration = end_time - start_time
print(f"Total Benchmarking Time: {total_duration:.2f} seconds")

# Save logs to benchmark_results.csv
log_df = pd.DataFrame({"Year": years, "CPU_Usage": cpu_log, "Memory_Usage": memory_log})
log_df.to_csv(output_csv_path, index=False)

# Save the combined average and total delay data to an Excel file with multiple sheets
with pd.ExcelWriter(output_excel_path, engine="openpyxl") as writer:
    pd.concat(avg_delay_data).to_excel(writer, sheet_name="Avg_Delay", index=False)
    pd.concat(total_delay_data).to_excel(writer, sheet_name="Total_Delay", index=False)

# Stop Spark session
spark.stop()

# Upload to S3
s3_client = boto3.client('s3')

# Ensure your environment has AWS credentials configured to access S3
s3_client.upload_file(output_excel_path, s3_bucket_name, "output/airline_delay_benchmark_output.xlsx")
s3_client.upload_file(output_csv_path, s3_bucket_name, "output/benchmark_results.csv")

# Final time logging
end_time = time.time()
print(f"Job completed in {end_time - start_time} seconds")