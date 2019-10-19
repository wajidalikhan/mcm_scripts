import sys
import time
from collections import defaultdict
import pprint
import copy
import json
import argparse 

sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import McM

"""
Setup argument parser

"""
parser = argparse.ArgumentParser(description="python SubmitNanoAODv5.py -rc wmLHEGS -pwg EXO -year 2018")
parser.add_argument("-r", "--request",  default='', help="B2G-Run3Summer19wmLHEGS-00013",type=str)
parser.add_argument("-rc", "--rootcampaign",  default='', help="wmLHEGS, GS, pLHE",type=str)
parser.add_argument("-d", "--dev",  default=1, help="dev=False/True",type=int)
parser.add_argument("-v", "--verbosity",  default=0, help="Debug mode", type=int)
parser.add_argument("-f", "--field",  default="", help="", type=str)
parser.add_argument("-value", "--value",  default = "", help = "GS2021", type = str)
parser.add_argument("-pwg", "--pwg",  default = 'TOP', help = 'TOP', type = str)
parser.add_argument("-y", "--year",  default = '2018', help = 'year of processing', type = str)
parser.add_argument("-c", "--getcookies",  default=0, help = "./getcookies", type = int)

args = parser.parse_args()

if len(sys.argv) <= 1:
  print('Usage: python SubmitNanoAODv5.py -h')
  exit(1)

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

# Global settings defining access to McM
cookie_file = ''


# Remember to use False first, to make sure that all tickets are creatable.
is_dry_run = False 
#use_dev_instance = False


if is_dry_run:
    print 'This is DRYRUN! No tickets will be created'
else:
    print 'WARNING!'*10
    print 'REAL QUERIES WILL BE MADE!!! Tickets will be created'
    print 'WARNING!'*10

#if use_dev_instance:
#    cookie_file = 'dev-cookie.txt'  #dev
#    print 'Running on dev instance!'
#else:
#    cookie_file = 'cookie.txt'      #prod
    print 'WARNING!'*10
    print 'Running on prod instance!!!'
    print 'WARNING!'*10

mcm = McM(dev=False, debug=True)

if args.year == '2018':
  campaign_name = "RunIIAutumn18MiniAOD"

elif args.year == '2017':
  campaign_name = 'RunIIFall17MiniAODv2'

elif args.year == '2016':
  campaign_name = 'RunIISummer16MiniAODv3'

N_REQUESTS_PER_TICKET = 30
PRIORITY_BLOCK = 1
TICKET_NOTE = 'NanoAODv5 submission: Request scanning based on ' + campaign_name 

campaigntochain = args.rootcampaign # 'wmLHEGS' # 'GS' # 'wmLHEGS' #'pLHE'

member_of_chain = ''

# Choose campaign types: #For wmLHEGS
if(campaigntochain == 'wmLHEGS'):
  if (args.year == '2018'): 
    dchain = 'chain_RunIIFall18wmLHEGS_flowRunIIAutumn18DRPremix_flowRunIIAutumn18MiniAOD_flowRunIIAutumn18NanoAODv5'
    member_of_chain = '*RunIIFall18wmLHEGS_flowRunIIAutumn18DRPremix*'
  
  elif (args.year == '2017'): 
    # chain_RunIIFall17wmLHEGS_flowRunIIFall17DRPremixPU2017_flowRunIIFall17MiniAODv2_flowRunIIFall17NanoAODv5
    # chain_RunIIFall17GS_flowRunIIFall17DRPremixPU2017_flowRunIIFall17MiniAODv2_flowRunIIFall17NanoAODv5
    # chain_RunIIFall17pLHE_flowRunIIFall17pLHE2GS_flowRunIIFall17DRPremixPU2017_flowRunIIFall17MiniAODv2_flowRunIIFall17NanoAODv5

    dchain = 'chain_RunIIFall17wmLHEGS_flowRunIIFall17DRPremixPU2017_flowRunIIFall17MiniAODv2_flowRunIIFall17NanoAODv5'
    member_of_chain = '*RunIIFall17wmLHEGS_flowRunIIFall17DRPremixPU2017*'
  
  elif (args.year == '2016'): 
    # chain_RunIISummer15wmLHEGS_flowRunIISummer16DR80PremixPUMoriond17_flowRunIISummer16MiniAODv3_flowRunIISummer16NanoAODv5
    # chain_RunIISummer15GS_flowRunIISummer16DR80PremixPUMoriond17_flowRunIISummer16MiniAODv3_flowRunIISummer16NanoAODv5
    # chain_RunIIWinter15pLHE_flowRunIIWinter15pLHEtoGS_flowRunIISummer16DR80PremixPUMoriond17_flowRunIISummer16MiniAODv3_flowRunIISummer16NanoAODv5

    dchain = 'chain_RunIISummer15wmLHEGS_flowRunIISummer16DR80PremixPUMoriond17_flowRunIISummer16MiniAODv3_flowRunIISummer16NanoAODv5'
    member_of_chain = '*RunIISummer15wmLHEGS_flowRunIISummer16DR80PremixPUMoriond17*'

