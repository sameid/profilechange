print ('KFDevMS-01 v0.08 \n')

import os
import json
import sys
import requests
import urllib
import urlparse
import getpass

cert ='cacert.pem'
os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(os.getcwd(), cert)

config = open('./config.json').read()
config = json.loads(config)

client_id = config['client_id']
profile_id = config['profile_id']
user = config['username']
verbose = config['verbose']

HOST = 'https://app.klipfolio.com/api/1'
##31637360
##user = raw_input('Username > ')
##pasw = getpass.getpass('Password > ')
##client_id = raw_input('Client ID > ')
##profile_id = raw_input('Profile ID > ')
##verbose = raw_input('Verbose (slow) [y/n] > ')

pasw = 'cust0m3r'

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
            
def post(req, data, headers, host=HOST):
    res = requests.post(host+req, auth=(user,pasw), data=json.dumps(data),headers=headers,verify=False)  
    return res.json()

def pprint(data):
    print ((json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '))))
    return;

##payload = {'name':'dpn-stress', 'description':'stress testing', 'seats':1, 'status':'active'}
##headers = {'content-type':'application/json'}      
##res = post(req='/clients', headers=headers, data=payload)
##
##pprint(res)

k = 0

##print ('Retrieving datasources for ' + client_id + ' ...')
b = get(req='/datasources')

if b['meta']['success'] == True and b['meta']['status'] == 200:
    a = b['data']['datasources']
##    print ('Changing profile IDs to ' + profile_id + ' ...')
    for i in a:
        ds = get(req='/datasources/'+i['id']+'?full=true')
        if ds['data']['connector'] == 'facebook' :
            pprint(ds)
            k = k + 1
##            try:
##                y = ds['data']['properties']['endpoint_url']
##            except KeyError:
##                break;
            
##            endpoint_url = parse_url(y, profile_id)
        
##            payload = {'properties': {'profile': profile_id, 'endpoint_url': endpoint_url, 'advancedQuery': endpoint_url}}
##            headers = {'content-type':'application/json'}
##            r = put (req='/datasources/'+i['id']+'/properties', data=payload, headers=headers )
    
##            if verbose == 'y':
##                print('*******************************************************************************************')
##                p = get(req='/datasources/' + i['id'] + '?full=true')
##                print p['data']['properties']['oauth_user_token']                
##                pretty_print_json(post(req='/datasources/'+i['id'] +'/@/refresh'))
##                print('*******************************************************************************************')

    break
    print k
    print (' ... Done!')
else:
    print ('Bad request was made:')
    print (b)
raw_input('Press return key to exit ...')
    

    



