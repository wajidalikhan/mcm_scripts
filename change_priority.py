# NEED this to be sourced before
# export PYTHONPATH=/afs/cern.ch/cms/PPD/PdmV/tools/wmcontrol:${PYTHONPATH}
# export PATH=/afs/cern.ch/cms/PPD/PdmV/tools/wmcontrol:${PATH}
# source /afs/cern.ch/cms/PPD/PdmV/tools/wmclient/current/etc/wmclient.sh

import os
import sys
import argparse

"""
Setup argument parser

"""

parser = argparse.ArgumentParser(description="python change_priority.py -rmin TOP-RunIIFall17MiniAODv2-00543 -rmax TOP-RunIIFall17MiniAODv2-00543 -p 10900 -v 0 -s 1")
parser.add_argument("-r", "--request",  default='', help="B2G-Run3Summer19wmLHEGS-00001",type = str)
parser.add_argument("-d", "--Dev",  default='True', help="dev=False/True",type=str)
parser.add_argument("-rmin", "--rmin",  default='', help="B2G-Run3Summer19wmLHEGS-00001",type = str)
parser.add_argument("-rmax", "--rmax",  default='', help="B2G-Run3Summer19wmLHEGS-00001",type = str)
parser.add_argument("-v", "--verbosity",  default=0, help="Debug mode", type = int)
parser.add_argument("-s", "--submit",  default=0, help="Submit", type = int)
parser.add_argument("-p", "--priority",  default=90000, help="Priority", type = int)

args = parser.parse_args()

if len(sys.argv) <= 1:
  print('e.g: python change_priority.py -rmin TOP-RunIIFall17MiniAODv2-00543 -rmax TOP-RunIIFall17MiniAODv2-00543 -p 10900 -v 0 -s 1') 
  print('Or: python change_priority.py -h')
  exit(1)

sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import McM

mcm = McM(dev=False)

requests = mcm.get_range_of_requests(args.rmin + ' -> ' + args.rmax)
#requests = mcm.get_range_of_requests('TOP-RunIIFall17MiniAODv2-00543 -> TOP-RunIIFall17MiniAODv2-00546')
#requests = mcm.get_range_of_requests(args.request)

print('Found %s requests' % (len(requests)))

for request in requests:
    if len(request['reqmgr_name']) > 0:
      if args.verbosity:
        result = os.system("echo 'wmpriority.py %s %s'" % (request['reqmgr_name'][-1]['name'], args.priority))
      if args.submit:
        result = os.system("wmpriority.py %s %s" % (request['reqmgr_name'][-1]['name'], args.priority))
        if result != 0:
            print('Change of priority failed for: %s. Exit code: %s' % (request['prepid'], result))
    else:
        print('Workflow is not registered for %s' % (request['prepid']))
