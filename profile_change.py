print ('KFDevMS-01 v0.06 \n')

import os
import json
import sys
import requests
import urllib
import urlparse
import getpass

cert ='cacert.pem'
os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(os.getcwd(), cert)

client_id = '6f65012d3a97a1017c679103f8469322'
profile_id = '31637360'
user = 'wouter@yargon.nl'
pasw = 'yargon!@#$%'
verbose = 'y'

HOST = 'https://app.klipfolio.com/api/1'
##31637360
##user = raw_input('Username > ')
##pasw = getpass.getpass('Password > ')
##client_id = raw_input('Client ID > ')
##profile_id = raw_input('Profile ID > ')
##verbose = raw_input('Verbose (slow) [y/n] > ')

def parse_url(x, pid):
    y = urlparse.urlparse(x)
    z = urlparse.parse_qsl(y.query)
    for n,key in enumerate(z):
        if key[0] == 'ids':
            lst = list(key)
            lst[1] = 'ga:' + pid
            key = tuple(lst)
            z[n] = key
    q = urllib.unquote(urllib.urlencode(z))
    new_url = urlparse.ParseResult(scheme=y.scheme, netloc=y.netloc, path=y.path, query=q, fragment=y.fragment, params=y.params)
    new_url = urlparse.urlunparse(new_url)
    return new_url

def get(req, host = HOST):
    res = requests.get(host+req, auth=(user,pasw), verify=False)  
    return res.json()

def put(req, data, headers, host=HOST):
    res = requests.put(host+req, auth=(user, pasw), data=json.dumps(data),headers=headers, verify=False )
    return res.json()
            
def post(req, host=HOST):
    res = requests.post(host+req, auth=(user,pasw), verify=False)  
    return res.json()

def pretty_print_json(data):
    print ((json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '))))
    return;

print ('Retrieving datasources for ' + client_id + ' ...')
b = get(req='/datasources?client_id=' + client_id )

if b['meta']['success'] == True and b['meta']['status'] == 200:
    a = b['data']['datasources']
    print ('Changing profile IDs to ' + profile_id + ' ...')
    for i in a:
        ds = get(req='/datasources/'+i['id']+'?full=true')
        if ds['data']['connector'] == 'google_analytics' :
            
            try:
                x = ds['data']['properties']['advancedQuery']
                y = ds['data']['properties']['endpoint_url']
            except KeyError:
                break;
            
            advanced_query = parse_url(x, profile_id)
            endpoint_url = parse_url(y, profile_id)
            
            payload = {'properties': {'profile': profile_id, 'advancedQuery': advanced_query, 'endpoint_url': endpoint_url}}
            headers = {'content-type':'application/json'}
            r = put (req='/datasources/'+i['id']+'/properties', data=payload, headers=headers )

            if verbose == 'y':
                print('*******************************************************************************************')
                pretty_print_json(get(req='/datasources/' + i['id'] + '?full=true'))
                pretty_print_json(post(req='/datasources/'+i['id'] +'/@/refresh'))
                print('*******************************************************************************************') 

    print (' ... Done!')
else:
    print ('Bad request was made:')
    print (b)
raw_input('Press return key to exit ...')
    

    



