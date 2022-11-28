FROM python:3.10
EXPOSE 8000 
WORKDIR /app 
# Copy requirements from host, to docker container in /app 
COPY ./requirements.txt .
# Copy everything from ./src directory to /app in the container
COPY ./app . 
RUN pip install -r requirements.txt 
# Run the application in the port 8000
CMD ["python", "-m", "uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app"]