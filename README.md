# How to Use the Dockerfile with Docker/Podman

## Steps

1. **Build the Docker Image**

   Open a terminal and navigate to the directory containing the Dockerfile. Run the following command to build the Docker image:

   ### Using Docker:
   ```sh
   docker build -t fastapi-ocr-service .
   ```

   ### Using Podman:
   ```sh
   podman build -t fastapi-ocr-service .
   ```

2. **Run the Docker Container**

   After the image is built, you can run a container using the following command:

   ### Using Docker:
   ```sh
   docker run -p 8000:8000 -v path/to/config.yaml:/config/config.yaml fastapi-ocr-service
   ```

   ### Using Podman:
   ```sh
   podman run -p 8000:8000 -v path/to/config.yaml:/config/config.yaml fastapi-ocr-service
   ```

3. **Access the FastAPI Application**

   Open your web browser and navigate to `http://localhost:8000` to access the FastAPI application.

4. **API Documentation**

   You can access the automatically generated API documentation at `http://localhost:8000/docs` or `http://localhost:8000/redoc`.