elif (campaigntochain == 'GS'): #For GS
  if (args.year == '2018'): 
    dchain = 'chain_RunIIFall18GS_flowRunIIAutumn18DRPremix_flowRunIIAutumn18MiniAOD_flowRunIIAutumn18NanoAODv5'
    member_of_chain = 'chain_RunIIFall18GS_flowRunIIAutumn18DRPremix*'
  
  elif (args.year == '2017'): 
    dchain = 'chain_RunIIFall17GS_flowRunIIFall17DRPremixPU2017_flowRunIIFall17MiniAODv2_flowRunIIFall17NanoAODv5'
    member_of_chain = 'chain_RunIIFall17GS_flowRunIIFall17DRPremix'
  
  elif (args.year == '2016'): 
    dchain = ''
    member_of_chain = ''

elif (campaigntochain == 'pLHE'): #For pLHE
  if (args.year == '2018'): 
    dchain = 'chain_RunIIFall18pLHE_flowRunIIFall18GS_flowRunIIAutumn18DRPremix_flowRunIIAutumn18MiniAOD_flowRunIIAutumn18NanoAODv5'
    member_of_chain = '*RunIIFall18pLHE_flowRunIIFall18GS_flowRunIIAutumn18DRPremix*'
  
  elif (args.year == '2017'): 
    dchain = 'chain_RunIIFall17pLHE_flowRunIIFall17pLHE2GS_flowRunIIFall17DRPremixPU2017_flowRunIIFall17MiniAODv2_flowRunIIFall17NanoAODv5'
    member_of_chain = '*RunIIFall17pLHE_flowRunIIFall17pLHE2GS_flowRunIIFall17DRPremix*'
  
  elif (args.year == '2016'): 
    dchain = ''
    member_of_chain = ''

ticketfilename = dchain + '.json'
print 50*"-"

if (args.pwg) == 'all':
  listprep = ['JME','HIG','SUS','BPH','SMP','EXO','B2G','BTV','FSQ','MUO','EGM','TOP']

else:
  listprep = [args.pwg] 

print "This is the list of %s requests that are deemed chainable: " % (listprep)
all_tickets=[]


# Get requests that are member of given campaign
requests_for_that_repeat=[]

