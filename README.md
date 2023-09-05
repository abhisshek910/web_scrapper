# Real Estate Data Web Scraping and API Project

This project demonstrates how to scrape real estate data from a government website, process the data, store it in a PostgreSQL database, and create a Flask API for data retrieval.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Note](#note)
- [Submitted By](#submission)


## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your system.
- PostgreSQL database set up with the necessary credentials.
- Required Python packages installed (see `requirements.txt`).

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/abhisshek910/web_scrapper.git
   cd web-scrapper

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt

   ```
3. Open web_scrapper.py and fill the below details with your credentials

    ```bash
    conn = psycopg2.connect(
    database="Web Scrapper",
    user="postgres",
    password="Abhi1234@5",
    host="localhost",
    port="5433",
   ) 
    ```

## Usage
1. Run the web scraper to collect real estate data and store in postgresql:

    ```bash
    python web_scrapper.py

    ```
2. Open the flask_api.py and here also set your database credentials

3. Now Start the Flask API to serve data:

    ```bash
    python flask_api.py

    ```

## API Endpoints

- `/api/by_doc_no/<doc_no>`: Search data by Document No.
- `/api/by_year/<year>`: Search data by Year of Registration.


## Note

1.  From line 59 to 65 in web_scrapper.py is code to automate captcha.If it does not works properly comment out the code and write captcha manually

2. Also after getting all the 50 records click on the extension superb-copy and enable it to translate the data into english

3. After the extension is enabled right click on the web page and translate the data to english manually and scroll down to end of the page. There is wait time of 50 secs to perform all these task

## Submitted By

These assignment is submitted by Abhishek Agrawal.