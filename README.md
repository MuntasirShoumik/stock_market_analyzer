# stock_market_analyzer


## Django Web Application:

This is a Django web application that allows users to analyze stock market data by visualizing in chars/graphs <br>
<a href ="https://stock-market-analyzer.onrender.com">Live link</a>
## Table of Contents
- [Features](#features)
- [Technologies used](#technologies-used)
- [Usage Instructions](#usage-instructions)
  - [Installation](#installation)
  - [Run the Development Server](#run-the-development-server)
  - [Access the Application](#access-the-application)
  


## Features

- User creation and authentication.
- Data table for doing CRUD on stock market data
- Data visualization
- chars/graphs customization

## Technologies used

  #### Frontend
       - HTML
       - CSS
       - Javascript
       - Jquery
       - bootstrap
  #### Backend
       - Django
       - PostgreSQL
       
## Usage Instructions

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/MuntasirShoumik/stock_market_analyzer
   

2. Go to the directory

3. Create and activate a virtual environment (optional):

   ```bash
   python -m venv venv
   venv/bin/activate

4. Install the required packages:
   
   ```bash
   pip install -r requirements.txt
   
5. Database migration

   #### Note: If want to use PostgreSQL or any other database then do the appropriate setup in the settings.py file. Or use the built-in SQLite by using the following commands:
   
   ```bash
   python manage.py makemigrations
   python manage.py migrate  

6. Create a supper user (optional):
   ```bash
   python manage.py createsuperuser

## Run the Development Server

   ```bash
   python manage.py runserver
   ```

## Access the Application
   
   ```bash
   http://localhost:8000/

