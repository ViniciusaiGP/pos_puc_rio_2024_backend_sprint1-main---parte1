FROM ubuntu:latest

# Install Python and pip
RUN apt update && \
    apt install -y python3 python3-pip python3-venv

# Create a working directory
WORKDIR /app

# Copy the requirements file first to leverage Docker caching
COPY requirements.txt .

# Create a virtual environment and install dependencies
RUN python3 -m venv venv && \
    ./venv/bin/pip install -r requirements.txt

# Copy the rest of your application code
COPY . .
EXPOSE 5000
# Set the entry point for your application
CMD ["./venv/bin/python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
