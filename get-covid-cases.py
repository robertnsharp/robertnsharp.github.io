from datetime import datetime, timedelta
import requests
from google.cloud import storage

def handle_msg(event, context):

    # Get the data: we're assuming here that the URL isn't going to change
    print('Getting latest case data')
    url = 'https://data.nsw.gov.au/data/dataset/aefcde60-3b0c-4bc0-9af1-6fe652944ec2/resource/21304414-1ff1-4243-a5d2-f52778048b29/download/covid-19-cases-by-notification-date-and-postcode-local-health-district-and-local-government-area.csv'
    res = requests.get(url, stream=True)
    
    # check response was a 200: if not, bail out
    if res.status_code != requests.codes.ok:
        raise RuntimeError('Got bad status code ' + res.status_code)

    # Upload the data to google cloud storage
    client = storage.Client()
    bucket = client.get_bucket('www.covidnextdoor.com')
    blob = bucket.blob('cases.csv')
    # Stream raw file to GCS
    blob.upload_from_file(res.raw, content_type='text/csv')
    print('Upload complete')