#!/usr/bin/env python3
# Extend user access token

import argparse
from facepy import get_extended_access_token

argParser = argparse.ArgumentParser()
argParser.add_argument('--appid', required=True)
argParser.add_argument('--appsecret', required=True)
argParser.add_argument('--token', required=True)
args = argParser.parse_args()

print(get_extended_access_token(args.token, args.appid, args.appsecret)[0])

