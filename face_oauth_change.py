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
            
def post(req, host=HOST):
    res = requests.post(host+req, auth=(user,pasw), verify=False)  
    return res.json()

def pprint(data):
    print ((json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '))))
    return;

##payload = {'name':'dpn-stress', 'description':'stress testing', 'seats':1, 'status':'active'}
##headers = {'content-type':'application/json'}      
##res = post(req='/clients', headers=headers, data=payload)
##
##pprint(res)
out = 'CAAGWkt3iv1EBAOXqoo2Fp7fcIk6a5ZCedO6MivbR9QLr08ZCgAq3moQNUk5j4SWnkAZCTxoMMO9mFB1wLoLpEPlKSL8MiFSSQSZAIBYVvj5QQ3NZC7r34XSuMuT92oBhsWUlU0DAauRcanYkMl2T7CEwMfuZBqjIDwGxM02wBbAZAyZBWAzRTMnVHXdz8LL5oQcZD'
ti = '70ec362e767bc5cecf94d5ff900d0e01'
            
##print ('Retrieving datasources for ' + client_id + ' ...')
b = get(req='/datasources')
if b['meta']['success'] == True and b['meta']['status'] == 200:
    a = b['data']['datasources']
    for i in a:
##        i['id'] = '31a2696ff03893dcecb37b7b1715a76a'
        ds = get(req='/datasources/'+i['id']+'?full=true')
        if ds['data']['connector'] == 'facebook' and ds['data']['properties']['oauth_user_token'] != out :
            payload = {'properties': {'oauth_user_token': out, 'token_id': ti}}
            headers = {'content-type':'application/json'}
            r = put (req='/datasources/'+i['id']+'/properties', data=payload, headers=headers )
            pprint (post(req='/datasources/'+i['id'] +'/@/enable'))
            if verbose == 'y':
                print('*******************************************************************************************')
                pprint(get(req='/datasources/' + i['id'] + '?full=true'))
##                pprint (post(req='/datasources/'+i['id'] +'/@/refresh'))
                print('*******************************************************************************************')

##            break;
    print (' ... Done!')
else:
    print ('Bad request was made:')
    print (b)
raw_input('Press return key to exit ...')
    

    



