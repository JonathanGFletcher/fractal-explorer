# fractal-explorer

![demo.png](./assets/demo.png)

## Architecture
- Docker Compose
- Nginx Reverse Proxy
- Python FastAPI Web Server
- React Web Client

## Features
- Asyncronous/concurrent fractal rendering in client
- Image caching using Docker volumes

## Run the Application

### Requirements
- Nvidia CUDA GPU with Compute Capability 3.0 or higher (required by CuPy)
- Docker with rootless access configured
- Nvidia Container Toolkit
- Developed and tested on Ubuntu 22.04 LTS with Nvidia drivers installed
- Program runs on WSL with Ubuntu-WSL Nvidia drivers installed

### Development
To run the application in development mode, use command `make dev`. This will host the web server with live reload using uvicorn, and will host the web client with live reload using Webpack dev server. Any changes made to the web client or web server while the application is running will be automatically included. Entrypoint to the application is `localhost:80`.

### Production
To run the application in production mode, use command `make run`. This will compile the web client into static files and will run the web server in production mode. Nginx hosts the web client files and directs server requests appropriately. Entrypoint to the application is `localhost:80`.
