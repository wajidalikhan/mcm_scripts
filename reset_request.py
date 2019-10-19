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

#_mixing = ['premix','classical']
#if (args.mixing) not in _mixing:
#  print('Select PU mixing: {}'.format(_mixing))
#  exit(0)

#member_of_chain = ''
#if args.mixing not in _mixing:

member_of_chain ='chain_RunIISummer19UL17'+args.rootcampaign+'_flowRunIISummer19UL17SIM_flowRunIISummer19UL17DIGIPremix_flowRunIISummer19UL17HLT_flowRunIISummer19UL17RECO_flowRunIISummer19UL17MiniAOD_flowRunIISummer19UL17NanoAOD'

#member_of_chain ='chain_RunIISummer19UL17'+args.rootcampaign+'_flowRunIISummer19UL17SIM'
  
#elif args.mixing not in _mixing:
#member_of_chain ='chain_RunIISummer19UL17'+args.rootcampaign+'_flowRunIISummer19UL17SIM_flowRunIISummer19UL17DIGI_flowRunIISummer19UL17HLT_flowRunIISummer19UL17RECO_flowRunIISummer19UL17MiniAOD_flowRunIISummer19UL17NanoAOD'

_pwg = ['JME','HIG','SUS','BPH','SMP','EXO','B2G','BTV','FSQ','MUO','EGM','TOP']

if args.pwg not in _pwg:
  print('No PWG selected, please select one: {}'.format(_pwg))
  exit(0)

else:
  chained_requests = mcm.get('chained_requests',query='member_of_campaign=%s&pwg=%s'%(member_of_chain,args.pwg))
  for chained_request in chained_requests:
    #print(chained_request['chain'][0])
    for i in range(0, chained_request['step']):
      print('Rewinding {} {} {}'.format(chained_request['prepid'], mcm.get('chained_requests', chained_request['prepid'], method='rewind'),'\n'))
    
    print('Reset : {} {}'.format(chained_request['chain'][0], mcm.approve('requests', chained_request['chain'][0], 0)))
    print('Option Reset : {} {} {}'.format(chained_request['chain'][0], mcm.get('requests', chained_request['chain'][0], method = 'option_reset'),'\n'))
  
  
  
  
  
  
  


