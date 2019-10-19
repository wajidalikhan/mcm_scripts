import sys
import os
import argparse
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import McM

"""
Setup argument parser

"""

parser = argparse.ArgumentParser(description="python sub_query.py -d 0 -s 1 -f ppd_tags -value ULPOG17 -pwg BTV -status submitted")
parser.add_argument("-s", "--submit",  default=0, help="submit/execute",type=int)
#parser.add_argument("-d", "--dryrun",  default=1, help="dry run", type=int)
parser.add_argument("-d", "--dev",  default=1, help="dev=False/True",type=int)
parser.add_argument("-status", "--status",  default='NONE', help="new,defined,submitted,done",type=str)
parser.add_argument("-v", "--verbosity",  default=0, help="Debug mode", type=int)
parser.add_argument("-f", "--field",  default="", help="", type=str)
parser.add_argument("-value", "--value",  default="", help="GS2021", type=str)
parser.add_argument("-c", "--getcookies",  default=0, help="./getcookies", type=int)
parser.add_argument("-pwg", "--pwg",  default= 'NONE', help = 'pwg', type = str)

args = parser.parse_args()

if len(sys.argv) <= 1:
  print('Usage: python sub_query.py -h')
  exit(1)

if (args.getcookies):
  cookies = './getcookie.sh'
  setenv  = './setenv.sh'
  os.system(cookies)
  os.system(setenv)

mcm = McM(dev=False)

_pwg = ['JME','HIG','SUS','BPH','SMP','EXO','B2G','BTV','FSQ','MUO','EGM','TOP']

allRequests = mcm.get('requests',query='member_of_campaign=RunIISummer19UL17MiniAOD&status='+args.status+'&pwg='+args.pwg)

#allRequests = mcm.get('requests',query='member_of_campaign=RunIISummer19UL17MiniAOD&status=submitted&pwg=HIG')
#allRequests = mcm.get('requests',query='tags=Run3HighSigmaZSimBS')

for r in allRequests:
  print(r['prepid'],r['member_of_chain'])

  if(args.dev):
    print('python ps_request.py -r '+ r['prepid'] +' -f '+ args.field +' -value '+ args.value +' -v 0 -c '+ str(args.getcookies) +' -d '+ str(args.dev) +'')

  elif(args.submit):
    cmd = 'python ps_request.py -r '+ r['prepid'] +' -f '+ args.field +' -value '+ args.value +' -v 0 -c 0 -d '+ str(args.dev) +''
    print(cmd)
    os.system(cmd)
