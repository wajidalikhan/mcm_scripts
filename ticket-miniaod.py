import sys
import time
from collections import defaultdict
import pprint
import copy
import json

today = time.mktime( time.localtime() )
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import restful
mcm=restful(dev=False)

pwgs=mcm.get('/restapi/users/get_pwg')['results']

print pwgs

#Pair between
#chain_RunIIWinter15pLHE_flowRunIIWinter15pLHEtoGS_flowRunIISpring15DR74Startup25ns - RunIIMiniAODv2PLHE
#chain_RunIIWinter15wmLHE_flowRunIIWinter15wmLHEtoGS_flowRunIISpring15DR74Startup25ns - RunIIMiniAODv2WMLHE
#chain_RunIIWinter15GS_flowRunIISpring15DR74Startup25ns - RunIIMiniAODv2

collector=defaultdict(lambda : defaultdict( lambda : defaultdict( int )))
#for cc in ccs:
print 50*"-"
#print cc['prepid']
for pwg in pwgs:
    print "\t",pwg
        ## get all chains from that pwg in that chained campaign
        #crs = mcm.getA('chained_requests', query='member_of_campaign=%s&pwg=%s'%(cc['prepid'],pwg))
    crs = mcm.getA('chained_requests', query='member_of_campaign=%s&pwg=%s'%('chain_RunIIWinter15pLHE_flowRunIIWinter15pLHEtoGS_flowRunIISpring15DR74Startup25ns',pwg))  
    for cr in crs:
        root_id = cr['chain'][0]
        print "\t\t",root_id
        campaign = root_id.split('-')[1]
        collector[pwg][campaign][root_id]+=1

print "This is the list of %s requests that are deemed chainable for miniaod round 2"%(pwgs)
#pprint.pprint( dict(collector) )
print collector
all_ticket=[]
for pwg in pwgs:
    ## create a ticket for the correct chain
    #ccs = mcm.getA('chained_campaigns', query='contains=....')
    ccs = mcm.getA('chained_campaigns', query='alias=RunIIMiniAODv2PLHE')
    for cc in ccs:
        alias = cc['alias']
        root_campaign = cc['campaigns'][0][0]
        for repeat in range(10):
            requests_for_that_repeat = map(lambda i : i[0], filter(lambda i : i[1]==repeat, collector[pwg][root_campaign].items()))
            if not requests_for_that_repeat: continue
            print requests_for_that_repeat
            requests_for_that_repeat.sort()
            ## create a ticket with that content
            mccm_ticket = { 'prepid' : pwg, ## this is how one passes it in the first place
                            'pwg' : pwg,
                            'requests'  : requests_for_that_repeat,
                            'notes' : "Second round of miniaod in RunIISpring15MiniAODv2",
                            'chains' : [ alias ],
                            'repetitions' : repeat,
                            'block' : 3
                            }
            print mccm_ticket
            all_ticket.append( copy.deepcopy( mccm_ticket ) )
                            
## you'll be able to re-read all tickets from the created json
open('all_tickets.json','w').write(json.dumps( all_ticket))

all_ticket = json.loads(open('all_tickets.json').read())
for ticket in all_ticket:
    ### flip the switch
    #mcm.putA('mccms', ticket )
    #time.sleep(10)
    pass
