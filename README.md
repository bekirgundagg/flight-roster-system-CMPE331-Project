# HvB Flight Roster System ✈️

This project is a web-based system designed to prepare and manage flight rosters for an imaginary airline. The system acts as a central platform (Main System) that aggregates data from four different service providers: Flight Information, Flight Crew (Pilots), Cabin Crew, and Passenger Information.

## 🚀 Project Overview

The HvB Flight Roster System provides a dashboard to manage flight operations efficiently. The core functionalities include:

* **Data Integration:** Combines data from four distinct APIs to generate a complete roster.
* **Visualization Views:**
    * **Tabular View:** A summary table displaying the name, type, and ID of all people on board.
    * **Plane View:** A visual seat plan allowing users to hover over seats to see passenger/crew details.
    * **Extended View:** Detailed tables separated by person type (Flight Crew, Cabin Crew, Passengers).
* **Roster Generation:** Supports both automatic and manual assignment of pilots and cabin crew based on constraints (e.g., vehicle type, seniority).
* **Passenger Management:** Handles seat assignments and links infant passengers (ages 0-2) to their parents.
* **Chef & Menu Integration:** Automatically selects random recipes from the assigned Chef's repertoire to add to the flight menu.

## 🛠 Installation & Setup

Follow the steps below to set up the project on your local machine.

### Prerequisites
* Python 3.x
* MySQL Server
* Git

### 1. Clone the Repository
Open your terminal and clone the project:
```bash
git clone https://github.com/bekirgundagg/flight-roster-system-CMPE331-Project
```
### 2) Create a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3) Install Dependencies
```bash
pip install -r requirements.txt
```

### 4) MySQL Database Setup

	1.	Connect to your MySQL server using MySQL Workbench or CLI.
	2.	Create a new empty database (example: hvb_db).
```bash
CREATE DATABASE hvb_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
### 5) Configure Environment Variables (.env)

Create a .env file in the root directory. This file stores sensitive settings like database credentials and Django secret keys.

Copy the template below and update DB_NAME, DB_USER, and DB_PASSWORD according to your local MySQL setup:

```bash
# Django Secret Key
SECRET_KEY=django-insecure-your-secret-key-here

# Debug Mode (Set to True for development)
DEBUG=True

# Database Configuration
DB_NAME=hvb_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

### 6) Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7) Load Mock Data (Optional but Recommended)

This populates the database with sample flights, crew, and passengers for testing:
```bash
python manage.py load_all_data
```

### 8) Run the Backend
```bash
python manage.py runserver
```
Backend will be available at: http://127.0.0.1:8000/
### 9) Run the Frontend
```bash
npm run dev
```
Frontend will be available at the URL shown in your terminal (commonly http://localhost:5173/).