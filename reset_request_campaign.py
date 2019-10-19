import sys
import os
import argparse
import json
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import McM

"""
Setup argument parser

"""

parser = argparse.ArgumentParser(description="python reset_request.py -d 1 -pwg HIG -rc wmLHEGEN")
parser.add_argument("-d", "--dryrun",  default=1, help="dry run", type=int)
parser.add_argument("-v", "--verbosity",  default=0, help="Debug mode", type=int)
parser.add_argument("-f", "--field",  default="", help="", type=str)
parser.add_argument("-value", "--value",  default="", help="GS2021", type=str)
parser.add_argument("-pwg", "--pwg",  default= 'NONE', help = 'pwg', type = str)
parser.add_argument("-c", "--getcookies",  default=0, help="./getcookies", type=int)
parser.add_argument("-rc", "--rootcampaign",  default='', help="wmLHEGS, GS, pLHE",type = str)
parser.add_argument("-mix", "--mixing",  default='premix', help = 'classical, premixing',type = str)

args = parser.parse_args()

if len(sys.argv) <= 1:
  print('Usage: python reset_query.py -h')
  exit(1)

if (args.getcookies):
  cookies = './getcookie.sh'
  setenv  = './setenv.sh'
  os.system(cookies)
  os.system(setenv)

mcm = McM(dev=False)

_rootcampaign = ['wmLHEGEN','GEN','pLHE']
if (args.rootcampaign) not in _rootcampaign:
  print('Select the root campaign from : {}'.format(_rootcampaign))
  exit(0)


member_of_campaign ='RunIISummer19UL17'+args.rootcampaign

_pwg = ['JME','HIG','SUS','BPH','SMP','EXO','B2G','BTV','FSQ','MUO','EGM','TOP']

if args.pwg not in _pwg:
  print('No PWG selected, please select one: {}'.format(_pwg))
  exit(0)

else:
  requests = mcm.get('requests',query='member_of_campaign=%s&pwg=%s'%(member_of_campaign, args.pwg))
  for request in requests:
    print(request['prepid'])
    print('Reset : {} {}'.format(request['prepid'], mcm.approve('requests', request['prepid'], 0)))
    print('Option Reset : {} {} {}'.format(request['prepid'], mcm.get('requests', request['prepid'], method = 'option_reset'),'\n'))
  
  
  
  
  
  
  


