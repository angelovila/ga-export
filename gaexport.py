"""Hello Analytics Reporting API V4."""

import argparse

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
VIEW_ID = creds.VIEW_ID

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
          'metrics': [{'expression': 'ga:sessions'}#,
                      #{'expression': 'ga:pageviews'},
                      #{'expression': 'ga:productDetailViews'},
                      #{'expression': 'ga:productAddsToCart'},
                      #{'expression': 'ga:productCheckouts'},
                      #{'expression': 'ga:uniquePurchases'},

                     ],
          'dimensions': [{'name':'ga:date'},
                         {'name':'ga:medium'}
                        ]
        }]
      }
  ).execute()


def print_response(response):
  """Parses and prints the Analytics Reporting API V4 response"""
  """
  a['data']['rows']   #returns a list of metrics and dimensions values
    example below only has date as dimensions
  [
  {u'metrics': [{u'values': [u'20535']}], u'dimensions': [u'20170408']},
  {u'metrics': [{u'values': [u'21403']}], u'dimensions': [u'20170409']},
  {u'metrics': [{u'values': [u'1350']}], u'dimensions': [u'20170410']}
  ]

    example below only has date as dimensions
    [
    {u'metrics': [{u'values': [u'4279']}], u'dimensions': [u'20170408', u'(none)']},
    {u'metrics': [{u'values': [u'140']}], u'dimensions': [u'20170408', u'(not set)']},
    {u'metrics': [{u'values': [u'2473']}], u'dimensions': [u'20170408', u'affiliate']}
    ]

  response['reports'][0]['columnHeader']  #returns the header
  {u'dimensions': [u'ga:date'],u'metricHeader': {u'metricHeaderEntries': [
      {u'type': u'INTEGER', u'name': u'ga:sessions'}
                                                                          ]
  }                                             }

  """

  """
  #ORIGINAL CODE
  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    rows = report.get('data', {}).get('rows', [])

    for row in rows:
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])

      for header, dimension in zip(dimensionHeaders, dimensions):
        print header + ': ' + dimension

      for i, values in enumerate(dateRangeValues):
        print 'Date range (' + str(i) + ')'
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          print metricHeader.get('name') + ': ' + value
  """
  for line in response['reports'][0]['data']['rows']:
      print 'date dimension', line['dimensions'][0]  #date dimension
      print 'medium dimension', line['dimensions'][1]  #medium
      print 'sessions metric', line['metrics'][0]['values'][0]  #sessions

def main():

  analytics = G.initialize_analyticsreporting()
  response = G.get_report(analytics)
  print_response(response)

if __name__ == '__main__':
  main()