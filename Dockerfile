# Base image
FROM ubuntu:20.04

# Set the working directory
WORKDIR /kick_interview_repo

# Create required directories in the working directory
RUN mkdir -p /kick_interview_repo/db_table_csv \
    && mkdir -p /kick_interview_repo/horse_pdf \
    && mkdir -p /kick_interview_repo/house_image

# Update the package lists for Ubuntu and install Python 3.8 and pip
RUN apt update \
    && apt install -y python3.8 python3-pip

# Upgrade pip to the latest version
RUN python3.8 -m pip install --no-cache-dir --upgrade pip

# Install Python dependencies
COPY requirements.txt /kick_interview_repo/
RUN python3.8 -m pip install --no-cache-dir -r requirements.txt
RUN python3.8 -m pip install uvicorn

# Copy local files into the working directory of the image
COPY crawler.py crawler_function.py etl_function.py fast_api.py /kick_interview_repo/
COPY data_base.db /kick_interview_repo/
COPY house_image/* /kick_interview_repo/house_image/

# Command to run the FastAPI service
CMD ["uvicorn", "fast_api:app", "--host", "0.0.0.0", "--port", "80"]


