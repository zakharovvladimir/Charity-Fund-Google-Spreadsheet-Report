# Charity Fund with Google Spreadsheet Report

## Application for Charity Fund + Google Spreadsheet Report

### Description 

The Foundation collects donations for various targeted projects: for medical care, for setting up pets colony in the basement, for food for abandoned pets - for any purpose related to the support of the feline population. + Opportunity to create reports to Google Spreadsheets.

### Techs

* python
* fastapi
* uvicorn
* SQLAlchemy
* alembic
* pydantic

### Install

`git clone https://github.com/zakharovvladimir/cat_charity_fund.git`<br>
`python -m venv venv`<br>
`source venv/Scripts/activate`

### How to use

`pip install -r requirements.txt`
`alembic upgrade head`
`uvicorn app.main:app --reload`<br>
Migrations: `alembic revision --autogenerate -m "Revision_2"`<br>
`127.0.0.1:8000`<br>
Docs:<br>
`127.0.0.1:8000/docs` - Swagger<br>
`127.0.0.1:8000/redoc` - ReDoc

### Google API Updates

Your Google account to .env:<br>
`EMAIL=yourgoogleaccount@gmail.com`<br>
<br>
Google Cloud Platform:<br>
Activate ```Google Drive API``` and ```Google Sheets API```<br>
Download and Add your JSON data from Google Cloud Platform (Template):<br>
```python
TYPE=''
PROJECT_ID=''
PRIVATE_KEY_ID=''
PRIVATE_KEY=''
CLIENT_EMAIL=''
CLIENT_ID=''
AUTH_URI=''
TOKEN_URI=''
AUTH_PROVIDER_X509_CERT_URL=''
CLIENT_X509_CERT_URL=''
```

### Author

Vladimir Zakharov // vladimir.zakharov.s@yandex.ru
