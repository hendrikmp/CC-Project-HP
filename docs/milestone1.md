# Milestone 1 – Practice Repository and Project Definition

Project: BlaBlaTrip – Do Trips Together With Strangers  
Student: Hendrik Pauthner  
Email: pauthner@campus.tu-berlin.de  
Course: Cloud Computing: Fundamentos e Infraestructuras - 25/26  


## 1. Milestone Goals

- Set up the development environment and repository
- Use Git/GitHub following best practices
- Document all Milestone 1 steps
- Project definition


## 2. Git/GitHub Setup

The Git setup and all subsequent project development are carried out within WSL running Ubuntu 24.04.


1. **Check if git is installed**  
   ```bash
   git --version
   ````

2. **Configured Git**
    ```bash
    git config --global user.name "Hendrik Pauthner"
    git config --global user.email "pauthner@campus.tu-berlin.de"
    ```
3. **Created SSH key**
    ```bash
   ssh-keygen -t ed25519 -C "pauthner@campus.tu-berlin.de"
   ssh-add ~/.ssh/id_ed25519
   ```
   Upon key generation the public key `id_ed25519.pub` was uploaded to GitHub.  

4. **GitHub Profile Setup**
   - Name
   - Profile picture
   - Location
   - University
   - 2FA Setup  

## 3. Project Repository Setup

1. Creaded a new project Repository in Github (CC-Project-HP)
    - Added *README.md* as parent document for documentation
    - Added *LICENSE* (GNU General Public License v3.0)
    - Added *.gitignore*
    - Added /docs folder with *milestone1.md* for documentation of the first Milestone
2. Cloned Project Reppsitroy to my local system
```bash
    git clone git@github.com:hendrikmp/CC-Project-HP.git
```

## 4. Project Description

**Project Name:** 
BlaBlaTrip

**Problem:**  
Many people want to explore nature or visit remote places, but these destinations are often difficult or impossible to reach without a car. Meanwhile, drivers often travel with empty seats and could benefit from sharing trips and costs.

**Solution:**  
BlaBlaTrip is a web application that connects drivers planning day trips with passengers looking to join. Drivers can post upcoming trips (destination, start time, duration, available seats, and price per seat), while passengers can search for trips or create requests for desired destinations. For mutual trust, the plattform also allows users to rate both drivers and passengers.

**Technology (tentative):**
- API specification: Swagger
- Backend: Python Framework FastAPI or Flask
- Database: MongoDB or Cloud-hosted database (e.g. Firebase)
- App will later be deployed on a cloud platform such as Google Cloud


**Minimum Viable Product (MVP):**
- Display list of available trips
- Add new trip (driver posts details)
- Join a trip (passenger signs up for a listed trip)
- Add trip requests (for users without a car)
- Search trips by location or date

**Possible Extensions:**
- Basic rating system for drivers and passengers
- Payment integration for automatic cost sharing
- Chat or booking confirmation system
- Geolocation-based trip suggestions

**How BlaBlaTrip benefits from the Cloud**  
BlaBlaTrip is suited for a cloud environment because it requires centralized data access, scalability, and constant availability. Users need to search, post, and join trips in real time from different locations, which demands a shared, always-online backend.

