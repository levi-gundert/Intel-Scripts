#!/usr/bin/env python

__author__ = '@levigundert'
__version__ = ('0', '0', '1')

'''
Script for passing IP addresses to specific types of threat intelligence web applications when there is no corresponding API available.

Usage: python Submit_IP_List_No_API.py -i [primary (base) URI] -m [ToS URI] -u [user] -p [password]
-f [filename containing list of IP addresses] -t [number of seconds to wait between IP address queries]

The script returns a token value and an HTTP response code for each IP address submitted.

exempli gratia:
u'6MLiOuD7cNubddbPcUOSxX9rUuDrFf00PNicFryq'
u'sZQjGw5YdhXgLXK8Xoj4sENFbWEdZq1bczSfdWJR'
u'Ix2qcFiDdQVSTFz5EjPR3aKnK3MPUIDJq7ENboO8'
['5.43.221.133',
 <Response [200]>,
 '109.255.166.171',
 <Response [200]>,
 '92.143.182.177',
 <Response [200]>]
'''

#import sys
#sys.path.insert(0, "/usr/local/lib/python2.7/dist-packages")

import argparse
import time
from bs4 import BeautifulSoup
from pprint import pprint

import requests
#To disable SSL warnings in request's "vendored" urllib3 module
#Also try "pip install requests[security]"
requests.packages.urllib3.disable_warnings()


parser = argparse.ArgumentParser(description="script, file, and destination URI parameters" )
parser.add_argument('--base_uri', '-i', type=str, help="full destination URI path, i.e. 'https://levigundert.com/?query='", required=True)
parser.add_argument('--terms_uri', '-m', type=str, help="accept terms URI path, i.e. 'https://levigundert.com/accept_terms'", required=False)
parser.add_argument('--user', '-u', type=str, help= "account username", required=False)
parser.add_argument('--passw0rd', '-p', type=str, help= "account password", required=False)
parser.add_argument( '--filename', '-f', type=str, help="location of the input file", required=True)
parser.add_argument( '--t1me', '-t', type=int, help="number of seconds to wait between queries", required=False)
args = parser.parse_args()

global base_uri, terms_uri, user, passw0rd, filename, t1me
base_uri = args.base_uri
terms_uri = args.terms_uri
user = args.user
passw0rd = args.passw0rd
filename = args.filename
t1me = args.t1me


def openfile():
    with open(filename) as file:
        lines = file.read().splitlines()
        return lines


def http_request(lines):
    _result = []
    for x in lines:
        session = requests.Session()
        try_headers = {"Accept-Language": "en-US, en;q=0.5"}

        response = session.get(url=terms_uri, timeout=5, verify=False, headers=try_headers, auth=(user, passw0rd))
        soup = BeautifulSoup(response.content)
        form = soup.form
        token = form.find('input', attrs={'name':'_token'}).get('value')
        pprint(token)

        #value = session.post(url=terms_uri, verify=False, timeout=5, auth=(user,passw0rd), headers={'Authorization':token})

        time.sleep(t1me)

        r = session.get(url=base_uri + x, timeout=5, verify=False, auth=(user, passw0rd), headers={'Authorization':token})
        _result.extend((x, r))
        #_result.append(r)
    pprint(_result)


def main():
    test = openfile()
    http_request(test)


if __name__ == "__main__":
    main()
