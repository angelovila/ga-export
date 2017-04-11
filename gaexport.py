"""Hello Analytics Reporting API V4."""

import argparse
import csv

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools

import creds  #credentials file

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
KEY_FILE_LOCATION = creds.KEY_FILE_LOCATION
SERVICE_ACCOUNT_EMAIL = creds.SERVICE_ACCOUNT_EMAIL
VIEW_ID = str(creds.VIEW_ID)

#date format should be 'YYYY-MM-DD' in str
STARTDATE = '2017-04-08'
ENDDATE = '2017-04-10'


def initialize_analyticsreporting():
  """Initializes an analyticsreporting service object.

  Returns:
    analytics an authorized analyticsreporting service object.
  """

  credentials = ServiceAccountCredentials.from_p12_keyfile(
    SERVICE_ACCOUNT_EMAIL, KEY_FILE_LOCATION, scopes=SCOPES)

  http = credentials.authorize(httplib2.Http())

  # Build the service object.
  analytics = build('analytics', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URI)

  return analytics


def get_report(analytics):
  # Use the Analytics Service Object to query the Analytics Reporting API V4.
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': STARTDATE, 'endDate': ENDDATE}],
          'metrics': [{'expression': 'ga:sessions'},
                      {'expression': 'ga:pageviews'},
                      {'expression': 'ga:productDetailViews'},
                      {'expression': 'ga:productAddsToCart'},
                      {'expression': 'ga:productCheckouts'},
                      {'expression': 'ga:uniquePurchases'},

                     ],
          'dimensions': [{'name':'ga:date'},
                         {'name':'ga:medium'},
                         {'name':'ga:userType'},
                         {'name':'ga:deviceCategory'}
                        ]
        }]
      }
  ).execute()


def print_response(response, filename='export.csv'):
  """
  write to csv file
  """
  """
  response['reports'][0]['data']['rows']   #returns a list of metrics and dimensions values
  [
  {u'metrics': [{u'values': [u'1446', u'4592', u'891', u'249', u'195', u'61']}], u'dimensions': [u'20170408', u'(none)', u'New Visitor', u'desktop']},
  {u'metrics': [{u'values': [u'162', u'543', u'206', u'5', u'5', u'0']}], u'dimensions': [u'20170409', u'referral', u'New Visitor', u'desktop']},
  {u'metrics': [{u'values': [u'1', u'1', u'1', u'0', u'0', u'0']}], u'dimensions': [u'20170408', u'display', u'Returning Visitor', u'desktop']}

  ]


  response['reports'][0]['columnHeader']  #returns the header
  {u'dimensions': [
                   u'ga:date',
                   u'ga:medium',
                   u'ga:userType',
                   u'ga:deviceCategory'
                  ],
   u'metricHeader': {u'metricHeaderEntries': [
                                              {u'type': u'INTEGER', u'name': u'ga:sessions'},
                                              {u'type': u'INTEGER', u'name': u'ga:pageviews'},
                                              {u'type': u'INTEGER', u'name': u'ga:productDetailViews'},
                                              {u'type': u'INTEGER', u'name': u'ga:productAddsToCart'},
                                              {u'type': u'INTEGER', u'name': u'ga:productCheckouts'},
                                              {u'type': u'INTEGER', u'name': u'ga:uniquePurchases'}]}}

  """
  #write in csv
  with open(filename, 'wb') as csvfile:
    writer = csv.writer(csvfile,
                        delimiter=',',
                        quoting=csv.QUOTE_MINIMAL
                        )
    writer.writerow(['date',
                     'medium',
                     'userType',
                     'deviceCategory',
                     'sessions',
                     'pageviews',
                     'productDetailViews',
                     'productAddToCart',
                     'productCheckouts',
                     'uniquePurchases'
                   ])
    for line in response['reports'][0]['data']['rows']:
      date = str(line['dimensions'][0])
      medium = str(line['dimensions'][1])
      userType = str(line['dimensions'][2])
      deviceCategory = str(line['dimensions'][3])
      sessions = str(line['metrics'][0]['values'][0])
      pageviews = str(line['metrics'][0]['values'][1])
      productDetailViews = str(line['metrics'][0]['values'][2])
      productAddsToCart = str(line['metrics'][0]['values'][3])
      productCheckouts = str(line['metrics'][0]['values'][4])
      uniquePurchases = str(line['metrics'][0]['values'][5])

      writer.writerow([date,
                       medium,
                       userType,
                       deviceCategory,
                       sessions,
                       pageviews,
                       productDetailViews,
                       productAddsToCart,
                       productCheckouts,
                       uniquePurchases
                       ])

def main():

  analytics = initialize_analyticsreporting()
  response = get_report(analytics)
  print_response(response)

if __name__ == '__main__':
  main()