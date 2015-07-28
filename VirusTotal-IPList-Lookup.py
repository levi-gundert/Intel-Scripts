#!/usr/local/bin/env python

__author__ = '@levigundert'

'''

Query Virus Total for a list of IP addresses with required command line arguments
(API key and the input file - containing the IP address list separated by new line)
and optional command line arguments
(time value between API queries, specified in seconds).

Example:
./VirusTotal-IPList-Lookup.py -a [API Key] -f [IP Address file list location] -t [seconds]

'''

#import sys
#sys.path.insert(0, "/usr/local/lib/python2.7/dist-packages")

import requests
#To disable SSL warnings in request's "vendored" urllib3 module
#Also try "pip install requests[security]"
requests.packages.urllib3.disable_warnings()

import argparse
import time
from pprint import pprint
from collections import namedtuple

Version = namedtuple('Version', ['major', 'minor'])
version = Version(0, 1)


parser = argparse.ArgumentParser(description="parameters for passing a file to Virus Total")
parser.add_argument( '--api', '-a', type=str, help="enter VT API key")
parser.add_argument( '--filename', '-f', type=str, help="location of the input file containing line separated IP addresses", required=True)
parser.add_argument( '--t1me', '-t', type=int, help="number of seconds to wait between queries", required=False)
args = parser.parse_args()


global api, filename, t1me
api = args.api
filename = args.filename
t1me = args.t1me

with open(filename) as file:
    lines = file.read().splitlines()

_result = []
for x in lines:
    params = {'ip': x, 'apikey': api}
    response = requests.get('https://www.virustotal.com/vtapi/v2/ip-address/report', params=params)
    response_json = response.json()
    _result.extend((x, response_json))
    time.sleep(t1me)

pprint(_result)