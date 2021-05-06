import requests
import sys
import time


class MetaDefenderApi:

    def __init__(self):

        self.api_key = 'YOUR API KEY'
        self.base_url = 'https://api.metadefender.com/v4/'

    # check if file with hash_value is previously scanned
    def hash_lookup(self, hash_value):

        # hash look up to retrieve scan report
        url = self.base_url + 'hash/' + hash_value
        header = {'apikey': self.api_key}
        response = requests.get(url, headers=header)

        # if hash was not found, return False
        if response.status_code == 404:
            return False
        # if error, exit
        elif response.status_code != 200:
            self.error_check(response.status_code)

        scan_report = response.json()

        return scan_report

    # upload new file to meta defender to scan and return data_id
    def upload_file(self, file_name):

        # upload file
        url = self.base_url + 'file'
        file = open(file_name, "rb")
        headers = {'apikey': self.api_key,
                   'content-type': 'application/octet-stream',
                   'filename': file_name}
        response = requests.post(url, headers=headers, data=file)

        # if error, exit
        if response.status_code != 200:
            self.error_check(response.status_code)

        # retrieve and return data_id
        data_id = response.json()['data_id']
        return data_id

    # retrieve scan report using data_id
    def retrieve_scan_report(self, data_id):

        print("\nWaiting for scan report...")

        url = self.base_url + 'file/' + data_id
        headers = {'apikey': self.api_key}

        # timer to keep track of time, if scan not complete after 5 min (300 seconds) -> exit
        start_time = time.time()
        current_time = time.time()

        # retrieve scan report and if progress < 100 try again for 5 min
        while current_time-start_time <= 300.0:
            # retrieve scan report
            response = requests.get(url, headers=headers)

            # if error, exit
            if response.status_code != 200:
                self.error_check(response.status_code)

            scan_report = response.json()
            # return scan report if progress is 100 else continue
            if scan_report['scan_results']['progress_percentage'] == 100:
                return scan_report

            time.sleep(5)
            current_time = time.time()

        print("Scan still in progress, please try after few minutes")
        sys.exit(1)

    def error_check(self, status_code):

        print("Error code:", status_code)

        if status_code == 400:
            print("Bad Request, There was a client error")
        elif status_code == 401:
            print("Authentication failed")
        elif status_code == 404:
            print("Endpoint/entity was not found")
        elif status_code == 405:
            print("Method Not Allowed, CORS configuration missing")
        elif status_code == 406:
            print("Payload type is not accepted")
        elif status_code == 408:
            print("Request Timeout, The request was over 60 seconds")
        elif status_code == 429:
            print("Rate limit exceeded or too many requests per second")
        elif status_code >= 500:
            print("Server Error")

        sys.exit(1)
