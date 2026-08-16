FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all the files into the container's working directory
COPY . .

# Install dependencies
RUN pip install -no-cache-dir --upgrade -r requirements.txt

# Define the command to start the application using Gunicorn with 4 worker processes
CMD ["gunicorn", "-w", "4",  "-b", "0.0.0.0:7860", "app:superkart_api"]
