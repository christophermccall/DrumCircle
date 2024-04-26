# Set base image (host OS)
FROM python:3.12-alpine

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /home/ubuntu/pyprojects/DrumCircle/circle

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN	sudo install mysql-client pkg-config
RUN	sudo apt-get install default-libmysqlclient-dev
RUN sudo apt-get install pkg-config build-essential libmysqlclient-dev
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY  app.py .

# Specify the command to run on container start
CMD [ "python3", "./drum.py" ]