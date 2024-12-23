# Use an official Python image as the base
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /web_app

# Copy the current directory's content into the container
COPY . /web_app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Just tells which port the app will listen on (information purpose, doesnt map anything)
EXPOSE 7777

# Command to run the application
CMD ["python3", "app.py"]
