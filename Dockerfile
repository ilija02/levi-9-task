# Use an official Python runtime as a parent image
FROM python:3.11-alpine


# Copy the current directory contents into the container at /app
COPY ./app /app

COPY requirements.txt /app/requirements.txt
# Set the working directory
WORKDIR /app

# Set nameservers
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf

# Accept a build argument for the port, with a default value of 8000
ARG PORT=8000

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the specified port
ENV PORT $PORT

# Make the specified port available to the world outside this container
EXPOSE $PORT

#Specify entrypoint
ENTRYPOINT [ "python" ]

# Run app.py when the container launches
CMD ["main.py"]
