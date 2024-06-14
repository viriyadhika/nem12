# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./backend /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for Gunicorn
EXPOSE 5000

# Start a dev server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]