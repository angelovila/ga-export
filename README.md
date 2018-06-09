# ga-export
google analytics api data  to spreadsheet



Running py file generate




How to run

1. Activate Google Analytics api and gather credentials - https://developers.google.com/analytics/devguides/reporting/ , https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py
2. Create creds.py file in the same folder as gaexport.py
3. creds.py should contain the following variables
  KEY_FILE_LOCATION #Google key file location
  SERVICE_ACCOUNT_EMAIL #account email
  STARTDATE #start date of data to pull
  ENDDATE #end date
4. run gaexport.py


Tweaks
get_report function contains what fields to pull
https://developers.google.com/analytics/devguides/reporting/core/v4/rest/v4/reports/batchGet#request-body
