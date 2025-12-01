# BlaBlaTrip

Project: BlaBlaTrip – Do Trips Together With Strangers  
Student: Hendrik Pauthner  
Email: pauthner@campus.tu-berlin.de  
Course: Cloud Computing: Fundamentos e Infraestructuras - 25/26

## Project Description:

**BlaBlaTrip** is a web application that connects drivers planning day trips with passengers looking to join. It helps people reach natural or remote destinations that are difficult to access without a car.  

Users will be able to search and request trips, post their own ones, and rate drivers as well as passengers they shared a trip with.

## Project Milestones / Documentation

The links of the project milestones and their respective documentation can be accessed below:

### [Milestone 1 – Practice Repository and Project Definition](docs/milestone1.md)

### [Milestone 2 – Continuous Integration](docs/milestone2.md)

### [Milestone 3 – Microservices Desgin](docs/milestone3.md)

### [Milestone 4 – Service Composition](docs/milestone4.md)

## Repository Structure
```
BlaBlaTrip/
├── .github/
|   └── workflows
|       └── python-app.yml
├── docs/
|   ├── milestone1.md
|   └── ...
├── logs/
├── shared/
|   └── Shared Logging Configuration
├── src/
|   ├── Business Logic / API / Application Layer ..
|   └── ...
├── tests/
|   ├── integration/ ...
|   └── unit/ ...
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── Makefile
├── README.md
└── requirements.txt
```


## How to Run the Application

### Prerequisites
- **Docker** and **Docker Compose** installed on your system.


### Running with Docker Compose

1. Build and start the application:  

   ```bash
   docker compose up --build -d
   ```
2. The Frontend will be available at http://localhost:3000. 
3. The Trips Service will be available at http://localhost:5001.  
To verify the application is running, visit the health check endpoint: http://localhost:5001/health
4. API Specification available at http://localhost:5001/openapi/swagger
5. To stop the application:

    ```bash
    docker compose down
    ```

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

