# JOBFUL - Job Scraper and API

## Overview
**JOBFUL** is a backend Python web scraper that collects job listings from various websites (JobBank, Indeed, LinkedIn) and stores them in a list. Using **FASTAPI**, the collected data is made available to users via API endpoints, allowing them to query job listings based on their desired skill, location, and page number.

## Features
- Scrapes job postings from multiple websites: JobBank, Indeed, and LinkedIn.
- Exposes multiple API endpoints to retrieve job listings.
- Users can specify a job skill, location, and page number to filter job results.
- Real-time job listings delivered to users via API.


## API Endpoints
### `GET /`
- **Description**: Returns a simple greeting message.
- 
## `DEPRECATED`
    ### `POST /jobank/get/`
    - **Description**: Retrieves job listings from JobBank.

    ### `POST /indeed/get`
    - **Description**:  Retrieves job listings from Indeed.
 
### `POST/linkdin/get`
- **Description**:Retrieves job listings from LinkedIn.


 

## Setup & Installation
### Prerequisites
Ensure you have the following installed:

    Python 3.x
    pip (Python package installer)

### Installation Steps

### Clone this repository:

    git clone https://github.com/gursimrangillnotinsane/webscrapper.git

### Install dependencies:

    cd webscrapper
    pip install -r requirements.txt

### Run the FastAPI server:

    uvicorn app.main:app --reload

Access the API at: http://127.0.0.1:8000

## Technologies Used

    Python 3.x
    FASTAPI for API development
    BeautifulSoup and requests for web scraping
    Pydantic for data validation
