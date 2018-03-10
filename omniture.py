import config
import uuid
from datetime import datetime
import hashlib
import binascii
import requests
import json
from time import sleep


class Omniture:

    def __init__(self):
        self.username = config.username
        self.sharedsecret = config.sharedsecret


    @staticmethod
    def _construct_header(properties):
        header = []
        for key, value in properties.items():
            header.append('{key}="{value}"'.format(key=key, value=value))
        return ', '.join(header)

    def _create_token(self):
        nonce = str(uuid.uuid4())
        base64nonce = binascii.b2a_base64(binascii.a2b_qp(nonce))
        created_date = datetime.utcnow().isoformat() + 'Z'
        sha = nonce + created_date + self.sharedsecret
        sha_object = hashlib.sha1(sha.encode())
        password_64 = binascii.b2a_base64(sha_object.digest())

        wsse_values = {
            "Username": self.username,
            "PasswordDigest": password_64.decode().strip(),
            "Nonce": base64nonce.decode().strip(),
            "Created": created_date,
        }
        header = 'UsernameToken ' + self._construct_header(wsse_values)

        return {'X-WSSE': header}

    def get_endpoint(self):
        url = "https://api3.omniture.com/admin/1.4/rest/?method=Company.GetEndpoint"
        headers = self._create_token()
        body = {
            "company": "Philips"
        }

        try:
            response = requests.request("POST", url, data=body, headers=headers)
            url = json.loads(response.text)
            return url
        except Exception as e:
            logging.debug(str(e))
            raise Exception("An error occured while requesting Get Endpoints")

    def get_queue(self, query_body):
        url = self.get_endpoint() + "?method=Report.Queue"
        headers = self._create_token()
        body = query_body
        try:
            response = requests.request("POST", url, data=body, headers=headers)
            jsonfile = json.loads(response.text)
            return jsonfile["reportID"]
        except Exception as e:
            logging.debug(str(e))
            raise Exception("An error occured while requesting queing a job")

    # To fetch the report using the queue created
    # Retires for 50 times with 10sec sleep each [50 * 10]
    def get_result(self, reportid, retry_count=50):
        url = self.get_endpoint() + "?method=Report.Get"
        status = 400
        retries = 0
        body = {
            "reportID": int(reportid)
        }

        while status != 200 or retries != retry_count:
            try:
                headers = self._create_token()
                response = requests.request("POST", url, data=body, headers=headers)
                status = response.status_code
                if status == 200:
                    return response
                else:
                    jsonfile = json.loads(response.text)
                    logging.debug(jsonfile['error_description'])
                    sleep(10)
                    retries += 1
            except Exception as e:
                logging.debug(str(e))
                raise Exception("An error occured while fetching a report")

# ClassObj = Omniture()
# ClassObj.get_endpoint()
