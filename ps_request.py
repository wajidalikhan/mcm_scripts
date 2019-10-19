import sys
import os 
import argparse
import json

sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import McM

"""
Setup argument parser

"""
parser = argparse.ArgumentParser(description="python ps_request.py -r B2G-Run3Summer19wmLHEGS-00013 -f process_string -value sigmZ5p7 -v 0 -c 0 -d 1")
parser.add_argument("-r", "--request",  default='', help="B2G-Run3Summer19wmLHEGS-00013",type=str)
parser.add_argument("-d", "--dev",  default=1, help="dev=False/True",type=int)
parser.add_argument("-v", "--verbosity",  default=0, help="Debug mode", type=int)
parser.add_argument("-f", "--field",  default="", help="", type=str)
parser.add_argument("-value", "--value",  default="", help="GS2021", type=str)
parser.add_argument("-c", "--getcookies",  default=0, help="./getcookies", type=int)

args = parser.parse_args()

if len(sys.argv) <= 1:
  print('Usage: python ps_request.py -h')
  exit(1)

if (args.getcookies):
  cookies = './getcookie.sh'
  setenv  = './setenv.sh'
  os.system(cookies)
  os.system(setenv)

if(args.dev):
  mcm = McM(dev=True)
  print("="*80) 
  print('Working on McM Development instance: {}'.format(args.dev))
  print("Get the McM Cookies and set the Grid Env: -c 1,  By default set to none: -c 0")
  print("="*80) 
else:
  mcm = McM(dev=False)
  print("="*80) 
  print('Working on McM Production instance: {}'.format(1+args.dev))
  print("Get the McM Cookies and set the Grid Env: -c 1,  By default set to none: -c 0")
  print("="*80) 

reqToUpdate = args.request 
fieldToUpdate = args.field

# Get a dictionnary of a request
req = mcm.get("requests", reqToUpdate)

if "prepid" not in req:
    print("Request doesn't exist")

else:
    print("Request: {}, field: {}, BEFORE Update: '{}'".format(args.request, args.field, req[args.field])) 
    if (args.verbosity):
      print(json.dumps(req, indent=1))
      print(req[fieldToUpdate])

    # Modify the field
    if(args.field == 'process_string'):
      req[fieldToUpdate] = args.value
    
    elif (args.field == 'tags'):
      req[fieldToUpdate] = [args.value]

    elif (args.field) == 'ppd_tags':
      req[fieldToUpdate] = [args.value]

    # Push the changes back to McM
    answer = mcm.update('requests', req)

    req2 = mcm.get("requests", reqToUpdate)
    print("Request: {}, field: {}, AFTER Update: '{}'".format(args.request, args.field, req[args.field])) 
