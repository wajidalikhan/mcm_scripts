import sys
import json
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
print(sys.path.append)

#from rest import *
from rest import McM
mcm = McM(dev=True)

# example to edit a request parameter(-s) and save it back in McM

#__req_to_update = "HIG-Summer12-01257" # doesn't exists
__req_to_update = "B2G-Run3Summer19wmLHEGS-00001"
#__field_to_update = "time_event"
__field_to_update = "tags"

# get a the dictionnary of a request
req = mcm.get("requests", __req_to_update)

if "prepid" not in req:
    # in case the request doesn't exists there is nothing to update
    print("Request doesn't exist")
else:
    print("Request's '%s' BEFORE update: %s" % (__field_to_update, req[__field_to_update]))
#    print(json.dumps(req, indent=1))
    print(req[__field_to_update])

#    # modify what we want
#    # time_event is a list for each sequence step
    req[__field_to_update] = ['GSfor2021']
#
#    # push it back to McM
    answer = mcm.update('requests', req)
    print(answer)
#
    req2 = mcm.get("requests", __req_to_update)
    print("Request's '%s' AFTER update: %s" %(__field_to_update, req2[__field_to_update]))