for pwg in listprep:
    page = 0
    requests = [{}]
    while len(requests) > 0:
        if(campaigntochain == 'wmLHEGS'):
            requests = mcm.get('requests', query='member_of_campaign=%s&pwg=%s&member_of_chain=%s' % (campaign_name, pwg, member_of_chain), page=page)
            page += 1

        elif(campaigntochain == 'GS'):
            requests = mcm.get('requests', query='member_of_campaign=%s&pwg=%s&member_of_chain=%s' % (campaign_name, pwg, member_of_chain), page=page)
            page += 1

        elif(campaigntochain == 'pLHE'):
            requests = mcm.get('requests', query='member_of_campaign=%s&pwg=%s&member_of_chain=%s' % (campaign_name, pwg, member_of_chain), page=page)
            page += 1

        # Iterate through results
        for req in requests:
            # Try to get total_events. Just in case, it's not there - return -1 and not crash
            total_events = req.get('total_events', -1)
            if total_events >= 1:
                print('\n')
                print('*INFO* Request ID: {}, Total Events: ({})'.format(req['prepid'], total_events))
                if ('MiniAOD' in req['prepid']):
                    chained_request_id = req['member_of_chain'][0]
                    print('*INFO* Chain: {}'.format(chained_request_id))
                    chained_requests = mcm.get('chained_requests', chained_request_id)
                    #-------------------------
                    if chained_requests is None:
                      print('')
                      print('Could not find %s' % (chained_request_id))
                    #-------------------------  
                    if len(chained_requests) < 3:
                      print('====> *ATTENTION* :', chained_requests)
                      print('Chain of %s is not long enough' % (chained_request_id))                                                    
                      continue 

                    if (campaigntochain == 'wmLHEGS' or campaigntochain == 'GS'):
                      print(chained_requests['chain'][0],chained_requests['chain'][1], chained_requests['chain'][2])
                      root_request = chained_requests['chain'][0]
                      dr_request = chained_requests['chain'][1]
                      mini_request = chained_requests['chain'][2]
                      do_chain = True

                      for i in range(1993, 2029):
                        suffix = str(i)
                        if (root_request == 'B2G-RunIISummer15wmLHEGS-0'+suffix):
                          chained_requests_for_root = mcm.get('chained_requests', query='contains=%s' % (root_request))
                          for chained_request_for_root in chained_requests_for_root:
                              if('NanoAODv5' in chained_request_for_root['prepid']):
                                  do_chain=False
                                  print 'CHAIN %s already existing' % (chained_request_for_root)
                                  break
                          if do_chain:
                              request_to_check = mcm.get('requests', root_request)
                              dr_request_to_check = mcm.get('requests', dr_request)
                              mini_request_to_check = mcm.get('requests', mini_request)
                              
                              if dr_request_to_check['keep_output'][1] == True and dr_request_to_check['status'] == 'done' and mini_request_to_check['status'] == 'done': 
                                  requests_for_that_repeat.append(root_request)
                                  print 'Added %s' % (root_request)
                    
                    if (campaigntochain == 'pLHE'):# To be fixed for pLHE campaign
                      try: 
                        if(args.verbosity):
                          print(chained_requests['chain'][0],chained_requests['chain'][1], chained_requests['chain'][2], chained_requests['chain'][2])

                        root_request = chained_requests['chain'][0]
                        dr_request = chained_requests['chain'][2]
                        mini_request = chained_requests['chain'][3]
                        do_chain = True
                      except IndexError:
                        print('====> *ATTENTION* : Either Root request {} or DR {} or MiniAOD {} request dose\'not exist'.format(root_request, dr_request,mini_request))
                        continue
                    
#                    chained_requests_for_root = mcm.get('chained_requests', query='contains=%s' % (root_request))
#                    for chained_request_for_root in chained_requests_for_root:
#                        if('NanoAODv5' in chained_request_for_root['prepid']):
#                            do_chain=False
#                            print 'CHAIN %s already existing' % (chained_request_for_root)
#                            break
#                    if do_chain:
#                        request_to_check = mcm.get('requests', root_request)
#                        dr_request_to_check = mcm.get('requests', dr_request)
#                        mini_request_to_check = mcm.get('requests', mini_request)
#                        
#                        if dr_request_to_check['keep_output'][1] == True and dr_request_to_check['status'] == 'done' and mini_request_to_check['status'] == 'done': 
#                            requests_for_that_repeat.append(root_request)
#                            print 'Added %s' % (root_request)
#
requests_for_that_repeat.sort()

for chunk in chunks(requests_for_that_repeat, N_REQUESTS_PER_TICKET):
    mccm_ticket = {'prepid': 'PPD',  
                   'pwg': 'PPD',
                   'requests': chunk,
                   'notes': TICKET_NOTE,
                   'chains': [str(dchain)],
                   'block': PRIORITY_BLOCK}
    all_tickets.append(mccm_ticket)

for ticket in all_tickets:
    print('Create ticket:\n%s' % (json.dumps(ticket, indent=4)))
    if not is_dry_run:
        res = mcm.put('mccms', ticket)
        ticket_prepid = res.get('prepid', None)
        print('Ticket prepid: %s' % (ticket_prepid))
        print('Generating and reserving requests...')
        res = mcm._McM__get('restapi/mccms/generate/%s/reserve/' % (ticket_prepid))
        #if res is not None:
        #    for ch_req in res.get('message'):
        #        print('Flow %s' % (ch_req['prepid']))
        #        flow_res = mcm.get('chained_requests', ch_req['prepid'], 'flow')
        #        print(flow_res)
        #        time.sleep(0.1)
        #else:
        #    print('Error generating and reserving for %s' % (ticket_prepid))

        time.sleep(0.2)
