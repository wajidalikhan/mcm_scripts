#!/bin/bash

export PYTHONPATH=/afs/cern.ch/cms/PPD/PdmV/tools/wmcontrol:${PYTHONPATH}
export PATH=/afs/cern.ch/cms/PPD/PdmV/tools/wmcontrol:${PATH}
source /afs/cern.ch/cms/PPD/PdmV/tools/wmclient/current/etc/wmclient.sh
voms-proxy-init -voms cms
export X509_USER_PROXY=$(voms-proxy-info --path)
